#!/usr/bin/env python3
"""Automated verification suite for informs-review-loop skill."""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TESTS_DIR = Path(__file__).resolve().parent
SKILL_DIR = TESTS_DIR.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"

sys.path.insert(0, str(SCRIPTS_DIR))

import evaluate_review_round as ev  # noqa: E402


def _write_review(
    round_dir: Path,
    filename: str,
    *,
    reviewer: str,
    model: str,
    round_num: int,
    decision: str,
    confidence: str = "High",
) -> None:
    round_dir.mkdir(parents=True, exist_ok=True)
    content = (
        f"---\n"
        f"reviewer: {reviewer}\n"
        f"model: {model}\n"
        f"journal: opre\n"
        f"round: {round_num}\n"
        f"decision: {decision}\n"
        f"confidence: {confidence}\n"
        f"---\n\n"
        f"## Overall Assessment & Verdict Rationale\n"
        f"Sample blind review verdict: {decision}.\n"
    )
    (round_dir / filename).write_text(content, encoding="utf-8")


class TestReviewLoopEvaluator(unittest.TestCase):
    def test_decision_normalization(self) -> None:
        self.assertEqual(ev.normalize_decision("Desk Reject"), ("Desk Reject", 0))
        self.assertEqual(ev.normalize_decision("Reject"), ("Reject", 1))
        self.assertEqual(ev.normalize_decision("Reject & Resubmit"), ("Reject & Resubmit", 2))
        self.assertEqual(ev.normalize_decision("Reject and Resubmit"), ("Reject & Resubmit", 2))
        self.assertEqual(ev.normalize_decision("Major Revision"), ("Major Revision", 3))
        self.assertEqual(ev.normalize_decision("Minor Revision"), ("Minor Revision", 4))
        self.assertEqual(ev.normalize_decision("Accept with Minor Revisions"), ("Minor Revision", 4))
        self.assertEqual(ev.normalize_decision("Accept"), ("Accept", 5))
        self.assertIsNone(ev.normalize_decision("Unclear"))

    def test_stopping_criterion_exact_semantics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "review_loop"

            # Round 1: Reject & Resubmit + Major + Minor -> CONTINUE (not all >= Major)
            r1 = root / "round_01"
            _write_review(r1, "rev1_claude_opus.md", reviewer="rev1", model="claude-opus-5-5-high", round_num=1, decision="Reject & Resubmit")
            _write_review(r1, "rev2_gemini_neon.md", reviewer="rev2", model="gemini-4-neon-xhigh", round_num=1, decision="Major Revision")
            _write_review(r1, "rev3_gpt.md", reviewer="rev3", model="gpt-oss-120b-medium", round_num=1, decision="Minor Revision")
            (r1 / "triage_plan.md").write_text("# ignored meta file\n", encoding="utf-8")

            p1 = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "evaluate_review_round.py"), str(root), "--round", "1"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(p1.returncode, 10, p1.stdout + p1.stderr)
            self.assertIn("CONTINUE", p1.stdout)

            # Round 2: All Major Revision (zero Minor) -> CONTINUE (need >= 1 Minor Revision)
            r2 = root / "round_02"
            _write_review(r2, "rev1_claude_opus.md", reviewer="rev1", model="claude-opus-5-5-high", round_num=2, decision="Major Revision")
            _write_review(r2, "rev2_gemini_neon.md", reviewer="rev2", model="gemini-4-neon-xhigh", round_num=2, decision="Major Revision")
            _write_review(r2, "rev3_gpt.md", reviewer="rev3", model="gpt-oss-120b-medium", round_num=2, decision="Major Revision")

            p2 = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "evaluate_review_round.py"), str(root), "--round", "2"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(p2.returncode, 10, p2.stdout + p2.stderr)
            self.assertIn("no reviewer reached Minor Revision", p2.stdout)

            # Round 3: Same all Major Revision -> PLATEAU_WARNING emitted
            r3 = root / "round_03"
            _write_review(r3, "rev1_claude_opus.md", reviewer="rev1", model="claude-opus-5-5-high", round_num=3, decision="Major Revision")
            _write_review(r3, "rev2_gemini_neon.md", reviewer="rev2", model="gemini-4-neon-xhigh", round_num=3, decision="Major Revision")
            _write_review(r3, "rev3_gpt.md", reviewer="rev3", model="gpt-oss-120b-medium", round_num=3, decision="Major Revision")

            p3 = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "evaluate_review_round.py"), str(root), "--round", "3"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(p3.returncode, 10, p3.stdout + p3.stderr)
            self.assertIn("PLATEAU_WARNING", p3.stdout)

            # Round 4: Three Major + One Minor across 4 distinct models -> CONVERGED (exit 0)!
            r4 = root / "round_04"
            _write_review(r4, "rev1_claude_opus.md", reviewer="rev1", model="claude-opus-5-5-high", round_num=4, decision="Major Revision")
            _write_review(r4, "rev2_gemini_neon.md", reviewer="rev2", model="gemini-4-neon-xhigh", round_num=4, decision="Major Revision")
            _write_review(r4, "rev3_gpt.md", reviewer="rev3", model="gpt-oss-120b-medium", round_num=4, decision="Minor Revision")
            _write_review(r4, "rev4_claude_sonnet.md", reviewer="rev4", model="claude-sonnet-5-5-high", round_num=4, decision="Major Revision")

            p4 = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "evaluate_review_round.py"), str(root), "--round", "4"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(p4.returncode, 0, p4.stdout + p4.stderr)
            self.assertIn("CONVERGED", p4.stdout)

            sb_text = (root / "scoreboard.md").read_text(encoding="utf-8")
            self.assertIn("Round 1", sb_text)
            self.assertIn("Round 4", sb_text)
            self.assertIn("CONVERGED", sb_text)

    def test_invalid_decision_exits_2(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "review_loop"
            r1 = root / "round_01"
            _write_review(r1, "rev1.md", reviewer="rev1", model="claude", round_num=1, decision="Looks pretty good")
            _write_review(r1, "rev2.md", reviewer="rev2", model="gemini", round_num=1, decision="Major Revision")
            p = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "evaluate_review_round.py"), str(root), "--round", "1"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(p.returncode, 2)


class TestSkillHygiene(unittest.TestCase):
    def test_relative_links_exist(self) -> None:
        link_re = re.compile(r"\]\((\.\.?/[^)#\s]+)")
        md_files = [SKILL_DIR / "SKILL.md"] + sorted((SKILL_DIR / "references").glob("*.md"))
        for md_path in md_files:
            text = md_path.read_text(encoding="utf-8")
            for rel in link_re.findall(text):
                target = (md_path.parent / rel).resolve()
                self.assertTrue(target.exists(), f"Broken link {rel} inside {md_path}")

    def test_zero_cjk_inside_skill(self) -> None:
        cjk_re = re.compile(r"[\u4e00-\u9fff]")
        for ext in ("*.md", "*.py"):
            for fp in SKILL_DIR.rglob(ext):
                txt = fp.read_text(encoding="utf-8", errors="replace")
                m = cjk_re.search(txt)
                self.assertIsNone(m, f"CJK char found in {fp}: {m.group(0) if m else ''}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
