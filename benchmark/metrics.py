"""Metric computations for the Smart Meeting benchmark suite.

Implements the measurement methods described in
Benchmarking_SmartMeeting.docx (section VI - PHUONG PHAP DO):
  - WER / CER via jiwer
  - DER / speaker confusion / speaker count diff / boundary P&R via pyannote.metrics
  - TER (turn-level speaker assignment error) and turn boundary deviation
  - Speaker numbering consistency
  - RTF (real-time factor) helpers
  - ROUGE-L for summary quality
"""

from __future__ import annotations

import io
import wave
from collections import defaultdict

import jiwer
from pyannote.core import Annotation, Segment
from pyannote.metrics.diarization import DiarizationErrorRate
from pyannote.metrics.segmentation import SegmentationPrecision, SegmentationRecall
from rouge_score import rouge_scorer

from benchmark.parsers import Segment as TSegment

_TEXT_TRANSFORM = jiwer.Compose(
    [
        jiwer.ToLowerCase(),
        jiwer.RemovePunctuation(),
        jiwer.RemoveMultipleSpaces(),
        jiwer.Strip(),
        jiwer.RemoveEmptyStrings(),
        jiwer.ReduceToListOfListOfWords(),
    ]
)

_CHAR_TRANSFORM = jiwer.Compose(
    [
        jiwer.ToLowerCase(),
        jiwer.RemovePunctuation(),
        jiwer.RemoveMultipleSpaces(),
        jiwer.Strip(),
        jiwer.RemoveEmptyStrings(),
        jiwer.ReduceToListOfListOfChars(),
    ]
)


def compute_wer(reference_text: str, hypothesis_text: str) -> float:
    """Word Error Rate (jiwer.wer), with lowercasing/punctuation normalization."""
    return jiwer.wer(
        reference_text,
        hypothesis_text,
        reference_transform=_TEXT_TRANSFORM,
        hypothesis_transform=_TEXT_TRANSFORM,
    )


def compute_cer(reference_text: str, hypothesis_text: str) -> float:
    """Character Error Rate (jiwer.cer), with lowercasing/punctuation normalization."""
    return jiwer.cer(
        reference_text,
        hypothesis_text,
        reference_transform=_CHAR_TRANSFORM,
        hypothesis_transform=_CHAR_TRANSFORM,
    )


def segments_to_annotation(segments: list[TSegment]) -> Annotation:
    """Build a pyannote Annotation (for diarization metrics) from parsed segments."""
    annotation = Annotation()
    for seg in segments:
        if seg.end > seg.start:
            annotation[Segment(seg.start, seg.end)] = seg.speaker
    return annotation


def compute_diarization_metrics(
    ref_segments: list[TSegment],
    hyp_segments: list[TSegment],
    boundary_tolerance: float = 0.5,
) -> dict:
    """Compute DER, speaker confusion, speaker-count diff and boundary P/R.

    Mirrors criteria 2.1-2.4 in Benchmarking_SmartMeeting.docx.
    """
    ref = segments_to_annotation(ref_segments)
    hyp = segments_to_annotation(hyp_segments)

    der_metric = DiarizationErrorRate()
    der = der_metric(ref, hyp)
    components = der_metric.compute_components(ref, hyp)
    total = components["total"] or 1.0

    ref_speakers = {seg.speaker for seg in ref_segments}
    hyp_speakers = {seg.speaker for seg in hyp_segments}

    precision = SegmentationPrecision(tolerance=boundary_tolerance)(ref, hyp)
    recall = SegmentationRecall(tolerance=boundary_tolerance)(ref, hyp)

    return {
        "der": der,
        "speaker_confusion": components["confusion"] / total,
        "missed_detection": components["missed detection"] / total,
        "false_alarm": components["false alarm"] / total,
        "ref_speaker_count": len(ref_speakers),
        "hyp_speaker_count": len(hyp_speakers),
        "speaker_count_diff": abs(len(ref_speakers) - len(hyp_speakers)),
        "boundary_precision": precision,
        "boundary_recall": recall,
    }


def _overlap(seg_a: TSegment, seg_b: TSegment) -> float:
    return max(0.0, min(seg_a.end, seg_b.end) - max(seg_a.start, seg_b.start))


def compute_turn_metrics(ref_segments: list[TSegment], hyp_segments: list[TSegment]) -> dict:
    """Turn Error Rate (3.1), turn boundary deviation (3.2) and speaker-numbering
    consistency (3.3).

    For each reference turn, the dominant overlapping hypothesis speaker is
    found and translated into reference-label space using the optimal
    DER mapping. A turn is an "error" if the mapped hypothesis speaker
    does not match the reference speaker for that turn (or if there is no
    overlapping hypothesis speech at all).
    """
    if not ref_segments:
        return {
            "ter": None,
            "turn_boundary_deviation": None,
            "speaker_numbering_consistency": None,
        }

    ref = segments_to_annotation(ref_segments)
    hyp = segments_to_annotation(hyp_segments)
    der_metric = DiarizationErrorRate()
    # mapping: hypothesis label -> reference label
    mapping = der_metric.optimal_mapping(ref, hyp) if hyp_segments else {}

    errors = 0
    boundary_deviations: list[float] = []

    for ref_seg in ref_segments:
        overlap_by_speaker: dict[str, float] = defaultdict(float)
        best_hyp_seg = None
        best_overlap = 0.0
        for hyp_seg in hyp_segments:
            ov = _overlap(ref_seg, hyp_seg)
            if ov > 0:
                overlap_by_speaker[hyp_seg.speaker] += ov
                if ov > best_overlap:
                    best_overlap = ov
                    best_hyp_seg = hyp_seg

        if not overlap_by_speaker:
            errors += 1
            continue

        dominant_hyp_speaker = max(overlap_by_speaker, key=overlap_by_speaker.get)
        mapped_speaker = mapping.get(dominant_hyp_speaker, dominant_hyp_speaker)
        if mapped_speaker != ref_seg.speaker:
            errors += 1

        if best_hyp_seg is not None:
            boundary_deviations.append(abs(best_hyp_seg.start - ref_seg.start))
            boundary_deviations.append(abs(best_hyp_seg.end - ref_seg.end))

    ter = errors / len(ref_segments)
    avg_deviation = (
        sum(boundary_deviations) / len(boundary_deviations) if boundary_deviations else None
    )

    # Speaker-numbering consistency: for each hypothesis speaker label, what
    # fraction of its total speaking time falls within its single dominant
    # reference speaker (i.e. it is never reused for a different person).
    hyp_total = defaultdict(float)
    hyp_overlap = defaultdict(lambda: defaultdict(float))
    for hyp_seg in hyp_segments:
        hyp_total[hyp_seg.speaker] += hyp_seg.end - hyp_seg.start
        for ref_seg in ref_segments:
            ov = _overlap(ref_seg, hyp_seg)
            if ov > 0:
                hyp_overlap[hyp_seg.speaker][ref_seg.speaker] += ov

    total_hyp_time = sum(hyp_total.values())
    if total_hyp_time > 0:
        consistent_time = sum(
            max(hyp_overlap[spk].values()) if hyp_overlap[spk] else 0.0
            for spk in hyp_total
        )
        consistency = consistent_time / total_hyp_time
    else:
        consistency = None

    return {
        "ter": ter,
        "turn_boundary_deviation": avg_deviation,
        "speaker_numbering_consistency": consistency,
    }


def compute_keyword_recognition(reference_text: str, hypothesis_text: str, keywords: list[str]) -> dict:
    """Fraction of reference keywords that also appear in the hypothesis text (1.5)."""
    ref_norm = reference_text.lower()
    hyp_norm = hypothesis_text.lower()

    present_in_ref = [kw for kw in keywords if kw.strip() and kw.strip().lower() in ref_norm]
    if not present_in_ref:
        return {"keyword_recognition": None, "keywords_in_ref": 0, "keywords_matched": 0}

    matched = [kw for kw in present_in_ref if kw.strip().lower() in hyp_norm]
    return {
        "keyword_recognition": len(matched) / len(present_in_ref),
        "keywords_in_ref": len(present_in_ref),
        "keywords_matched": len(matched),
    }


def compute_rouge_l(reference_summary: str, hypothesis_summary: str) -> float:
    """ROUGE-L F-measure between reference and generated summaries (4.5)."""
    scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=False)
    scores = scorer.score(reference_summary, hypothesis_summary)
    return scores["rougeL"].fmeasure


def get_audio_duration_seconds(audio_bytes: bytes) -> float | None:
    """Read a WAV file's duration in seconds. Returns None if it cannot be parsed."""
    try:
        with wave.open(io.BytesIO(audio_bytes), "rb") as wav_file:
            frames = wav_file.getnframes()
            rate = wav_file.getframerate()
            if rate == 0:
                return None
            return frames / float(rate)
    except (wave.Error, EOFError):
        return None


def compute_rtf(processing_time_seconds: float, audio_duration_seconds: float) -> float | None:
    """Real-Time Factor = processing time / audio duration."""
    if audio_duration_seconds is None or audio_duration_seconds <= 0:
        return None
    return processing_time_seconds / audio_duration_seconds
