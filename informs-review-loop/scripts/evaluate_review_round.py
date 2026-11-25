#!/usr/bin/env python3
"""Evaluate a multi-model blind peer-review round and enforce the stopping criterion.

Stopping criterion (CONVERGED -> exit 0):
  1. At least `--min-reviewers` (default 2; recommended 3+) valid reviews exist.
  2. EVERY reviewer rates `>= Major Revision` (rank >= 3; zero Desk Reject / Reject / R&R).
  3. AT LEAST ONE reviewer rates `>= Minor Revision` (rank >= 4; Minor Revision or Accept).

Exit codes:
  0  - CONVERGED (stop loop and deliver final report)
  10 - CONTINUE  (not yet converged; proceed to triage & revision unless max rounds / plateau)
  2  - INVALID   (missing round folder, too few reviews, or unparseable decision)
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


META_FILENAMES = {
    "triage_plan.md",
    "summary.md",
    "scoreboard.md",
    "deferred_rr_backlog.md",
    "notes.md",
    "readme.md",
}


class ReviewVerdict(NamedTuple):
    file_name: str
    reviewer: str
    role: str
    model: str
    journal: str
    round_num: int
    decision: str
    rank: int
    confidence: str


def normalize_decision(raw: str) -> tuple[str, int] | None:
    """Map raw reviewer decision strings to canonical (label, rank)."""
    cleaned = re.sub(r"[*_`\"']", "", raw).strip()
    low = re.sub(r"\s+", " ", cleaned.lower())
    if not low:
        return None
    if "desk" in low and "reject" in low:
        return ("Desk Reject", 0)
    if (
        ("reject" in low and "resubmit" in low)
        or ("revise" in low and "resubmit" in low)
        or low in {"r&r", "r & r", "rr"}
    ):
        return ("Reject & Resubmit", 2)
    if re.search(r"\breject\b", low):
        return ("Reject", 1)
    if "major" in low:
        return ("Major Revision", 3)
    if "minor" in low:
        return ("Minor Revision", 4)
    if "accept" in low:
        return ("Accept", 5)
    return None


def parse_review_file(path: Path, default_round: int) -> ReviewVerdict:
    text = path.read_text(encoding="utf-8", errors="replace")
    meta: dict[str, str] = {}

    fm_match = re.match(r"^\s*---\s*\n(.*?)\n---\s*(?:\n|$)", text, flags=re.DOTALL)
    header_block = fm_match.group(1) if fm_match else "\n".join(text.splitlines()[:25])
    for line in header_block.splitlines():
        m = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.+?)\s*$", line)
        if m:
            meta[m.group(1).strip().lower()] = m.group(2).strip().strip("\"'")

    raw_decision = meta.get("decision") or meta.get("verdict") or meta.get("recommendation") or ""
    norm = normalize_decision(raw_decision)
    if norm is None:
        raise ValueError(
            f"Unparseable or missing decision in {path.name} (got {raw_decision!r}); "
            "expected Desk Reject | Reject | Reject & Resubmit | Major Revision | Minor Revision | Accept."
        )
    decision_label, rank = norm

    round_str = meta.get("round", "")
    round_num = int(round_str) if round_str.isdigit() else default_round

    return ReviewVerdict(
        file_name=path.name,
        reviewer=meta.get("reviewer") or path.stem,
        role=meta.get("role") or "Reviewer",
        model=meta.get("model") or "unknown",
        journal=meta.get("journal") or "unknown",
        round_num=round_num,
        decision=decision_label,
        rank=rank,
        confidence=meta.get("confidence") or "Medium",
    )


def find_round_dir(review_loop_dir: Path, round_num: int) -> Path | None:
    for candidate in (
        review_loop_dir / f"round_{round_num:02d}",
        review_loop_dir / f"round_{round_num}",
    ):
        if candidate.is_dir():
            return candidate
    return None


def load_round_verdicts(round_dir: Path, round_num: int) -> list[ReviewVerdict]:
    verdicts: list[ReviewVerdict] = []
    for md_path in sorted(round_dir.glob("*.md")):
        if md_path.name.lower() in META_FILENAMES:
            continue
        verdicts.append(parse_review_file(md_path, default_round=round_num))
    return verdicts


def evaluate_convergence(
    verdicts: list[ReviewVerdict], *, min_reviewers: int = 2
) -> tuple[bool, str]:
    if len(verdicts) < min_reviewers:
        return (
            False,
            f"Insufficient reviews: found {len(verdicts)}, need at least {min_reviewers}.",
        )
    all_major_plus = all(v.rank >= 3 for v in verdicts)
    any_minor_plus = any(v.rank >= 4 for v in verdicts)
    if all_major_plus and any_minor_plus:
        return (
            True,
            "CONVERGED: every reviewer rated >= Major Revision AND at least one rated >= Minor Revision.",
        )
    reasons: list[str] = []
    below_major = [f"{v.reviewer}={v.decision}" for v in verdicts if v.rank < 3]
    if below_major:
        reasons.append(f"below Major Revision: {', '.join(below_major)}")
    if not any_minor_plus:
        reasons.append("no reviewer reached Minor Revision or Accept yet")
    return False, "CONTINUE: " + "; ".join(reasons) + "."


def discover_all_rounds(review_loop_dir: Path) -> list[tuple[int, Path]]:
    found: dict[int, Path] = {}
    if not review_loop_dir.is_dir():
        return []
    for child in sorted(review_loop_dir.iterdir()):
        if not child.is_dir():
            continue
        m = re.fullmatch(r"round_(\d+)", child.name)
        if m:
            found[int(m.group(1))] = child
    return sorted(found.items(), key=lambda item: item[0])


def detect_plateau(
    review_loop_dir: Path, current_round: int, current_verdicts: list[ReviewVerdict]
) -> bool:
    """Return True if current round did not improve over previous round's verdict distribution."""
    if current_round <= 1 or not current_verdicts:
        return False
    prev_dir = find_round_dir(review_loop_dir, current_round - 1)
    if prev_dir is None:
        return False
    try:
        prev_verdicts = load_round_verdicts(prev_dir, current_round - 1)
    except ValueError:
        return False
    if not prev_verdicts:
        return False
    prev_min = min(v.rank for v in prev_verdicts)
    prev_max = max(v.rank for v in prev_verdicts)
    prev_avg = sum(v.rank for v in prev_verdicts) / len(prev_verdicts)
    cur_min = min(v.rank for v in current_verdicts)
    cur_max = max(v.rank for v in current_verdicts)
    cur_avg = sum(v.rank for v in current_verdicts) / len(current_verdicts)
    return (cur_min <= prev_min) and (cur_max <= prev_max) and (cur_avg <= prev_avg)


def write_scoreboard(review_loop_dir: Path, min_reviewers: int = 2) -> Path:
    lines: list[str] = [
        "# Blind Peer-Review Rating Trajectory Scoreboard",
        "",
        "Target stopping criterion: **ALL reviewers >= Major Revision** AND **>= 1 reviewer >= Minor Revision**.",
        "",
    ]
    rounds = discover_all_rounds(review_loop_dir)
    summary_rows: list[str] = []

    for r_num, r_dir in rounds:
        try:
            verdicts = load_round_verdicts(r_dir, r_num)
        except ValueError as exc:
            lines.append(f"## Round {r_num} (PARSE ERROR: {exc})")
            lines.append("")
            continue
        if not verdicts:
            continue
        converged, status_msg = evaluate_convergence(verdicts, min_reviewers=min_reviewers)
        min_v = min(verdicts, key=lambda v: v.rank).decision
        max_v = max(verdicts, key=lambda v: v.rank).decision
        verdict_list = ", ".join(f"{v.reviewer}: {v.decision}" for v in verdicts)
        summary_rows.append(
            f"| Round {r_num} | {len(verdicts)} | {min_v} | {max_v} | {'CONVERGED' if converged else 'CONTINUE'} | {verdict_list} |"
        )

    if summary_rows:
        lines.extend(
            [
                "## Round-by-Round Summary",
                "",
                "| Round | Reviewers | Lowest Verdict | Highest Verdict | Gate | Breakdown |",
                "| :--- | :---: | :--- | :--- | :---: | :--- |",
                *summary_rows,
                "",
            ]
        )

    for r_num, r_dir in rounds:
        try:
            verdicts = load_round_verdicts(r_dir, r_num)
        except ValueError:
            continue
        if not verdicts:
            continue
        converged, status_msg = evaluate_convergence(verdicts, min_reviewers=min_reviewers)
        lines.extend(
            [
                f"## Round {r_num} Details (`{'CONVERGED' if converged else 'CONTINUE'}`)",
                "",
                f"> {status_msg}",
                "",
                "| Reviewer | Role | Model | Decision | Rank (0-5) | Confidence | File |",
                "| :--- | :--- | :--- | :--- | :---: | :---: | :--- |",
            ]
        )
        for v in verdicts:
            lines.append(
                f"| `{v.reviewer}` | {v.role} | `{v.model}` | **{v.decision}** | {v.rank} | {v.confidence} | `{r_dir.name}/{v.file_name}` |"
            )
        lines.append("")

    out_path = review_loop_dir / "scoreboard.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Parse blind reviewer verdicts for a review-loop round and check stopping criterion."
    )
    parser.add_argument("review_loop_dir", type=Path, help="Path to review_loop/ directory")
    parser.add_argument("--round", dest="round_num", type=int, required=True, help="Round number (1-based)")
    parser.add_argument("--max-rounds", type=int, default=4, help="Safety ceiling for rounds (default: 4)")
    parser.add_argument("--min-reviewers", type=int, default=2, help="Minimum reviewers required (default: 2)")
    parser.add_argument("--no-scoreboard", action="store_true", help="Do not write scoreboard.md")
    args = parser.parse_args()

    round_dir = find_round_dir(args.review_loop_dir, args.round_num)
    if round_dir is None:
        print(
            f"ERROR: round directory not found for round {args.round_num} under {args.review_loop_dir}",
            file=sys.stderr,
        )
        return 2

    try:
        verdicts = load_round_verdicts(round_dir, args.round_num)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if len(verdicts) < args.min_reviewers:
        print(
            f"ERROR: found only {len(verdicts)} review(s) in {round_dir}; expected >= {args.min_reviewers}.",
            file=sys.stderr,
        )
        return 2

    distinct_models = {v.model for v in verdicts if v.model and v.model != "unknown"}
    converged, message = evaluate_convergence(verdicts, min_reviewers=args.min_reviewers)
    plateau = (not converged) and detect_plateau(args.review_loop_dir, args.round_num, verdicts)

    print(f"ROUND {args.round_num} EVALUATION ({round_dir.name}, {len(verdicts)} reviewers, {len(distinct_models)} distinct model(s)):")
    for v in verdicts:
        print(f"  - [{v.reviewer}] ({v.role} | {v.model}): {v.decision} (rank={v.rank}, confidence={v.confidence})")
    print(f"STATUS: {message}")
    if len(verdicts) < 3:
        print("NOTE: Panel has fewer than 3 reviewers; a 3-model panel is recommended for reliable convergence.")
    if plateau:
        print("PLATEAU_WARNING: Verdict distribution did not improve vs. previous round; review whether remaining blockers are P2 high-effort items needing user input.")
    if (not converged) and args.round_num >= args.max_rounds:
        print(f"MAX_ROUNDS_REACHED: Reached safety ceiling ({args.max_rounds} rounds); stop loop and present remaining P2/unresolved items to the user.")

    if not args.no_scoreboard:
        sb = write_scoreboard(args.review_loop_dir, min_reviewers=args.min_reviewers)
        print(f"SCOREBOARD: {sb}")

    return 0 if converged else 10


if __name__ == "__main__":
    raise SystemExit(main())
