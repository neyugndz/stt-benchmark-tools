"""Acceptance criteria (Bo tieu chi de xuat - Muc V) from Benchmarking_SmartMeeting.docx,
encoded as comparisons against the metrics computed in benchmark/metrics.py.

Each criterion knows which metric key(s) it needs from the `results` dict
produced by the Streamlit app, how to format the measured value, and how to
decide PASS / FAIL / N/A / MANUAL.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional

PASS = "Đạt"
FAIL = "Không đạt"
NA = "N/A"
MANUAL = "Thủ công / định tính"


def fmt_pct(value: Optional[float]) -> str:
    return "N/A" if value is None else f"{value * 100:.1f}%"


def fmt_num(value: Optional[float], unit: str = "") -> str:
    return "N/A" if value is None else f"{value:.2f}{unit}"


@dataclass
class Criterion:
    id: str
    group: int
    group_name: str
    name: str
    threshold_text: str
    method_text: str
    priority: str
    metric_keys: list[str]
    value_fn: Callable[[dict], Optional[str]]
    status_fn: Callable[[dict], str]
    extra_keys: list[str] = field(default_factory=list)

    def evaluate(self, results: dict) -> dict:
        if not all(results.get(k) is not None for k in self.metric_keys):
            return {
                "ID": self.id,
                "Nhóm": self.group_name,
                "Tiêu chí": self.name,
                "Ngưỡng": self.threshold_text,
                "Giá trị đo": NA,
                "Kết quả": NA,
                "Ưu tiên": self.priority,
                "Cách đo": self.method_text,
            }
        return {
            "ID": self.id,
            "Nhóm": self.group_name,
            "Tiêu chí": self.name,
            "Ngưỡng": self.threshold_text,
            "Giá trị đo": self.value_fn(results),
            "Kết quả": self.status_fn(results),
            "Ưu tiên": self.priority,
            "Cách đo": self.method_text,
        }


def _lt(threshold: float):
    return lambda r, k: PASS if r[k] < threshold else FAIL


def _gt(threshold: float):
    return lambda r, k: PASS if r[k] > threshold else FAIL


def _le_abs(threshold: float):
    return lambda r, k: PASS if abs(r[k]) <= threshold else FAIL


GROUP_1 = "Nhóm 1 - Nhận dạng giọng nói"
GROUP_2 = "Nhóm 2 - Phân tách người nói "
GROUP_3 = "Nhóm 3 - Gán người nói theo overlap"
GROUP_4 = "Nhóm 4 - Hệ thống đầu cuối (end-to-end)"
GROUP_5 = "Nhóm 5 - Hiệu năng & độ trễ"


CRITERIA: list[Criterion] = [
    # ---------------- Nhom 1 ----------------
    Criterion(
        id="1.1",
        group=1,
        group_name=GROUP_1,
        name="WER - phòng yên tĩnh",
        threshold_text="< 22%",
        method_text="jiwer.wer(ref,hyp) sau chuẩn hoá; audio sạch",
        priority="Cao",
        metric_keys=["wer"],
        value_fn=lambda r: fmt_pct(r["wer"]),
        status_fn=lambda r: _lt(0.22)(r, "wer"),
    ),
    Criterion(
        id="1.2",
        group=1,
        group_name=GROUP_1,
        name="WER - có nhiễu / phòng vang",
        threshold_text="< 38%",
        method_text="jiwer.wer(ref,hyp); audio nhiễu, chất lượng thấp",
        priority="TB",
        metric_keys=["wer"],
        value_fn=lambda r: fmt_pct(r["wer"]),
        status_fn=lambda r: _lt(0.38)(r, "wer"),
    ),
    Criterion(
        id="1.3",
        group=1,
        group_name=GROUP_1,
        name="CER - tiếng Việt có dấu",
        threshold_text="< 13%",
        method_text="jiwer.cer(ref,hyp)",
        priority="Cao",
        metric_keys=["cer"],
        value_fn=lambda r: fmt_pct(r["cer"]),
        status_fn=lambda r: _lt(0.13)(r, "cer"),
    ),
    Criterion(
        id="1.4",
        group=1,
        group_name=GROUP_1,
        name="RTF lane STT (realtime)",
        threshold_text="< 1.0",
        method_text="thời gian xử lý STT / thời lượng audio",
        priority="Rất cao",
        metric_keys=["rtf_stt"],
        value_fn=lambda r: fmt_num(r["rtf_stt"]),
        status_fn=lambda r: _lt(1.0)(r, "rtf_stt"),
    ),
    Criterion(
        id="1.5",
        group=1,
        group_name=GROUP_1,
        name="Nhận dạng thuật ngữ / tên riêng",
        threshold_text="> 80%",
        method_text="Danh sách 50-100 từ họp thường gặp soạn trước",
        priority="TB",
        metric_keys=["keyword_recognition"],
        value_fn=lambda r: fmt_pct(r["keyword_recognition"]),
        status_fn=lambda r: _gt(0.80)(r, "keyword_recognition"),
    ),
    # ---------------- Nhom 2 ----------------
    Criterion(
        id="2.1",
        group=2,
        group_name=GROUP_2,
        name="DER tổng",
        threshold_text="< 22%",
        method_text="pyannote.metrics DiarizationErrorRate(ref_rttm, hyp_rttm)",
        priority="Rất cao",
        metric_keys=["der"],
        value_fn=lambda r: fmt_pct(r["der"]),
        status_fn=lambda r: _lt(0.22)(r, "der"),
    ),
    Criterion(
        id="2.2",
        group=2,
        group_name=GROUP_2,
        name="Speaker confusion",
        threshold_text="< 12%",
        method_text="Thành phần confusion của DER",
        priority="Rất cao",
        metric_keys=["speaker_confusion"],
        value_fn=lambda r: fmt_pct(r["speaker_confusion"]),
        status_fn=lambda r: _lt(0.12)(r, "speaker_confusion"),
    ),
    Criterion(
        id="2.3",
        group=2,
        group_name=GROUP_2,
        name="Sai số số người nói",
        threshold_text="|Δ| ≤ 1",
        method_text="|num_detected - num_true|",
        priority="Cao",
        metric_keys=["speaker_count_diff"],
        value_fn=lambda r: fmt_num(r["speaker_count_diff"]),
        status_fn=lambda r: _le_abs(1)(r, "speaker_count_diff"),
    ),
    Criterion(
        id="2.4",
        group=2,
        group_name=GROUP_2,
        name="P/R biên giới lượt (±0.5s)",
        threshold_text="P > 0.80 / R > 0.75",
        method_text="So hyp_rttm với ref_rttm, dung sai 0.5s",
        priority="Cao",
        metric_keys=["boundary_precision", "boundary_recall"],
        value_fn=lambda r: f"P={r['boundary_precision']*100:.1f}% / R={r['boundary_recall']*100:.1f}%",
        status_fn=lambda r: PASS if (r["boundary_precision"] > 0.80 and r["boundary_recall"] > 0.75) else FAIL,
    ),
    Criterion(
        id="2.5",
        group=2,
        group_name=GROUP_2,
        name="RTF diarization (CPU)",
        threshold_text="< 1.5",
        method_text="thời gian xử lý diart / thời lượng audio",
        priority="Cao",
        metric_keys=["rtf_diarization"],
        value_fn=lambda r: fmt_num(r["rtf_diarization"]),
        status_fn=lambda r: _lt(1.5)(r, "rtf_diarization"),
    ),
    Criterion(
        id="2.6",
        group=2,
        group_name=GROUP_2,
        name="So sánh preset (A/B)",
        threshold_text="chọn min DER",
        method_text="Lặp DIART_PRESET ∈ {ami, voxconverse, dihard}; cần chạy nhiều lần",
        priority="TB",
        metric_keys=[],
        value_fn=lambda r: NA,
        status_fn=lambda r: MANUAL,
    ),
    # ---------------- Nhom 3 ----------------
    Criterion(
        id="3.1",
        group=3,
        group_name=GROUP_3,
        name="TER - tỉ lệ lượt gán sai người",
        threshold_text="< 15%",
        method_text="Khớp lượt hyp↔ref theo thời gian, đếm % sai nhãn speaker",
        priority="Rất cao",
        metric_keys=["ter"],
        value_fn=lambda r: fmt_pct(r["ter"]),
        status_fn=lambda r: _lt(0.15)(r, "ter"),
    ),
    Criterion(
        id="3.2",
        group=3,
        group_name=GROUP_3,
        name="Độ chính xác biên lượt STT",
        threshold_text="< 0.5s lệch TB",
        method_text="So start/end lượt STT với mốc tiếng nói thật",
        priority="TB",
        metric_keys=["turn_boundary_deviation"],
        value_fn=lambda r: fmt_num(r["turn_boundary_deviation"], "s"),
        status_fn=lambda r: _lt(0.5)(r, "turn_boundary_deviation"),
    ),
    Criterion(
        id="3.3",
        group=3,
        group_name=GROUP_3,
        name="Nhất quán đánh số người nói",
        threshold_text="100%",
        method_text="Cùng 1 người → cùng 'Người nói N' suốt phiên (first-appearance)",
        priority="Cao",
        metric_keys=["speaker_numbering_consistency"],
        value_fn=lambda r: fmt_pct(r["speaker_numbering_consistency"]),
        status_fn=lambda r: PASS if r["speaker_numbering_consistency"] >= 0.999 else FAIL,
    ),
    # ---------------- Nhom 4 ----------------
    Criterion(
        id="4.1",
        group=4,
        group_name=GROUP_4,
        name="WER toàn phiên (nội dung DOCX)",
        threshold_text="< 27%",
        method_text="So bản ghi tay toàn phiên với text trong DOCX",
        priority="Rất cao",
        metric_keys=["wer"],
        value_fn=lambda r: fmt_pct(r["wer"]),
        status_fn=lambda r: _lt(0.27)(r, "wer"),
    ),
    Criterion(
        id="4.2",
        group=4,
        group_name=GROUP_4,
        name="TER trong DOCX",
        threshold_text="< 15%",
        method_text="Đối chiếu nhãn người nói trong DOCX với nhãn chuẩn",
        priority="Rất cao",
        metric_keys=["ter"],
        value_fn=lambda r: fmt_pct(r["ter"]),
        status_fn=lambda r: _lt(0.15)(r, "ter"),
    ),
    Criterion(
        id="4.3",
        group=4,
        group_name=GROUP_4,
        name="RTF end-to-end (warm)",
        threshold_text="< 1.5",
        method_text="Từ bắt đầu xử lý đến xuất DOCX / thời lượng audio",
        priority="Rất cao",
        metric_keys=["rtf_e2e"],
        value_fn=lambda r: fmt_num(r["rtf_e2e"]),
        status_fn=lambda r: _lt(1.5)(r, "rtf_e2e"),
    ),
    Criterion(
        id="4.4",
        group=4,
        group_name=GROUP_4,
        name="Ổn định phiên dài > 2h",
        threshold_text="Không crash, RAM ổn định",
        method_text="5 file x 30 phút cùng 1 session; theo dõi RAM",
        priority="Rất cao",
        metric_keys=[],
        value_fn=lambda r: NA,
        status_fn=lambda r: MANUAL,
    ),
    Criterion(
        id="4.5",
        group=4,
        group_name=GROUP_4,
        name="Chất lượng tóm tắt (Qwen)",
        threshold_text="Đạt theo rubric / ROUGE-L cao",
        method_text="Chấm người hoặc ROUGE-L với bản tóm tắt mẫu",
        priority="TB",
        metric_keys=["rouge_l"],
        value_fn=lambda r: fmt_pct(r["rouge_l"]),
        status_fn=lambda r: MANUAL if r.get("rouge_l") is None else (PASS if r["rouge_l"] >= 0.4 else FAIL),
    ),
    # ---------------- Nhom 5 ----------------
    Criterion(
        id="5.1",
        group=5,
        group_name=GROUP_5,
        name="RTF STT (lane 1)",
        threshold_text="< 1.0",
        method_text="time.perf_counter quanh vòng decode",
        priority="Rất cao",
        metric_keys=["rtf_stt"],
        value_fn=lambda r: fmt_num(r["rtf_stt"]),
        status_fn=lambda r: _lt(1.0)(r, "rtf_stt"),
    ),
    Criterion(
        id="5.2",
        group=5,
        group_name=GROUP_5,
        name="RTF diart (lane 2)",
        threshold_text="< 1.5",
        method_text="Đo riêng thread feeder; theo dõi backlog drain",
        priority="Cao",
        metric_keys=["rtf_diarization"],
        value_fn=lambda r: fmt_num(r["rtf_diarization"]),
        status_fn=lambda r: _lt(1.5)(r, "rtf_diarization"),
    ),
    Criterion(
        id="5.3",
        group=5,
        group_name=GROUP_5,
        name="Thời gian hoàn thiện",
        threshold_text="< 0.3x audio",
        method_text="drain + gán overlap + khôi phục dấu câu",
        priority="Cao",
        metric_keys=["finalize_ratio"],
        value_fn=lambda r: fmt_num(r["finalize_ratio"]),
        status_fn=lambda r: _lt(0.3)(r, "finalize_ratio"),
    ),
    Criterion(
        id="5.4",
        group=5,
        group_name=GROUP_5,
        name="Thời gian tóm tắt (Qwen NPU)",
        threshold_text="< 60s / phiên",
        method_text="Đo wall-clock gọi Nexa",
        priority="TB",
        metric_keys=["summary_time"],
        value_fn=lambda r: fmt_num(r["summary_time"], "s"),
        status_fn=lambda r: _lt(60)(r, "summary_time"),
    ),
    Criterion(
        id="5.5",
        group=5,
        group_name=GROUP_5,
        name="Xuất DOCX",
        threshold_text="< 5s",
        method_text="Đo wall-clock export",
        priority="TB",
        metric_keys=["docx_export_time"],
        value_fn=lambda r: fmt_num(r["docx_export_time"], "s"),
        status_fn=lambda r: _lt(5)(r, "docx_export_time"),
    ),
]


def evaluate_all(results: dict) -> list[dict]:
    return [c.evaluate(results) for c in CRITERIA]
