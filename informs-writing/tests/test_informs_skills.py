#!/usr/bin/env python3
"""Automated verification suite for informs-writing and informs-zh-review skills."""
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
INFORMS_WRITING_DIR = TESTS_DIR.parent
SKILLS_ROOT = INFORMS_WRITING_DIR.parent
SCRIPTS_DIR = INFORMS_WRITING_DIR / "scripts"
ZH_REVIEW_DIR = SKILLS_ROOT / "informs-zh-review"

sys.path.insert(0, str(SCRIPTS_DIR))

import audit_informs_draft as aud  # noqa: E402
import audit_manuscript_contract as contract  # noqa: E402
import check_pdf_layout as pdf_qa  # noqa: E402
import check_prose_craft as craft  # noqa: E402


CLEAN_TEX_BASE = r"""
\documentclass[mnsc,nonblindrev]{informs4}
\begin{document}
\TITLE{Optimal Dispatch Under Supply Delays}
\ABSTRACT{We study dynamic dispatch when carriers face stochastic travel delays. Using a fluid-limit relaxation and priority coupling, we show that a threshold index rule reduces expected holding costs by roughly 2\% relative to a greedy FIFO baseline.}
\KEYWORDS{dispatching; supply delays; queueing control}
\SUBJECTCLASS{Queues: optimization}
\AREAOFREVIEW{Operations and Supply Chains}
\maketitle

\section{Introduction}\label{sec:intro}
Online freight marketplaces assign incoming orders to drivers under uncertain transit times. We introduce the threshold parameter $\tau$ early to balance holding cost $h$ against dispatch delay $\delta$.

\section{Model}\label{sec:model}
At each epoch, the planner observes backlog $q$ and selects threshold $\tau$ to minimize average cost $h q + \delta$. Equation~\eqref{eq:bellman} characterizes the value function across regimes (spanning 2019--2023).
\begin{equation}\label{eq:bellman}
V(q) = \min_{\tau \ge 0} \bigl\{ h q + \delta \tau \bigr\}.
\end{equation}
Unreferenced intermediate algebra is left unnumbered:
\begin{align*}
h q + \delta \tau \le 2 V(q).
\end{align*}

\begin{table}[t]
\centering
\caption{Main Benchmark Comparison}
\begin{tabular}{lcc}
\toprule
Policy & Cost & Gap (\%) \\
\midrule
FIFO & 12.43 & 2.18 \\
Threshold & 12.16 & 0.00 \\
\bottomrule
\end{tabular}
\end{table}

In Section 2.1, our estimates remain statistically significant ($p = 0.012$) across thresholds ($0.05$). Table~1 confirms the pattern described above.

\section{Conclusion}
Although our fluid model abstracts from multi-hop transshipment, future work can relax single-leg routing.

\ECSwitch
\ECHead{Online Appendix}
\section{Proofs}
Full derivations appear in Online Appendix EC.1.
\end{document}
"""


class TestInformsAudit(unittest.TestCase):
    def test_master_template_clean_mnsc_opre_ijoc(self) -> None:
        master = (INFORMS_WRITING_DIR / "templates" / "informs4-master.tex").read_text(
            encoding="utf-8"
        )
        for j in ("mnsc", "ijoc"):
            findings = aud.audit_manuscript(master, journal=j)
            errs = [f for f in findings if f.severity == "ERROR"]
            self.assertEqual(errs, [], f"Expected 0 ERRORs on master template for {j}, got {errs}")

        opre_master = master.replace("% \\SUBJECTCLASS", "\\SUBJECTCLASS").replace(
            "% \\AREAOFREVIEW", "\\AREAOFREVIEW"
        )
        errs_opre = [f for f in aud.audit_manuscript(opre_master, journal="opre") if f.severity == "ERROR"]
        self.assertEqual(errs_opre, [], f"Expected 0 ERRORs on OR-uncommented master template, got {errs_opre}")

    def test_clean_manuscript_and_carveouts(self) -> None:
        findings = aud.audit_manuscript(CLEAN_TEX_BASE, journal="mnsc")
        errs = [f for f in findings if f.severity == "ERROR"]
        self.assertEqual(errs, [], f"Expected 0 ERRORs on CLEAN_TEX_BASE, got {errs}")

    def test_disease_1_equation_hygiene_and_orphans(self) -> None:
        bad_eq = CLEAN_TEX_BASE.replace(
            r"\end{align*}",
            "\\end{align*}\n\\begin{equation}\\label{eq:unused}\nx = y + z.\n\\end{equation}\n\\begin{eqnarray}a &=& b\\end{eqnarray}",
        )
        cats = {f.category for f in aud.audit_manuscript(bad_eq) if f.severity == "ERROR"}
        self.assertIn("EquationHygiene", cats)

        orphan_tex = CLEAN_TEX_BASE.replace(
            r"\section{Model}\label{sec:model}",
            r"\section{Model}\label{sec:model} Consider $u_1 + v_2 + w_3 + r_4 + s_5 + z_6 + p_7$.",
        )
        cats2 = {f.category for f in aud.audit_manuscript(orphan_tex) if f.severity == "ERROR"}
        self.assertIn("OrphanNotation", cats2)

    def test_disease_2_cold_start_and_disease_6_definitions(self) -> None:
        cold = CLEAN_TEX_BASE.replace(
            r"\section{Model}\label{sec:model}" + "\n" + "At each epoch",
            "\\section{Model}\\label{sec:model}\n\\begin{definition}[Slack] Let $x>0$.\\end{definition}\nAt each epoch",
        )
        cats = {f.category for f in aud.audit_manuscript(cold)}
        self.assertIn("ColdStartBlock", cats)

        dup_defs = CLEAN_TEX_BASE.replace(
            r"\section{Conclusion}",
            "\\begin{definition}[Index] First.\\end{definition}\n"
            "\\begin{definition}[Index] Second.\\end{definition}\n"
            "\\begin{definition}[Extra] Third.\\end{definition}\n\\section{Conclusion}",
        )
        cats2 = {f.category for f in aud.audit_manuscript(dup_defs) if f.severity == "ERROR"}
        self.assertIn("DefinitionBloat", cats2)
        self.assertIn("DuplicateDefinition", cats2)

    def test_disease_3_4_5_7_hard_blocks(self) -> None:
        injected = CLEAN_TEX_BASE.replace(
            "Online freight marketplaces assign incoming orders to drivers under uncertain transit times.",
            "With the rapid development of e-commerce, we delve into this pivotal tapestry---not merely routing, but also dispatch, thereby enabling synergy. "
            "Moreover, X. Furthermore, Y. Additionally, Z. As a matter of fact, this improves profit by 1.32\\%. "
            "Although we establish optimality, this does not fully establish robustness. "
            "Unlike the previous version, I have fixed this issue.",
        )
        findings = aud.audit_manuscript(injected, journal="mnsc")
        err_cats = {f.category for f in findings if f.severity == "ERROR"}
        for expected in (
            "AICliche",
            "ParticipialTail",
            "TransitionGlue",
            "EmDash",
            "NegParallel",
            "Chinglish",
            "McCloskeyBloat",
            "DefensiveCaveat",
            "DecimalDump",
            "ContextLeakage",
        ):
            self.assertIn(expected, err_cats, f"Missing expected ERROR {expected}; got {err_cats}")

    def test_appendix_and_table_and_journal_rules(self) -> None:
        bad = CLEAN_TEX_BASE.replace(r"\ECSwitch", r"\appendix").replace(
            r"\begin{tabular}{lcc}", r"\begin{tabular}{|l|c|c|}" + "\n\\hline"
        )
        err_cats = {f.category for f in aud.audit_manuscript(bad, journal="msom") if f.severity == "ERROR"}
        self.assertIn("AppendixPolicy", err_cats)
        self.assertIn("TableHygiene", err_cats)
        self.assertIn("MSOM-Abstract", err_cats)

        msom_fn = CLEAN_TEX_BASE.replace("FIFO baseline", "FIFO\\footnote{Bad} baseline")
        err_msom = {f.category for f in aud.audit_manuscript(msom_fn, journal="msom") if f.severity == "ERROR"}
        self.assertIn("Journal-MSOM", err_msom)

        no_subj = CLEAN_TEX_BASE.replace(r"\SUBJECTCLASS{Queues: optimization}", "")
        err_opre = {f.category for f in aud.audit_manuscript(no_subj, journal="opre") if f.severity == "ERROR"}
        self.assertIn("Journal-OR", err_opre)

    def test_cli_exit_code_blocks_on_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bad_file = Path(tmp) / "bad.tex"
            bad_file.write_text(CLEAN_TEX_BASE.replace("delivers", "").replace("roughly 2\\%", "1.47%"), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "audit_informs_draft.py"), str(bad_file), "--journal", "mnsc"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
            proc_adv = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "audit_informs_draft.py"), str(bad_file), "--advisory"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc_adv.returncode, 0)

    def test_visual_layout_hazard_warnings(self) -> None:
        hazards = (
            CLEAN_TEX_BASE.replace(
                r"\begin{table}[t]",
                "\\vspace{-1em}\n\\begin{table}[H]",
            )
            .replace(r"\begin{tabular}{lcc}", "\\resizebox{\\textwidth}{!}{\\begin{tabular}{lcc}")
            .replace(r"\end{tabular}", "\\end{tabular}}")
        )
        warn_cats = {f.category for f in aud.audit_manuscript(hazards, journal="mnsc") if f.severity == "WARN"}
        self.assertIn("FloatPlacement", warn_cats)
        self.assertIn("TableScaling", warn_cats)
        self.assertIn("NegativeVspace", warn_cats)


class TestProseCraft(unittest.TestCase):
    def test_craft_rules(self) -> None:
        sample = (
            "Our empirical data proves that efficiency matters—wait. "
            "With the rapid development of the consumer and customer and buyer, the optimization capability implementation matters. "
            "This shows the effect of the design of the structure of the system. "
            "This suggests a rule. This reveals another point. "
            "There is a pattern. There is a pattern. There is a pattern. There is a pattern."
        )
        issues = craft.analyze_prose(sample, section="results")
        cats = {i.category for i in issues}
        for expected in (
            "EmDash",
            "EvidenceCalibration",
            "Chinglish",
            "SynonymDrift",
            "AbstractNounPile",
            "PrepositionChain",
            "NakedThis",
            "RepetitiveOpeners",
        ):
            self.assertIn(expected, cats, f"Expected {expected}, got {cats}")


class TestContractAuditor(unittest.TestCase):
    def test_contract_drift_and_unified_placement(self) -> None:
        bad_md = """
# Abstract
Our algorithm improves profit by 18% and always achieves optimality.

# Results
Regression estimates in our sample are consistent with a 12% profit gain under linear utility.

# Conclusion
Our study proves universal dominance across all settings.
See Online Appendix EC.2.
"""
        _inv, findings = contract.audit_contract(bad_md, journal="mnsc")
        cats = {f.category for f in findings}
        self.assertIn("ClaimEscalation", cats)
        self.assertIn("MissingComparator", cats)
        self.assertIn("MagnitudeDrift", cats)
        self.assertIn("EmptyECPointer", cats)

        bucket, note = contract.classify_result_item("Theorem 1: Threshold optimality", "opre")
        self.assertEqual(bucket, "MAIN_BODY")
        self.assertIn("Online Appendix EC.x", note)

        bucket_ec, note_ec = contract.classify_result_item("Robustness check with alternative clustering", "msom")
        self.assertEqual(bucket_ec, "ONLINE_APPENDIX_EC")
        self.assertNotIn("\\appendix", note_ec.lower())

        bucket_ijoc, _ = contract.classify_result_item("Benchmark instances and solver GitHub code", "ijoc")
        self.assertIn("COMPANION_REPO", bucket_ijoc)

    def test_word_count_parity_and_balance(self) -> None:
        sample_md = "# Abstract\n" + " ".join(["word"] * 90) + "\n\n# Introduction\n" + " ".join(["text"] * 900)
        _inv, findings = contract.audit_contract(
            sample_md,
            journal="mnsc",
            exemplar_abs_words=180,
            exemplar_intro_words=1500,
        )
        cats = {f.category for f in findings}
        self.assertIn("WordCountParity", cats)

        _inv2, ok_findings = contract.audit_contract(
            sample_md,
            journal="mnsc",
            exemplar_abs_words=95,
            exemplar_intro_words=920,
        )
        ok_cats = {f.category for f in ok_findings}
        self.assertNotIn("WordCountParity", ok_cats)


class TestPdfLayoutAuditor(unittest.TestCase):
    def test_clean_pdf_with_math_scripts_passes(self) -> None:
        import fitz

        with tempfile.TemporaryDirectory() as tmp:
            pdf_path = Path(tmp) / "clean.pdf"
            doc = fitz.open()
            for p in range(2):
                page = doc.new_page(width=612, height=792)
                for y in range(100, 660, 22):
                    page.insert_text(
                        (72, y),
                        f"Page {p + 1} clean line {y}: concrete operational intuition holds cleanly.",
                        fontsize=10.5,
                    )
                # Simulated inline variable with small subscript/superscript slightly overlapping bbox
                page.insert_text((72, 682), "x", fontsize=11.0)
                page.insert_text((77, 686), "i", fontsize=6.5)
                page.insert_text((78, 677), "2", fontsize=6.5)
            doc.save(str(pdf_path))
            doc.close()

            findings, _ = pdf_qa.audit_pdf(pdf_path)
            errs = [f for f in findings if f.severity == "ERROR"]
            self.assertEqual(errs, [], f"Expected 0 ERRORs on clean PDF, got {errs}")

    def test_garbled_overlap_blank_gap_margin_and_log(self) -> None:
        import fitz

        with tempfile.TemporaryDirectory() as tmp:
            pdf_path = Path(tmp) / "broken.pdf"
            log_path = Path(tmp) / "broken.log"
            snap_dir = Path(tmp) / "snaps"

            doc = fitz.open()
            # Page 1: mojibake Ã©, unresolved ??, [?], overlapping lines, right-margin overflow
            p1 = doc.new_page(width=612, height=792)
            p1.insert_text((72, 100), "Broken mojibake Ã© in Section ?? and citation [?].", fontsize=11)
            p1.insert_text((72, 102), "Colliding overlapping line drawn right across top line.", fontsize=11)
            p1.insert_text((430, 160), "Extremely long overflowing expression into right margin edge!", fontsize=11)
            for y in range(200, 680, 24):
                p1.insert_text((72, y), f"Body filler row {y} keeping page non-blank.", fontsize=10.5)

            # Page 2: completely blank interior page
            doc.new_page(width=612, height=792)

            # Page 3: top text + giant mid-page gap + bottom text
            p3 = doc.new_page(width=612, height=792)
            p3.insert_text((72, 105), "Top block ends abruptly before restrictive float gap.", fontsize=11)
            p3.insert_text((72, 125), "Short continuation line above whitespace gap.", fontsize=11)
            p3.insert_text((72, 640), "Bottom block forced way down leaving giant void.", fontsize=11)

            doc.save(str(pdf_path))
            doc.close()

            log_path.write_text(
                "Missing character: There is no \u2212 in font cmr10!\n"
                "Overfull \\hbox (18.5pt too wide) in paragraph at lines 42--45\n"
                "Underfull \\vbox (badness 10000) has occurred while \\output is active\n",
                encoding="utf-8",
            )

            findings, snaps = pdf_qa.audit_pdf(pdf_path, log_path=log_path, render_dir=snap_dir)
            cats = {f.category for f in findings}
            for expected in (
                "GarbledText",
                "UnresolvedRef",
                "TextOverlap",
                "MarginProtrusion",
                "BlankPage",
                "MidPageGap",
                "MissingGlyph",
                "OverfullHbox",
                "UnderfullVbox",
            ):
                self.assertIn(expected, cats, f"Missing expected PDF finding {expected}; got {cats}")

            self.assertTrue(len(snaps) >= 2, f"Expected flagged PNG snapshots, got {snaps}")
            for sp in snaps:
                self.assertTrue(sp.is_file() and sp.stat().st_size > 0)

            proc = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "check_pdf_layout.py"), str(pdf_path), "--render-flagged", str(snap_dir)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)


class TestSkillHygieneAndLinks(unittest.TestCase):
    def test_zero_cjk_inside_informs_writing(self) -> None:
        cjk_re = re.compile(r"[\u4e00-\u9fff]")
        for ext in ("*.md", "*.py", "*.tex", "*.txt"):
            for fp in INFORMS_WRITING_DIR.rglob(ext):
                txt = fp.read_text(encoding="utf-8", errors="replace")
                m = cjk_re.search(txt)
                self.assertIsNone(
                    m,
                    f"CJK character '{m.group(0) if m else ''}' found in English-only skill file: {fp}",
                )

    def test_skill_markdown_relative_links_exist(self) -> None:
        link_re = re.compile(r"\]\((\.\.?/[^)#\s]+)")
        md_files = [INFORMS_WRITING_DIR / "SKILL.md", ZH_REVIEW_DIR / "SKILL.md"] + sorted(
            (INFORMS_WRITING_DIR / "references").glob("*.md")
        )
        for md_path in md_files:
            self.assertTrue(md_path.is_file(), f"Missing {md_path}")
            text = md_path.read_text(encoding="utf-8")
            for rel in link_re.findall(text):
                target = (md_path.parent / rel).resolve()
                self.assertTrue(
                    target.exists(),
                    f"Broken link {rel} inside {md_path} -> {target}",
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
