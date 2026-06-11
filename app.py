"""Streamlit benchmark tool for the Smart Meeting STT/Diarization/Summarization
pipeline, implementing the criteria from Benchmarking_SmartMeeting.docx.

Run with:
    streamlit run app.py
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from benchmark import metrics, report
from benchmark.parsers import parse_transcript, segments_to_text
from benchmark.thresholds import FAIL, MANUAL, NA, PASS, evaluate_all

st.set_page_config(page_title="Smart Meeting Benchmark", layout="wide")

st.title("Smart Meeting - Công cụ Benchmark")
st.caption(
    "Đối chiếu transcript / thời gian xử lý của hệ thống với dữ liệu tham chiếu (ground truth) "
    "và so sánh với bộ tiêu chí trong Benchmarking_SmartMeeting.docx"
)


def _read_text(uploaded_file, pasted_text: str) -> str:
    if uploaded_file is not None:
        return uploaded_file.read().decode("utf-8")
    return pasted_text or ""


def _parse_or_none(content: str, label: str):
    if not content.strip():
        return None
    try:
        return parse_transcript(content)
    except ValueError as exc:
        st.error(f"Không thể đọc transcript '{label}': {exc}")
        return None


# ---------------------------------------------------------------------------
# Sidebar - inputs
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("1. Audio")
    audio_file = st.file_uploader("File audio (WAV 16kHz mono)", type=["wav"])
    audio_duration = None
    if audio_file is not None:
        audio_duration = metrics.get_audio_duration_seconds(audio_file.read())
        if audio_duration:
            st.success(f"Thời lượng audio: {audio_duration:.1f}s")
        else:
            st.warning("Không đọc được thời lượng từ file WAV.")
    if audio_duration is None:
        manual_duration = st.number_input(
            "Hoặc nhập thời lượng audio (giây)", min_value=0.0, value=0.0, step=1.0
        )
        audio_duration = manual_duration or None

    audio_condition = st.radio(
        "Điều kiện audio (cho tiêu chí 1.1 / 1.2)",
        options=["Phòng yên tĩnh (1.1, < 22%)", "Có nhiễu / phòng vang (1.2, < 38%)"],
    )

    st.header("2. Transcript - Hệ thống (Hypothesis)")
    hyp_file = st.file_uploader(
        "File transcript hệ thống (.json/.txt)", type=["json", "txt"], key="hyp_file"
    )
    hyp_text_input = st.text_area(
        "...hoặc dán transcript hệ thống vào đây",
        height=120,
        placeholder="[00:00:00.000 --> 00:00:03.500] Người nói 1: nội dung...",
        key="hyp_text",
    )

    st.header("3. Transcript - Tham chiếu (Reference / Ground truth)")
    ref_file = st.file_uploader(
        "File transcript tham chiếu (.json/.txt)", type=["json", "txt"], key="ref_file"
    )
    ref_text_input = st.text_area(
        "...hoặc dán transcript tham chiếu vào đây",
        height=120,
        placeholder="[00:00:00.000 --> 00:00:03.500] Người nói 1: nội dung...",
        key="ref_text",
    )

    st.header("4. Từ khoá / thuật ngữ")
    keyword_text = st.text_area(
        "Danh sách từ khoá, mỗi dòng 1 từ (50-100 từ họp thường gặp)",
        height=80,
        placeholder="ngân sách\nKPI\nđối tác\n...",
    )

    st.header("5. Tóm tắt phiên họp")
    ref_summary_text = st.text_area("Bản tóm tắt mẫu (tham chiếu)", height=80)
    hyp_summary_text = st.text_area("Bản tóm tắt hệ thống tạo ra", height=80)

    st.header("6. Thời gian xử lý đo thực tế (giây)")
    col1, col2 = st.columns(2)
    with col1:
        stt_time = st.number_input("Thời gian STT", min_value=0.0, value=0.0, step=0.1)
        diar_time = st.number_input("Thời gian diarization", min_value=0.0, value=0.0, step=0.1)
        finalize_time = st.number_input("Thời gian hoàn thiện (finalize)", min_value=0.0, value=0.0, step=0.1)
    with col2:
        summary_time = st.number_input("Thời gian tóm tắt (Qwen)", min_value=0.0, value=0.0, step=0.1)
        export_time = st.number_input("Thời gian xuất DOCX", min_value=0.0, value=0.0, step=0.1)

    auto_e2e = st.checkbox("Tự động tính RTF end-to-end = tổng các giai đoạn trên", value=True)
    if auto_e2e:
        e2e_time = stt_time + diar_time + finalize_time + summary_time + export_time
        st.caption(f"Tổng thời gian end-to-end (tự động) = {e2e_time:.2f}s")
    else:
        e2e_time = st.number_input("Thời gian end-to-end (giây)", min_value=0.0, value=0.0, step=0.1)

    run_clicked = st.button("Chạy benchmark", type="primary")


# ---------------------------------------------------------------------------
# Parse inputs
# ---------------------------------------------------------------------------
hyp_content = _read_text(hyp_file, hyp_text_input)
ref_content = _read_text(ref_file, ref_text_input)

hyp_segments = _parse_or_none(hyp_content, "hệ thống (hypothesis)")
ref_segments = _parse_or_none(ref_content, "tham chiếu (reference)")

with st.expander("Xem trước transcript đã phân tích", expanded=False):
    col_hyp, col_ref = st.columns(2)
    with col_hyp:
        st.subheader("Hệ thống (Hypothesis)")
        if hyp_segments:
            st.dataframe(
                pd.DataFrame([s.__dict__ for s in hyp_segments]), width="stretch", height=250
            )
        else:
            st.info("Chưa có dữ liệu.")
    with col_ref:
        st.subheader("Tham chiếu (Reference)")
        if ref_segments:
            st.dataframe(
                pd.DataFrame([s.__dict__ for s in ref_segments]), width="stretch", height=250
            )
        else:
            st.info("Chưa có dữ liệu.")


# ---------------------------------------------------------------------------
# Run benchmark
# ---------------------------------------------------------------------------
if run_clicked:
    if not hyp_segments or not ref_segments:
        st.error("Cần cung cấp cả transcript hệ thống và transcript tham chiếu để chạy benchmark.")
    else:
        hyp_text = segments_to_text(hyp_segments)
        ref_text = segments_to_text(ref_segments)

        results: dict = {}

        # Nhom 1: STT
        results["wer"] = metrics.compute_wer(ref_text, hyp_text)
        results["cer"] = metrics.compute_cer(ref_text, hyp_text)

        keyword_list = [k.strip() for k in keyword_text.splitlines() if k.strip()]
        if keyword_list:
            kw = metrics.compute_keyword_recognition(ref_text, hyp_text, keyword_list)
            results["keyword_recognition"] = kw["keyword_recognition"]
        else:
            results["keyword_recognition"] = None

        # Nhom 2: Diarization
        diar = metrics.compute_diarization_metrics(ref_segments, hyp_segments)
        results.update(diar)

        # Nhom 3: Turn assignment
        turn_metrics = metrics.compute_turn_metrics(ref_segments, hyp_segments)
        results.update(turn_metrics)

        # Nhom 4 & 5: RTF / timing
        results["rtf_stt"] = metrics.compute_rtf(stt_time, audio_duration) if stt_time > 0 else None
        results["rtf_diarization"] = metrics.compute_rtf(diar_time, audio_duration) if diar_time > 0 else None
        results["rtf_e2e"] = metrics.compute_rtf(e2e_time, audio_duration) if e2e_time > 0 else None
        results["finalize_ratio"] = metrics.compute_rtf(finalize_time, audio_duration) if finalize_time > 0 else None
        results["summary_time"] = summary_time if summary_time > 0 else None
        results["docx_export_time"] = export_time if export_time > 0 else None

        # Nhom 4.5: Summary quality
        if ref_summary_text.strip() and hyp_summary_text.strip():
            results["rouge_l"] = metrics.compute_rouge_l(ref_summary_text, hyp_summary_text)
        else:
            results["rouge_l"] = None

        rows = evaluate_all(results)

        # Hide whichever of 1.1 / 1.2 doesn't match the chosen audio condition
        if audio_condition.startswith("Phòng yên tĩnh"):
            rows = [r for r in rows if r["ID"] != "1.2"]
        else:
            rows = [r for r in rows if r["ID"] != "1.1"]

        df = pd.DataFrame(rows)

        n_pass = int((df["Kết quả"] == PASS).sum())
        n_fail = int((df["Kết quả"] == FAIL).sum())
        n_na = int((df["Kết quả"].isin([NA, MANUAL])).sum())

        meta = {
            "timestamp": report.now_timestamp(),
            "audio_name": audio_file.name if audio_file is not None else "N/A",
            "audio_duration": f"{audio_duration:.1f}s" if audio_duration else "N/A",
            "audio_condition": audio_condition,
            "n_hyp_segments": len(hyp_segments),
            "n_ref_segments": len(ref_segments),
            "n_keywords": len(keyword_list),
            "has_summary": bool(ref_summary_text.strip() and hyp_summary_text.strip()),
            "timings_seconds": {
                "stt": stt_time,
                "diarization": diar_time,
                "finalize": finalize_time,
                "summary": summary_time,
                "docx_export": export_time,
                "end_to_end": e2e_time,
            },
            "hyp_text": hyp_content,
            "ref_text": ref_content,
        }

        # Persist everything needed to redraw the results, so that clicking a
        # download button (which triggers a Streamlit rerun) doesn't make the
        # whole results section disappear.
        st.session_state["benchmark_run"] = {
            "results": results,
            "rows": rows,
            "n_pass": n_pass,
            "n_fail": n_fail,
            "n_na": n_na,
            "meta": meta,
        }


# ---------------------------------------------------------------------------
# Display results (persisted in session_state so download buttons don't
# clear the page on rerun)
# ---------------------------------------------------------------------------
run_data = st.session_state.get("benchmark_run")

if run_data is None:
    st.info("Nhập dữ liệu ở thanh bên trái rồi nhấn 'Chạy benchmark'.")
else:
    results = run_data["results"]
    rows = run_data["rows"]
    n_pass = run_data["n_pass"]
    n_fail = run_data["n_fail"]
    n_na = run_data["n_na"]
    meta = run_data["meta"]
    df = pd.DataFrame(rows)

    st.header("Kết quả")

    m1, m2, m3 = st.columns(3)
    m1.metric("Đạt", n_pass)
    m2.metric("Không đạt", n_fail)
    m3.metric("N/A / Thủ công", n_na)

    def _highlight(row):
        if row["Kết quả"] == PASS:
            color = "background-color: #d4edda"
        elif row["Kết quả"] == FAIL:
            color = "background-color: #f8d7da"
        else:
            color = "background-color: #f0f0f0"
        return [color] * len(row)

    for group in df["Nhóm"].unique():
        st.subheader(group)
        group_df = df[df["Nhóm"] == group].drop(columns=["Nhóm"])
        st.dataframe(
            group_df.style.apply(_highlight, axis=1),
            width="stretch",
            hide_index=True,
        )

    with st.expander("Chi tiết giá trị đo được (raw)"):
        st.json({k: v for k, v in results.items()})

    # ------------------------------------------------------------------
    # Export report
    # ------------------------------------------------------------------
    st.header("Xuất báo cáo")
    st.caption("Tải báo cáo để lưu lại hoặc gửi đi đánh giá.")

    md_report = report.build_markdown_report(meta, results, rows, n_pass, n_fail, n_na)
    json_report = report.build_json_report(meta, results, rows, n_pass, n_fail, n_na)
    csv_report = df.to_csv(index=False)

    # Freeze the filename timestamp at run time (stored in meta) so it stays
    # stable across reruns triggered by the download buttons themselves.
    timestamp_slug = meta["timestamp"].replace(" ", "_").replace(":", "-")
    col_md, col_json, col_csv = st.columns(3)
    with col_md:
        st.download_button(
            "Tải báo cáo Markdown (.md)",
            data=md_report,
            file_name=f"benchmark_report_{timestamp_slug}.md",
            mime="text/markdown",
            key="download_md",
        )
    with col_json:
        st.download_button(
            "Tải báo cáo JSON (.json)",
            data=json_report,
            file_name=f"benchmark_report_{timestamp_slug}.json",
            mime="application/json",
            key="download_json",
        )
    with col_csv:
        st.download_button(
            "Tải bảng kết quả CSV (.csv)",
            data=csv_report,
            file_name=f"benchmark_results_{timestamp_slug}.csv",
            mime="text/csv",
            key="download_csv",
        )
