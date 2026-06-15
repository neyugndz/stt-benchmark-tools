"""QA + repair tools for LLM-generated ground-truth transcripts.

Two checks/fixes, both deterministic (no LLM involved):

1. Word-rate sanity check
   ---------------------------------------------------------------
   Verbatim Vietnamese speech runs at roughly 2.5-4.5 words/sec.
   If a ground-truth file's overall words/sec falls well outside that
   band, it is very likely the model SUMMARIZED/paraphrased instead of
   transcribing verbatim (too low) or duplicated/garbled content (too
   high).

2. RTTM-based speaker relabeling
   ---------------------------------------------------------------
   LLM transcription prompts ask the model to both (a) transcribe and
   (b) invent+remember a consistent "Nguoi noi N" numbering across the
   whole session. (b) drifts on long files: a speaker who returns after
   a long gap can get assigned a new/wrong number.

   If you have an RTTM file with STABLE, real speaker names (e.g. from
   pyannote diarization, which clusters over the whole recording and
   does not have this drift problem), this script re-derives the
   "Nguoi noi N" labels deterministically: each ground-truth segment is
   matched to the RTTM segment with the largest time overlap, and the
   RTTM speaker name is mapped to "Nguoi noi N" by first-appearance
   order (in time). This removes any drift the LLM introduced.

Usage:
    python scripts/groundtruth_qa.py wordrate <groundtruth.json> [...]
    python scripts/groundtruth_qa.py relabel <groundtruth.json> <rttm> <out.json>
    python scripts/groundtruth_qa.py diff <groundtruth.json> <rttm>
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

WPS_LOW = 2.2
WPS_HIGH = 5.0


def _parse_rttm_time(raw: str) -> float:
    """Parse a possibly thousands-dotted RTTM timestamp, e.g. '1.010.000' -> 1010.0.

    Standard RTTM timestamps have exactly 3 decimal digits (milliseconds).
    Some exports insert '.' as a thousands separator (locale bug), giving
    multi-dot strings like '1.010.000'. Stripping all dots and dividing by
    1000 handles both the normal case ('16.000' -> 16.0) and the
    thousands-separator case ('1.010.000' -> 1010.0).
    """
    digits = raw.replace(".", "")
    return int(digits) / 1000.0


def parse_rttm(path: Path) -> list[tuple[float, float, str]]:
    segments = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or not line.startswith("SPEAKER"):
            continue
        parts = re.split(r"\s+", line)
        # SPEAKER <file> <chnl> <tbeg> <tdur> <NA> <NA> <name> <NA> <NA>
        tbeg = _parse_rttm_time(parts[3])
        tdur = _parse_rttm_time(parts[4])
        name = parts[7]
        segments.append((tbeg, tbeg + tdur, name))
    segments.sort(key=lambda s: s[0])
    return segments


def _overlap(a_start, a_end, b_start, b_end) -> float:
    return max(0.0, min(a_end, b_end) - max(a_start, b_start))


def wordrate_check(paths: list[Path]) -> None:
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        segments = data["segments"] if isinstance(data, dict) and "segments" in data else data
        total_words = sum(len(seg["text"].split()) for seg in segments)
        duration = max(seg["end"] for seg in segments) - min(seg["start"] for seg in segments)
        wps = total_words / duration if duration else 0.0
        flag = ""
        if wps < WPS_LOW:
            flag = "  <-- SUSPICIOUSLY LOW: likely summarized/paraphrased, not verbatim"
        elif wps > WPS_HIGH:
            flag = "  <-- SUSPICIOUSLY HIGH: possible duplication/garbled output"
        print(f"{path.name:50s} words={total_words:6d} dur={duration:7.1f}s  wps={wps:5.2f}{flag}")


def _match_rttm(segments: list[dict], rttm_segments: list[tuple[float, float, str]],
                name_to_label: dict[str, str] | None) -> list[str | None]:
    """Match each ground-truth segment to an RTTM speaker name.

    On an exact overlap tie between two RTTM candidates, prefer whichever
    candidate's mapped label matches the segment's CURRENT speaker label
    (gives Gemini the benefit of the doubt on ambiguous short
    interjections, instead of flipping them based on RTTM list order).
    """
    matched: list[str | None] = []
    for seg in segments:
        candidates: list[tuple[float, str]] = []
        for r_start, r_end, r_name in rttm_segments:
            ov = _overlap(seg["start"], seg["end"], r_start, r_end)
            if ov > 0:
                candidates.append((ov, r_name))
        if not candidates:
            matched.append(None)
            continue
        best_ov = max(ov for ov, _ in candidates)
        tied = [name for ov, name in candidates if ov == best_ov]
        if len(tied) > 1 and name_to_label is not None:
            for name in tied:
                if name_to_label.get(name) == seg["speaker"]:
                    matched.append(name)
                    break
            else:
                matched.append(tied[0])
        else:
            matched.append(tied[0])
    return matched


def _build_label_map(segments: list[dict], rttm_segments: list[tuple[float, float, str]]) -> dict[str, str]:
    # First pass (no tie-breaking info yet) just to get first-appearance order.
    matched_names = _match_rttm(segments, rttm_segments, None)
    name_to_label: dict[str, str] = {}
    next_n = 1
    for name in matched_names:
        if name is not None and name not in name_to_label:
            name_to_label[name] = f"Người nói {next_n}"
            next_n += 1
    return name_to_label


def relabel(json_path: Path, rttm_path: Path, out_path: Path) -> None:
    data = json.loads(json_path.read_text(encoding="utf-8"))
    segments = data["segments"] if isinstance(data, dict) and "segments" in data else data
    rttm_segments = parse_rttm(rttm_path)

    name_to_label = _build_label_map(segments, rttm_segments)
    matched_names = _match_rttm(segments, rttm_segments, name_to_label)

    changed = 0
    for seg, name in zip(segments, matched_names):
        new_label = name_to_label.get(name, seg["speaker"]) if name else seg["speaker"]
        if new_label != seg["speaker"]:
            changed += 1
        seg["speaker"] = new_label

    out_path.write_text(json.dumps(segments, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Relabeled {json_path.name}: {changed}/{len(segments)} segments changed.")
    print("RTTM name -> label mapping:")
    for name, label in name_to_label.items():
        print(f"  {name:25s} -> {label}")
    print(f"Wrote {out_path}")


def diff(json_path: Path, rttm_path: Path) -> None:
    data = json.loads(json_path.read_text(encoding="utf-8"))
    segments = data["segments"] if isinstance(data, dict) and "segments" in data else data
    rttm_segments = parse_rttm(rttm_path)

    name_to_label = _build_label_map(segments, rttm_segments)
    matched_names = _match_rttm(segments, rttm_segments, name_to_label)

    print(f"{'start':>8} {'end':>8} {'rttm_name':25s} {'expected':12s} {'current':12s}")
    n_mismatch = 0
    for seg, name in zip(segments, matched_names):
        expected = name_to_label.get(name, "?") if name else "?"
        marker = ""
        if expected != seg["speaker"]:
            marker = "  <-- MISMATCH"
            n_mismatch += 1
        print(f"{seg['start']:8.1f} {seg['end']:8.1f} {name or '?':25s} {expected:12s} {seg['speaker']:12s}{marker}")
    print(f"\n{n_mismatch} mismatches out of {len(segments)} segments")


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        return
    cmd = sys.argv[1]
    if cmd == "wordrate":
        wordrate_check([Path(p) for p in sys.argv[2:]])
    elif cmd == "relabel":
        relabel(Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]))
    elif cmd == "diff":
        diff(Path(sys.argv[2]), Path(sys.argv[3]))
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
