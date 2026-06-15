"""Batch-run the Smart Meeting benchmark metrics across multiple
groundtruth/hypothesis transcript pairs (data_groundtruth / data_hypothesis).

Usage:
    python scripts/batch_eval.py
"""

from __future__ import annotations

import json
import sys
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from benchmark import metrics
from benchmark.parsers import parse_transcript, segments_to_text

BENCH_DIR = ROOT.parent
GT_DIR = BENCH_DIR / "data_groundtruth"
HYP_DIR = BENCH_DIR / "data_hypothesis"

PAIRS = [
    ("toadam1_bhyt", GT_DIR / "transcript_toadam1_bhyt_groundtruth.json",
     HYP_DIR / "toadam1_bhyt" / "transcript_toadam1_bhyt.txt",
     HYP_DIR / "toadam1_bhyt" / "timings.json", None),
    ("toadam2_gdpt", GT_DIR / "transcript_toadam2_gdpt_groundtruth.json",
     HYP_DIR / "toadam2_gdpt" / "transcript_toadam2_gdpt.txt",
     HYP_DIR / "toadam2_gdpt" / "timings.json", None),
    ("toadam3_quanlyvonmoi", GT_DIR / "transcript_toadam3_quanlyvonmoi_groundtruth.json",
     HYP_DIR / "toadam3_quanlyvonmoi" / "transcript_toadam3_quanlyvonmoi.txt",
     HYP_DIR / "toadam3_quanlyvonmoi" / "timings.json", None),
    ("toadam4_nongsanxuatkhau", GT_DIR / "transcript_toadam4_nongsanxuatkhau_groundtruth.fixed.json",
     HYP_DIR / "toadam4_nongsanxuatkhau" / "transcript_toadam4_nongsanxuatkhau.txt",
     HYP_DIR / "toadam4_nongsanxuatkhau" / "timings.json", None),
    ("toadam5_doingoaivn", GT_DIR / "transcript_toadam5_doingoaivn_groundtruth.json",
     HYP_DIR / "toadam5_doingoaivn" / "transcript_toadam5_doingoaivn.txt",
     HYP_DIR / "toadam5_doingoaivn" / "timings.json", None),
    ("toadam6_kinhte", GT_DIR / "transcript_toadam6_kinhte_groundtruth.json",
     HYP_DIR / "toadam6_kinhte" / "transcript_toadam6_kinhte.txt",
     HYP_DIR / "toadam6_kinhte" / "timings.json", None),
    ("toadam7_nongdocon", GT_DIR / "transcript_toadam7_nongdocon_groundtruth.json",
     HYP_DIR / "toadam7_nongdocon" / "transcript_toadam7_nongdocon.txt",
     HYP_DIR / "toadam7_nongdocon" / "timings.json", None),
    ("3p_meeting_zipformer", GT_DIR / "transcript_3p_meeting_groundtruth.json",
     HYP_DIR / "3p_meeting_demo" / "transcript_3p_meeting_zipformer.txt",
     HYP_DIR / "3p_meeting_demo" / "timings.json",
     HYP_DIR / "3p_meeting_demo" / "Audio_MEETING-20260605-1059.wav"),
]


def audio_duration(wav_path: Path | None, ref_segments) -> tuple[float, bool]:
    """Return (duration_seconds, is_real_audio)."""
    if wav_path and wav_path.exists():
        with wave.open(str(wav_path), "rb") as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            if rate:
                return frames / float(rate), True
    # fallback: max end time across reference segments (approximation)
    return max((s.end for s in ref_segments), default=0.0), False


def main() -> None:
    rows = []
    for name, gt_path, hyp_path, timings_path, wav_path in PAIRS:
        ref_segments = parse_transcript(gt_path.read_text(encoding="utf-8"))
        hyp_segments = parse_transcript(hyp_path.read_text(encoding="utf-8"))

        ref_text = segments_to_text(ref_segments)
        hyp_text = segments_to_text(hyp_segments)

        wer = metrics.compute_wer(ref_text, hyp_text)
        cer = metrics.compute_cer(ref_text, hyp_text)

        diar = metrics.compute_diarization_metrics(ref_segments, hyp_segments)
        turn = metrics.compute_turn_metrics(ref_segments, hyp_segments)

        timings = json.loads(timings_path.read_text(encoding="utf-8")) if timings_path.exists() else {}
        dur, is_real = audio_duration(wav_path, ref_segments)
        rtf_stt = metrics.compute_rtf(timings.get("stt", 0), dur) if dur else None
        rtf_diar = metrics.compute_rtf(timings.get("diarization", 0), dur) if dur else None

        rows.append({
            "file": name,
            "n_ref_turns": len(ref_segments),
            "n_hyp_turns": len(hyp_segments),
            "audio_dur_s": round(dur, 1),
            "dur_is_estimate": not is_real,
            "wer_%": round(wer * 100, 1),
            "cer_%": round(cer * 100, 1),
            "der_%": round(diar["der"] * 100, 1),
            "spk_confusion_%": round(diar["speaker_confusion"] * 100, 1),
            "ref_spk": diar["ref_speaker_count"],
            "hyp_spk": diar["hyp_speaker_count"],
            "spk_count_diff": diar["speaker_count_diff"],
            "boundary_P_%": round(diar["boundary_precision"] * 100, 1),
            "boundary_R_%": round(diar["boundary_recall"] * 100, 1),
            "ter_%": round(turn["ter"] * 100, 1) if turn["ter"] is not None else None,
            "spk_numbering_consistency_%": round(turn["speaker_numbering_consistency"] * 100, 1)
                if turn["speaker_numbering_consistency"] is not None else None,
            "rtf_stt": round(rtf_stt, 3) if rtf_stt is not None else None,
            "rtf_diar": round(rtf_diar, 3) if rtf_diar is not None else None,
            "stt_time_s": timings.get("stt"),
            "diar_time_s": timings.get("diarization"),
        })

    import pandas as pd
    df = pd.DataFrame(rows)
    pd.set_option("display.width", 250)
    print(df.to_string(index=False))
    df.to_csv(ROOT / "report" / "batch_eval_results.csv", index=False)
    print(f"\nSaved to {ROOT / 'report' / 'batch_eval_results.csv'}")


if __name__ == "__main__":
    main()
