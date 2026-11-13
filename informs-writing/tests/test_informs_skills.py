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
        link_re = re.compile(r"\]\((\./[^)#\s]+)")
        for skill_dir in (INFORMS_WRITING_DIR, ZH_REVIEW_DIR):
            skill_md = skill_dir / "SKILL.md"
            self.assertTrue(skill_md.is_file(), f"Missing {skill_md}")
            text = skill_md.read_text(encoding="utf-8")
            for rel in link_re.findall(text):
                target = (skill_dir / rel).resolve()
                self.assertTrue(
                    target.exists(),
                    f"Broken link {rel} inside {skill_md} -> {target}",
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
