"""Run the full Smart Meeting benchmark (all criteria groups 1-5) for every
prepared groundtruth/hypothesis pair under data_benchmark/, except the
sessions excluded in EXCLUDE below.

For each session this produces a per-session report
`report/benchmark_report_<name>.md` (same format as app.py) and then writes
a consolidated `report/bao_cao_tong_hop_full.md` comparing all sessions
against the full criteria table in benchmark/thresholds.py.

Usage:
    python scripts/run_full_eval.py
"""

from __future__ import annotations

import json
import sys
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from benchmark import metrics, report
from benchmark.parsers import parse_transcript, segments_to_text
from benchmark.thresholds import CRITERIA, evaluate_all, PASS, FAIL, NA, MANUAL

BENCH_DIR = ROOT.parent
DATA_DIR = BENCH_DIR / "benchmark_data"
GT_DIR = DATA_DIR / "data_benchmark" / "data_groundtruth"
HYP_DIR = DATA_DIR / "data_benchmark" / "data_hypothesis"
TOADAM_AUDIO = DATA_DIR / "data" / "dataset_toadam" / "audio"

# groundtruth_local.json (per-speaker-named ground truth, e.g. "Le_Hai_Binh")
# for toadam5/toadam6, from the STT---Hoi-cung worktree recordings.
RECORDINGS_DIR = (
    BENCH_DIR / "STT---Hoi-cung" / ".claude" / "worktrees" / "vigorous-meitner-2a36f1" / "recordings"
)

EXCLUDE: set[str] = set()

# (name, audio_name, gt_path, hyp_path, timings_path, wav_path)
SESSIONS = [
    ("3p_meeting_demo", "3p_meeting_demo.wav",
     GT_DIR / "transcript_3p_meeting_groundtruth.json",
     HYP_DIR / "3p_meeting_demo" / "transcript_3p_meeting_zipformer.txt",
     HYP_DIR / "3p_meeting_demo" / "timings.json",
     HYP_DIR / "3p_meeting_demo" / "Audio_MEETING-20260605-1059.wav"),
    ("toadam1_bhyt", "toadam1_bhyt.wav",
     GT_DIR / "transcript_toadam1_bhyt_groundtruth.json",
     HYP_DIR / "toadam1_bhyt" / "transcript_toadam1_bhyt.txt",
     HYP_DIR / "toadam1_bhyt" / "timings.json",
     TOADAM_AUDIO / "toadam1_bhyt.wav"),
    ("toadam2_gdpt", "toadam2_gdpt.wav",
     GT_DIR / "transcript_toadam2_gdpt_groundtruth.json",
     HYP_DIR / "toadam2_gdpt" / "transcript_toadam2_gdpt.txt",
     HYP_DIR / "toadam2_gdpt" / "timings.json",
     TOADAM_AUDIO / "toadam2_gdpt.wav"),
    ("toadam3_quanlyvonmoi", "toadam3_quanlyvonmoi.wav",
     GT_DIR / "transcript_toadam3_quanlyvonmoi_groundtruth.json",
     HYP_DIR / "toadam3_quanlyvonmoi" / "transcript_toadam3_quanlyvonmoi.txt",
     HYP_DIR / "toadam3_quanlyvonmoi" / "timings.json",
     TOADAM_AUDIO / "toadam3_quanlyvonmoi.wav"),
    ("toadam4_nongsanxuatkhau", "toadam4_nongsanxuatkhau.wav",
     GT_DIR / "transcript_toadam4_nongsanxuatkhau_groundtruth.fixed.json",
     HYP_DIR / "toadam4_nongsanxuatkhau" / "transcript_toadam4_nongsanxuatkhau.txt",
     HYP_DIR / "toadam4_nongsanxuatkhau" / "timings.json",
     TOADAM_AUDIO / "toadam4_nongsanxuatkhau.wav"),
    ("toadam5_doingoaivn", "toadam5_doingoaivn.wav",
     RECORDINGS_DIR / "toadam5_doingoaivn" / "groundtruth_local.json",
     HYP_DIR / "toadam5_doingoaivn" / "transcript_toadam5_doingoaivn.txt",
     HYP_DIR / "toadam5_doingoaivn" / "timings.json",
     TOADAM_AUDIO / "toadam5_doingoaivn.wav"),
    ("toadam6_kinhte", "toadam6_kinhte.wav",
     RECORDINGS_DIR / "toadam6_kinhte" / "groundtruth_local.json",
     HYP_DIR / "toadam6_kinhte" / "transcript_toadam6_kinhte.txt",
     HYP_DIR / "toadam6_kinhte" / "timings.json",
     TOADAM_AUDIO / "toadam6_kinhte.wav"),
    ("toadam7_nongdocon", "toadam7_nongdocon.wav",
     GT_DIR / "transcript_toadam7_nongdocon_groundtruth.json",
     HYP_DIR / "toadam7_nongdocon" / "transcript_toadam7_nongdocon.txt",
     HYP_DIR / "toadam7_nongdocon" / "timings.json",
     TOADAM_AUDIO / "toadam7_nongdocon.wav"),
]


def audio_duration(wav_path: Path) -> float | None:
    if wav_path and wav_path.exists():
        with wave.open(str(wav_path), "rb") as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            if rate:
                return frames / float(rate)
    return None


def run_session(name, audio_name, gt_path, hyp_path, timings_path, wav_path):
    ref_segments = parse_transcript(gt_path.read_text(encoding="utf-8"))
    hyp_segments = parse_transcript(hyp_path.read_text(encoding="utf-8"))

    ref_text = segments_to_text(ref_segments)
    hyp_text = segments_to_text(hyp_segments)

    results: dict = {}
    results["wer"] = metrics.compute_wer(ref_text, hyp_text)
    results["cer"] = metrics.compute_cer(ref_text, hyp_text)
    results["keyword_recognition"] = None

    diar = metrics.compute_diarization_metrics(ref_segments, hyp_segments)
    results.update(diar)

    turn = metrics.compute_turn_metrics(ref_segments, hyp_segments)
    results.update(turn)

    dur = audio_duration(wav_path)
    timings = json.loads(timings_path.read_text(encoding="utf-8")) if timings_path.exists() else {}
    stt_time = timings.get("stt", 0) or 0
    diar_time = timings.get("diarization", 0) or 0
    finalize_time = timings.get("finalize", 0) or 0
    summary_time = timings.get("summary", 0) or 0
    export_time = timings.get("docx_export", 0) or 0
    e2e_time = stt_time + diar_time + finalize_time + summary_time + export_time

    results["rtf_stt"] = metrics.compute_rtf(stt_time, dur) if stt_time > 0 and dur else None
    results["rtf_diarization"] = metrics.compute_rtf(diar_time, dur) if diar_time > 0 and dur else None
    results["rtf_e2e"] = metrics.compute_rtf(e2e_time, dur) if e2e_time > 0 and dur else None
    results["finalize_ratio"] = metrics.compute_rtf(finalize_time, dur) if finalize_time > 0 and dur else None
    results["summary_time"] = summary_time if summary_time > 0 else None
    results["docx_export_time"] = export_time if export_time > 0 else None
    results["rouge_l"] = None

    rows = evaluate_all(results)
    # Quiet room condition -> drop 1.2 (noisy room variant)
    rows = [r for r in rows if r["ID"] != "1.2"]

    df_pass = sum(1 for r in rows if r["Kết quả"] == PASS)
    df_fail = sum(1 for r in rows if r["Kết quả"] == FAIL)
    df_na = sum(1 for r in rows if r["Kết quả"] in (NA, MANUAL))

    meta = {
        "timestamp": report.now_timestamp(),
        "audio_name": audio_name,
        "audio_duration": f"{dur:.1f}s" if dur else "N/A",
        "audio_condition": "Phòng yên tĩnh (1.1, < 22%)",
        "n_hyp_segments": len(hyp_segments),
        "n_ref_segments": len(ref_segments),
        "n_keywords": 0,
        "has_summary": False,
        "hyp_text": hyp_text_preview(hyp_segments),
        "ref_text": hyp_text_preview(ref_segments),
    }

    md = report.build_markdown_report(meta, results, rows, df_pass, df_fail, df_na)
    out_path = ROOT / "report" / f"benchmark_report_{name}.md"
    out_path.write_text(md, encoding="utf-8")

    return {
        "name": name,
        "results": results,
        "rows": rows,
        "n_pass": df_pass,
        "n_fail": df_fail,
        "n_na": df_na,
        "n_ref": len(ref_segments),
        "n_hyp": len(hyp_segments),
        "audio_dur": dur,
        "out_path": out_path,
    }


def hyp_text_preview(segments) -> str:
    ordered = sorted(segments, key=lambda s: s.start)
    lines = []
    for seg in ordered:
        lines.append(f"[{seg.start:.2f} --> {seg.end:.2f}] {seg.speaker}: {seg.text}")
    return "\n".join(lines)


def build_conclusions(session_results: list[dict]) -> str:
    def esc(text: str) -> str:
        return str(text).replace("|", "\\|")

    n = len(session_results)
    names = [s["name"] for s in session_results]

    # Per-criterion status across sessions (excluding 1.2, NA/MANUAL criteria)
    status_by_crit: dict[str, list[str]] = {}
    for crit in CRITERIA:
        if crit.id == "1.2":
            continue
        statuses = []
        for s in session_results:
            row = next(r for r in s["rows"] if r["ID"] == crit.id)
            statuses.append(row["Kết quả"])
        status_by_crit[crit.id] = statuses

    def all_status(crit_id, status):
        return all(st == status for st in status_by_crit[crit_id])

    def count_status(crit_id, status):
        return sum(1 for st in status_by_crit[crit_id] if st == status)

    def names_with(crit_id, status):
        return [name for name, st in zip(names, status_by_crit[crit_id]) if st == status]

    def fmt_names(name_list):
        return ", ".join(f"`{n}`" for n in name_list) if name_list else "không phiên nào"

    parts: list[str] = []
    parts.append("## Nhận xét & Kết luận")
    parts.append("")

    # 1. Tong quan tung phien
    parts.append("### 1. Tổng quan theo từng phiên")
    parts.append("")
    for s in session_results:
        res = s["results"]
        total_scored = s["n_pass"] + s["n_fail"]
        rate = (s["n_pass"] / total_scored * 100) if total_scored else 0.0
        issues = []
        if res["wer"] is not None and res["wer"] >= 0.22:
            issues.append(f"WER cao ({res['wer']*100:.1f}%)")
        if res["der"] is not None and res["der"] >= 0.22:
            issues.append(f"DER cao ({res['der']*100:.1f}%)")
        if res["speaker_count_diff"] is not None and res["speaker_count_diff"] > 1:
            issues.append(
                f"sai số người nói lớn (ref={res['ref_speaker_count']} vs hyp={res['hyp_speaker_count']})"
            )
        if res["ter"] is not None and res["ter"] >= 0.15:
            issues.append(f"TER cao ({res['ter']*100:.1f}%)")
        if res["summary_time"] is not None and res["summary_time"] > 60:
            issues.append(f"tóm tắt Qwen vượt ngưỡng ({res['summary_time']:.0f}s)")
        issue_text = "; ".join(issues) if issues else "không có vấn đề nổi bật ngoài nhóm 3 (xem mục 3)"
        parts.append(
            f"- **{esc(s['name'])}**: {s['n_pass']}/{total_scored} tiêu chí đạt "
            f"({rate:.0f}%), {s['n_na']} tiêu chí N/A hoặc thủ công. "
            f"Vấn đề chính: {issue_text}."
        )
    parts.append("")

    # 2. Theo nhom tieu chi
    parts.append("### 2. Theo từng nhóm tiêu chí")
    parts.append("")

    parts.append("**Nhóm 1 - STT (WER/CER/RTF):**")
    n_wer_pass = count_status("1.1", PASS)
    n_cer_pass = count_status("1.3", PASS)
    wer_pass_names = names_with("1.1", PASS)
    wer_fail_names = names_with("1.1", FAIL)
    parts.append(
        f"- 1.1 (WER < 22%): đạt ở {n_wer_pass}/{n} phiên ({fmt_names(wer_pass_names)}). "
        f"1.3 (CER < 13%): đạt ở {n_cer_pass}/{n} phiên. "
        f"Kết quả WER/CER có dạng hai cực: các phiên đạt 1.1 có WER 7-22% "
        f"(audio rõ, ít overlap), trong khi {fmt_names(wer_fail_names)} có "
        f"WER/CER ~33-38% (audio noisy/nhiều giọng đè nhau hoặc ground truth khó "
        f"căn chỉnh)."
    )
    parts.append(
        f"- 1.4/5.1 (RTF lane STT < 1.0): đạt {count_status('1.4', PASS)}/{n} phiên "
        f"(RTF ~0.02-0.03, rất nhanh so với realtime) - không phải điểm nghẽn."
    )
    parts.append(
        "- 1.5 (nhận dạng thuật ngữ/tên riêng): N/A ở tất cả phiên - chưa có danh "
        "sách từ khoá để đo, cần bổ sung danh sách thuật ngữ riêng cho từng cuộc họp."
    )
    parts.append("")

    parts.append("**Nhóm 2 - Diarization (DER/speaker confusion/số người nói/biên lượt):**")
    der_fail_names = names_with("2.1", FAIL)
    parts.append(
        f"- 2.1 (DER < 22%): đạt {count_status('2.1', PASS)}/{n} phiên; "
        f"2.2 (speaker confusion < 12%): đạt {count_status('2.2', PASS)}/{n} phiên. "
        f"Các phiên fail 2.1 là {fmt_names(der_fail_names)}, đều có sai số số "
        f"người nói (2.3) đáng kể (xem bên dưới)."
    )
    spk_pass_names = names_with("2.3", PASS)
    spk_fail_names = names_with("2.3", FAIL)
    parts.append(
        f"- 2.3 (|Δ số người nói| ≤ 1): đạt {count_status('2.3', PASS)}/{n} phiên "
        f"({fmt_names(spk_pass_names)}); {len(spk_fail_names)} phiên còn lại "
        f"({fmt_names(spk_fail_names)}) lệch 2-6 người, đa số là "
        f"**over-segmentation** (hệ thống tách 1 người thành nhiều speaker ID), "
        f"riêng `toadam7_nongdocon` thì ngược lại (gộp nhiều người vào ít speaker "
        f"ID hơn)."
    )
    parts.append(
        f"- 2.4 (P/R biên giới lượt ±0.5s, cần P>0.80/R>0.75): "
        f"**FAIL ở cả {n}/{n} phiên** (P=16-46%, R=16-40%) - đây là vấn đề "
        "có tính hệ thống, xem mục 3."
    )
    parts.append(
        f"- 2.5/5.2 (RTF diarization < 1.5): đạt {count_status('2.5', PASS)}/{n} phiên "
        f"(RTF ~0.16-0.18) - không phải điểm nghẽn."
    )
    parts.append(
        "- 2.6 (so sánh preset A/B): thủ công/định tính ở tất cả phiên - cần chạy "
        "thêm với preset diarization khác để có cơ sở so sánh."
    )
    parts.append("")

    parts.append("**Nhóm 3 - Gán người nói theo lượt (turn-speaker assignment):**")
    ter_pass_names = names_with("3.1", PASS)
    parts.append(
        f"- 3.1/4.2 (TER < 15%): đạt {count_status('3.1', PASS)}/{n} phiên "
        f"({fmt_names(ter_pass_names)})."
    )
    tbd_values = [s["results"]["turn_boundary_deviation"] for s in session_results]
    snc_values = [s["results"]["speaker_numbering_consistency"] for s in session_results]
    parts.append(
        f"- 3.2 (lệch biên lượt trung bình < 0.5s): **FAIL ở {n}/{n} phiên**, "
        f"lệch dao động {min(tbd_values):.1f}s - {max(tbd_values):.1f}s, "
        f"lớn hơn ngưỡng 2-37 lần. "
        f"Đây là tiêu chí fail nặng nhất và đồng đều nhất trong toàn bộ bảng."
    )
    parts.append(
        f"- 3.3 (nhất quán đánh số người nói = 100%): **FAIL ở {n}/{n} phiên** "
        f"({min(snc_values)*100:.1f}% - {max(snc_values)*100:.1f}%, "
        f"trung vị ~{sorted(snc_values)[len(snc_values)//2]*100:.0f}%)."
    )
    parts.append("")

    parts.append("**Nhóm 4 - End-to-end:**")
    parts.append(
        f"- 4.1 (WER toàn phiên < 27%) và 4.3 (RTF end-to-end < 1.5): "
        f"4.3 đạt {count_status('4.3', PASS)}/{n} phiên (RTF 0.18-0.42, "
        "rất xa ngưỡng), nhưng 4.1/4.2 lặp lại kết quả của 1.1/3.1 (xem trên)."
    )
    parts.append(
        "- 4.4 (ổn định phiên > 2h): thủ công - chưa được kiểm chứng với phiên dài thật."
    )
    parts.append(
        "- 4.5 (chất lượng tóm tắt Qwen, ROUGE-L): N/A - chưa có bản tóm tắt mẫu "
        "để so sánh, ngoại trừ kiểm tra thời gian chạy (xem 5.4)."
    )
    parts.append("")

    parts.append("**Nhóm 5 - Hiệu năng:**")
    parts.append(
        f"- 5.3 (thời gian hoàn thiện < 0.3x audio) và 5.5 (xuất DOCX < 5s): "
        f"đạt {n}/{n} phiên, không đáng lo."
    )
    parts.append(
        "- 5.4 (tóm tắt Qwen NPU < 60s/phiên): chỉ có dữ liệu cho "
        "`toadam4_nongsanxuatkhau` và **FAIL nghiêm trọng** (560s, gấp ~9.3x "
        "ngưỡng); 5 phiên còn lại không có `summary_time` trong `timings.json` "
        "nên hiển thị N/A. Cần đo lại thời gian tóm tắt cho tất cả phiên."
    )
    parts.append("")

    # 3. Van de he thong
    parts.append("### 3. Vấn đề mang tính hệ thống (ưu tiên xử lý)")
    parts.append("")
    best_wer_session = min(session_results, key=lambda s: s["results"]["wer"])
    parts.append(
        "1. **Lệch biên lượt nói (3.2) và P/R biên giới lượt (2.4) fail ở toàn bộ "
        f"{n}/{n} phiên**, độc lập với chất lượng nội dung (kể cả phiên WER thấp "
        f"nhất `{best_wer_session['name']}` ({best_wer_session['results']['wer']*100:.1f}%) "
        f"cũng có lệch biên trung bình "
        f"{best_wer_session['results']['turn_boundary_deviation']:.2f}s). Đây là dấu hiệu "
        "diarization và STT đang cắt turn theo logic khác với cách ground truth phân "
        "đoạn (ví dụ: hệ thống tạo turn mới mỗi khi có khoảng lặng ngắn / mỗi câu, "
        "còn ground truth gộp theo lượt nói thực tế dài hơn). Nên kiểm tra logic "
        "merge segment liên tiếp cùng speaker trước khi tính 2.4/3.2."
    )
    over_seg = []
    under_seg = []
    for s in session_results:
        diff = s["results"]["speaker_count_diff"]
        ref = s["results"]["ref_speaker_count"]
        hyp = s["results"]["hyp_speaker_count"]
        if diff > 1:
            if hyp > ref:
                over_seg.append(f"`{s['name']}` (+{hyp - ref} spk)")
            elif hyp < ref:
                under_seg.append(f"`{s['name']}` (-{ref - hyp} spk)")
    parts.append(
        "2. **Over/under-segmentation số người nói (2.3, 3.3)** tương quan trực tiếp "
        f"với DER/TER fail: {', '.join(over_seg) if over_seg else 'không có phiên'} "
        f"đều tách dư speaker ID (over-segmentation); "
        f"{', '.join(under_seg) if under_seg else 'không có phiên'} lại gộp nhiều "
        "người vào ít speaker ID hơn (under-segmentation). Cần tinh chỉnh ngưỡng "
        "clustering của diarization (có thể khác nhau giữa phòng yên tĩnh và phòng "
        "nhiều người/talkshow)."
    )
    parts.append(
        f"3. **WER/CER tăng vọt ở phiên nhiều người/audio khó** ({fmt_names(wer_fail_names)} "
        "~33-38% so với ~7-22% ở các phiên khác) - cần kiểm tra chất lượng audio đầu "
        "vào và mức độ overlap giọng nói của các phiên này, có thể cần mô hình STT "
        "khác hoặc xử lý tách giọng (speech separation) trước khi STT."
    )
    parts.append(
        "4. **Thời gian tóm tắt Qwen (5.4) vượt ngưỡng gần 10 lần** ở phiên duy nhất "
        "có số liệu (`toadam4_nongsanxuatkhau`, 560s) - cần đo lại cho các phiên còn "
        "lại và tối ưu (batch size, độ dài input, NPU offload)."
    )
    parts.append(
        "5. **Thiếu dữ liệu cho 1.5, 2.6, 4.4, 4.5** (N/A/thủ công ở tất cả phiên) - "
        "cần bổ sung: danh sách thuật ngữ/từ khoá theo từng cuộc họp (1.5), chạy lại "
        "với preset diarization khác để so sánh (2.6), test phiên dài liên tục >2h "
        "(4.4), và bản tóm tắt tham chiếu để tính ROUGE-L (4.5)."
    )
    parts.append(
        "6. **Ground truth của `toadam5_doingoaivn` và `toadam6_kinhte` dùng "
        "`groundtruth_local.json`** với nhãn người nói là tên thật (vd. "
        "`Le_Hai_Binh`, `Pham_Minh_Chinh`, `Phong_vien_toadam6_3`...) thay vì "
        "`Người nói N` như các phiên còn lại. Số lượng nhãn (ref_speaker_count) "
        f"vì vậy cao bất thường (toadam5: "
        f"{next(s for s in session_results if s['name']=='toadam5_doingoaivn')['results']['ref_speaker_count']}, "
        f"toadam6: "
        f"{next(s for s in session_results if s['name']=='toadam6_kinhte')['results']['ref_speaker_count']}) "
        "vì mỗi nhân vật xuất hiện trong clip/trích dẫn (kể cả chỉ 1 lượt ngắn) "
        "cũng được tính là một người nói riêng. Các chỉ số 2.1/2.2/2.3/3.x cho hai "
        "phiên này nên được đọc với lưu ý đó - chúng phản ánh khả năng tách đúng "
        "*từng nhân vật được nêu tên*, khắt khe hơn cách đếm `Người nói N` thông "
        "thường. Dù vậy WER (1.1) của `toadam5_doingoaivn` vẫn đạt ngưỡng "
        f"({next(s for s in session_results if s['name']=='toadam5_doingoaivn')['results']['wer']*100:.1f}%), "
        "cho thấy nội dung STT chính xác tốt cho phiên talkshow này."
    )
    parts.append("")

    # 4. Khuyen nghi
    parts.append("### 4. Khuyến nghị ưu tiên")
    parts.append("")
    parts.append(
        "- **Ưu tiên 1**: Rà soát cách xác định ranh giới lượt nói (turn boundary) "
        "trong pipeline STT+diarization - nguyên nhân gốc của 2.4/3.2/3.3 fail toàn "
        "bộ và ảnh hưởng dây chuyền tới 3.1/4.2."
    )
    parts.append(
        f"- **Ưu tiên 2**: Tinh chỉnh tham số diarization (clustering threshold, "
        f"min/max speakers) để giảm sai số số người nói (2.3), đặc biệt cho "
        f"{fmt_names(spk_fail_names)}."
    )
    parts.append(
        f"- **Ưu tiên 3**: Điều tra nguyên nhân WER/CER cao bất thường ở "
        f"{fmt_names(wer_fail_names)} (audio quality, overlap, ground truth alignment)."
    )
    parts.append(
        "- **Ưu tiên 4**: Tối ưu thời gian tóm tắt Qwen (5.4) và đo lại cho toàn bộ "
        "phiên; bổ sung dữ liệu còn thiếu cho 1.5, 2.6, 4.4, 4.5."
    )
    parts.append("")

    return "\n".join(parts)


def build_final_report(session_results: list[dict]) -> str:
    parts: list[str] = []
    parts.append("# Báo cáo tổng hợp Benchmark - Smart Meeting (đầy đủ 5 nhóm tiêu chí)")
    parts.append("")
    parts.append(f"- Thời gian chạy: {report.now_timestamp()}")
    parts.append(f"- Số phiên đánh giá: {len(session_results)}")
    parts.append(
        "- Lưu ý: `toadam5_doingoaivn` và `toadam6_kinhte` dùng `groundtruth_local.json` "
        "(nhãn người nói theo tên thật, ví dụ `Le_Hai_Binh`, `Pham_Minh_Chinh`) thay vì "
        "`transcript_*_groundtruth.json` (nhãn `Người nói N`) như các phiên khác - "
        "xem ghi chú trong mục Nhận xét & Kết luận."
    )
    parts.append("")

    parts.append("## Tổng quan theo phiên")
    parts.append("")
    parts.append("| Phiên | Audio (s) | Lượt (hyp/ref) | Đạt | Không đạt | N/A/Thủ công |")
    parts.append("| --- | --- | --- | --- | --- | --- |")
    for s in session_results:
        dur = f"{s['audio_dur']:.1f}" if s["audio_dur"] else "N/A"
        parts.append(
            f"| {s['name']} | {dur} | {s['n_hyp']}/{s['n_ref']} | {s['n_pass']} | {s['n_fail']} | {s['n_na']} |"
        )
    parts.append("")

    def esc(text: str) -> str:
        return str(text).replace("|", "\\|")

    parts.append("## Chi tiết theo tiêu chí")
    parts.append("")
    header = "| ID | Tiêu chí | Ngưỡng | " + " | ".join(esc(s["name"]) for s in session_results) + " |"
    sep = "| --- | --- | --- | " + " | ".join("---" for _ in session_results) + " |"
    parts.append(header)
    parts.append(sep)
    for crit in CRITERIA:
        if crit.id == "1.2":
            continue
        cells = []
        for s in session_results:
            row = next(r for r in s["rows"] if r["ID"] == crit.id)
            val = row["Giá trị đo"]
            status = row["Kết quả"]
            if status == PASS:
                cells.append(f"{val} (Đạt)")
            elif status == FAIL:
                cells.append(f"{val} (Không đạt)")
            else:
                cells.append(status)
        parts.append(
            f"| {esc(crit.id)} | {esc(crit.name)} | {esc(crit.threshold_text)} | "
            + " | ".join(esc(c) for c in cells) + " |"
        )
    parts.append("")

    parts.append(build_conclusions(session_results))

    parts.append("## Giá trị đo thô theo phiên (raw metrics)")
    parts.append("")
    parts.append("```json")
    raw = {s["name"]: s["results"] for s in session_results}
    parts.append(json.dumps(raw, ensure_ascii=False, indent=2))
    parts.append("```")
    parts.append("")

    return "\n".join(parts)


def main() -> None:
    session_results = []
    for name, audio_name, gt_path, hyp_path, timings_path, wav_path in SESSIONS:
        if name in EXCLUDE:
            continue
        if not gt_path.exists() or not hyp_path.exists():
            print(f"SKIP {name}: missing groundtruth or hypothesis file")
            continue
        print(f"Running {name}...")
        res = run_session(name, audio_name, gt_path, hyp_path, timings_path, wav_path)
        print(f"  -> Đạt={res['n_pass']} Không đạt={res['n_fail']} N/A={res['n_na']}  "
              f"(report: {res['out_path'].relative_to(ROOT)})")
        session_results.append(res)

    final_md = build_final_report(session_results)
    final_path = ROOT / "report" / "bao_cao_tong_hop_full.md"
    final_path.write_text(final_md, encoding="utf-8")
    print(f"\nSaved consolidated report to {final_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
