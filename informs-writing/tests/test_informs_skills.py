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

        stacked_props = CLEAN_TEX_BASE.replace(
            r"\section{Conclusion}",
            "To characterize optimal dispatch, we begin with the short-lead-time benchmark.\n"
            "\\begin{proposition}Short lead times admit a threshold rule.\\end{proposition}\n"
            "Next we state Proposition 2.\n"
            "\\begin{proposition}Long lead times compress the feedback gain.\\end{proposition}\n"
            "\\section{Conclusion}",
        )
        stacked_warns = {f.category for f in aud.audit_manuscript(stacked_props) if f.severity == "WARN"}
        self.assertIn("UnbridgedResult", stacked_warns)

        bridged_props = CLEAN_TEX_BASE.replace(
            r"\section{Conclusion}",
            "To characterize optimal dispatch, we begin with the short-lead-time benchmark.\n"
            "\\begin{proposition}Short lead times admit a threshold rule.\\end{proposition}\n"
            "Proposition 1 settles the short-lead-time regime where on-hand stock never expires in transit, "
            "leaving open how the optimal policy shifts once lead time exceeds shelf life. "
            "To resolve that long-lead-time bottleneck, our next result bounds the remaining value of state feedback.\n"
            "\\begin{proposition}Long lead times compress the feedback gain.\\end{proposition}\n"
            "\\section{Conclusion}",
        )
        bridged_warns = {f.category for f in aud.audit_manuscript(bridged_props) if f.severity == "WARN"}
        self.assertNotIn("UnbridgedResult", bridged_warns)

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

    def test_abstract_word_threshold_270(self) -> None:
        abs_255 = " ".join(["dispatch"] * 255)
        tex_255 = CLEAN_TEX_BASE.replace(
            "We study dynamic dispatch when carriers face stochastic travel delays. Using a fluid-limit relaxation and priority coupling, we show that a threshold index rule reduces expected holding costs by roughly 2\\% relative to a greedy FIFO baseline.",
            abs_255,
        )
        cats_255 = {f.category for f in aud.audit_manuscript(tex_255, journal="ijoc")}
        self.assertNotIn("Abstract", cats_255)

        abs_280 = " ".join(["dispatch"] * 280)
        tex_280 = CLEAN_TEX_BASE.replace(
            "We study dynamic dispatch when carriers face stochastic travel delays. Using a fluid-limit relaxation and priority coupling, we show that a threshold index rule reduces expected holding costs by roughly 2\\% relative to a greedy FIFO baseline.",
            abs_280,
        )
        warns_280 = {f.category for f in aud.audit_manuscript(tex_280, journal="ijoc") if f.severity == "WARN"}
        self.assertIn("Abstract", warns_280)


    def test_parenthetical_gloss_warnings_and_carveouts(self) -> None:
        gloss_tex = CLEAN_TEX_BASE.replace(
            "Online freight marketplaces assign incoming orders to drivers under uncertain transit times.",
            "Online freight marketplaces assign incoming orders under a threshold rule "
            "(that is, a policy that dispatches orders once backlog exceeds a cutoff).",
        )
        warn_cats = {f.category for f in aud.audit_manuscript(gloss_tex, journal="mnsc") if f.severity == "WARN"}
        self.assertIn("ParentheticalGloss", warn_cats)

        dense_tex = CLEAN_TEX_BASE.replace(
            "Online freight marketplaces assign incoming orders to drivers under uncertain transit times.",
            "Carriers apply a dispatch cutoff (the daily backlog threshold) during demand surges (the evening delivery peak).",
        )
        dense_warns = {f.category for f in aud.audit_manuscript(dense_tex, journal="mnsc") if f.severity == "WARN"}
        self.assertIn("ParentheticalGloss", dense_warns)

        clean_carveouts = CLEAN_TEX_BASE.replace(
            "Online freight marketplaces assign incoming orders to drivers under uncertain transit times.",
            "Carriers solve a mixed-integer linear program (MILP) following prior work "
            "(Levi et al. 2015, Besbes and Zeevi 2020) and benchmark costs (Table 1; see Online Appendix EC.1).",
        )
        carveout_warns = {f.category for f in aud.audit_manuscript(clean_carveouts, journal="mnsc") if f.severity == "WARN"}
        self.assertNotIn("ParentheticalGloss", carveout_warns)

    def test_numeric_clutter_warnings_and_trend_prose_carveouts(self) -> None:
        cluttered_tex = CLEAN_TEX_BASE.replace(
            "Online freight marketplaces assign incoming orders to drivers under uncertain transit times.",
            "In Panel A, raising $L$ from 1 to 5 causes excess cost to jump from 5.1 (5.6\\%) to 20.7 (+21\\%), "
            "while the open-loop gap narrows from 9.3 at $L=1$ to 4.4 at $L=2$, 2.1 at $L=3$, and 0.6 at $L=5$.",
        )
        warn_cats = {f.category for f in aud.audit_manuscript(cluttered_tex, journal="mnsc") if f.severity == "WARN"}
        self.assertIn("NumericClutter", warn_cats)

        trend_tex = CLEAN_TEX_BASE.replace(
            "Online freight marketplaces assign incoming orders to drivers under uncertain transit times.",
            "As lead time grows relative to shelf life, the age-blind benchmark deteriorates sharply, increasing "
            "excess cost roughly fourfold, whereas the state-feedback advantage steadily narrows (Table 1).",
        )
        trend_warns = {f.category for f in aud.audit_manuscript(trend_tex, journal="mnsc") if f.severity == "WARN"}
        self.assertNotIn("NumericClutter", trend_warns)

    def test_opre_official_guidelines_checks(self) -> None:
        orig_abs = "We study dynamic dispatch when carriers face stochastic travel delays. Using a fluid-limit relaxation and priority coupling, we show that a threshold index rule reduces expected holding costs by roughly 2\\% relative to a greedy FIFO baseline."
        opre_base = CLEAN_TEX_BASE.replace("[mnsc,nonblindrev]", "[opre,dblanonrev]")

        # 195-word single-paragraph abstract passes for opre
        ok_195 = opre_base.replace(orig_abs, " ".join(["dispatch"] * 195))
        errs_195 = [f for f in aud.audit_manuscript(ok_195, journal="opre") if f.severity == "ERROR"]
        self.assertEqual(errs_195, [], f"Expected 0 ERRORs for 195-word OPRE abstract, got {errs_195}")

        # 205-word abstract fails hard for opre (and contract auditor)
        bad_205 = opre_base.replace(orig_abs, " ".join(["dispatch"] * 205))
        err_cats = {f.category for f in aud.audit_manuscript(bad_205, journal="opre") if f.severity == "ERROR"}
        self.assertIn("Journal-OR", err_cats)
        _inv, c_findings = contract.audit_contract("# Abstract\n" + " ".join(["word"] * 205), journal="opre")
        self.assertTrue(any(f.severity == "ERROR" and f.category == "AbstractLength" for f in c_findings))

        # Multi-paragraph abstract and math in abstract fail hard for opre
        bad_multi = opre_base.replace(orig_abs, "First paragraph with math $x > 0$.\n\nSecond paragraph.")
        multi_errs = {f.category for f in aud.audit_manuscript(bad_multi, journal="opre") if f.severity == "ERROR"}
        self.assertIn("Journal-OR", multi_errs)
        self.assertIn("Abstract", multi_errs)

        # nonblindrev emits double-anonymous advisory warning for opre
        nonblind_warns = {f.category for f in aud.audit_manuscript(CLEAN_TEX_BASE, journal="opre") if f.severity == "WARN"}
        self.assertIn("Journal-OR", nonblind_warns)

    def test_mnsc_official_guidelines_checks(self) -> None:
        orig_abs = "We study dynamic dispatch when carriers face stochastic travel delays. Using a fluid-limit relaxation and priority coupling, we show that a threshold index rule reduces expected holding costs by roughly 2\\% relative to a greedy FIFO baseline."
        mnsc_base = CLEAN_TEX_BASE.replace("[mnsc,nonblindrev]", "[mnsc,dblanonrev]")

        # 245-word single-paragraph abstract passes for mnsc
        ok_245 = mnsc_base.replace(orig_abs, " ".join(["dispatch"] * 245))
        errs_245 = [f for f in aud.audit_manuscript(ok_245, journal="mnsc") if f.severity == "ERROR"]
        self.assertEqual(errs_245, [], f"Expected 0 ERRORs for 245-word MNSC abstract, got {errs_245}")

        # 255-word abstract fails hard for mnsc (and contract auditor)
        bad_255 = mnsc_base.replace(orig_abs, " ".join(["dispatch"] * 255))
        err_cats = {f.category for f in aud.audit_manuscript(bad_255, journal="mnsc") if f.severity == "ERROR"}
        self.assertIn("Journal-MS", err_cats)
        _inv, c_findings = contract.audit_contract("# Abstract\n" + " ".join(["word"] * 255), journal="mnsc")
        self.assertTrue(any(f.severity == "ERROR" and f.category == "AbstractLength" for f in c_findings))

        # Multi-paragraph abstract fails hard for mnsc
        bad_multi = mnsc_base.replace(orig_abs, "First paragraph.\n\nSecond paragraph.")
        multi_errs = {f.category for f in aud.audit_manuscript(bad_multi, journal="mnsc") if f.severity == "ERROR"}
        self.assertIn("Journal-MS", multi_errs)

        # nonblindrev emits double-anonymous advisory warning for mnsc
        nonblind_warns = {f.category for f in aud.audit_manuscript(CLEAN_TEX_BASE, journal="mnsc") if f.severity == "WARN"}
        self.assertIn("Journal-MS", nonblind_warns)

    def test_msom_and_ijoc_official_guidelines_checks(self) -> None:
        orig_abs = "We study dynamic dispatch when carriers face stochastic travel delays. Using a fluid-limit relaxation and priority coupling, we show that a threshold index rule reduces expected holding costs by roughly 2\\% relative to a greedy FIFO baseline."

        # M&SOM: 290-word 3-part structured abstract passes cleanly with dblanonrev
        msom_base = CLEAN_TEX_BASE.replace("[mnsc,nonblindrev]", "[msom,dblanonrev]")
        msom_290_abs = (
            "\\textbf{Problem definition:} " + " ".join(["dispatch"] * 90)
            + " \\textbf{Methodology/results:} " + " ".join(["routing"] * 100)
            + " \\textbf{Managerial implications:} " + " ".join(["capacity"] * 90)
        )
        ok_msom = msom_base.replace(orig_abs, msom_290_abs)
        errs_msom = [f for f in aud.audit_manuscript(ok_msom, journal="msom") if f.severity == "ERROR"]
        self.assertEqual(errs_msom, [], f"Expected 0 ERRORs for 290-word MSOM structured abstract, got {errs_msom}")

        # M&SOM: >300-word abstract fails hard in both draft and contract auditors
        bad_msom_310 = msom_base.replace(orig_abs, msom_290_abs + " " + " ".join(["policy"] * 30))
        msom_errs = {f.category for f in aud.audit_manuscript(bad_msom_310, journal="msom") if f.severity == "ERROR"}
        self.assertIn("MSOM-Abstract", msom_errs)
        _inv, c_msom = contract.audit_contract("# Abstract\n" + " ".join(["word"] * 305), journal="msom")
        self.assertTrue(any(f.severity == "ERROR" and f.category == "AbstractLength" for f in c_msom))

        # M&SOM: nonblindrev triggers double-anonymous WARN
        msom_nonblind_warns = {f.category for f in aud.audit_manuscript(CLEAN_TEX_BASE, journal="msom") if f.severity == "WARN"}
        self.assertIn("Journal-MSOM", msom_nonblind_warns)

        # IJOC: single-blind nonblindrev does NOT trigger a double-anonymous warning; >300w or multi-paragraph fails hard
        ijoc_base = CLEAN_TEX_BASE.replace("[mnsc,nonblindrev]", "[ijoc,nonblindrev]")
        ijoc_findings = aud.audit_manuscript(ijoc_base, journal="ijoc")
        self.assertEqual([f for f in ijoc_findings if f.severity == "ERROR"], [])
        self.assertFalse(any("double-anonymous" in f.message.lower() for f in ijoc_findings))

        bad_ijoc_310 = ijoc_base.replace(orig_abs, " ".join(["solver"] * 310))
        ijoc_errs = {f.category for f in aud.audit_manuscript(bad_ijoc_310, journal="ijoc") if f.severity == "ERROR"}
        self.assertIn("Journal-IJOC", ijoc_errs)
        bad_ijoc_multi = ijoc_base.replace(orig_abs, "First paragraph.\n\nSecond paragraph.")
        self.assertIn("Journal-IJOC", {f.category for f in aud.audit_manuscript(bad_ijoc_multi, journal="ijoc") if f.severity == "ERROR"})
        _inv2, c_ijoc = contract.audit_contract("# Abstract\n" + " ".join(["word"] * 305), journal="ijoc")
        self.assertTrue(any(f.severity == "ERROR" and f.category == "AbstractLength" for f in c_ijoc))


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

    def test_parenthetical_gloss_craft_check(self) -> None:
        bad = (
            "The retailer adopts a threshold rule (meaning it ships orders whenever backlog exceeds a cutoff). "
            "This policy stabilizes daily throughput."
        )
        bad_cats = {i.category for i in craft.analyze_prose(bad, section="model")}
        self.assertIn("ParentheticalGloss", bad_cats)

        good = (
            "The retailer solves a mixed-integer linear program (MILP) following standard queueing models "
            "(Smith 2020, Chen and Lee 2022) and summarizes benchmark costs (Table 2)."
        )
        good_cats = {i.category for i in craft.analyze_prose(good, section="model")}
        self.assertNotIn("ParentheticalGloss", good_cats)

    def test_numeric_clutter_craft_check(self) -> None:
        bad = (
            "Extending shelf life expands the savings gap from 4.4 to 16.8, a 22% reduction below the open-loop rule, "
            "while the base-stock excess shrinks from 10.0 to 1.3 (2.2%)."
        )
        bad_cats = {i.category for i in craft.analyze_prose(bad, section="results")}
        self.assertIn("NumericClutter", bad_cats)

        good = (
            "Extending shelf life widens the advantage of state feedback roughly fourfold relative to open-loop control, "
            "because surviving cohorts persist longer and carry greater replenishment value (Table 2, Figure 3b). "
            "In Section 4.1, these estimates remain significant (p = 0.012)."
        )
        good_cats = {i.category for i in craft.analyze_prose(good, section="results")}
        self.assertNotIn("NumericClutter", good_cats)


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

    def test_intro_page_cap_three_pages(self) -> None:
        import fitz

        with tempfile.TemporaryDirectory() as tmp:
            # 1) Passing: Intro from Page 1 (y=120) to Page 3 (y=400) -> ~2.35 pages
            ok_pdf = Path(tmp) / "ok_intro.pdf"
            doc_ok = fitz.open()
            for idx in range(4):
                pg = doc_ok.new_page(width=612, height=792)
                if idx == 0:
                    pg.insert_text((72, 120), "1 Introduction", fontsize=12)
                if idx == 2:
                    pg.insert_text((72, 400), "2 Model Setup", fontsize=12)
                for y in range(150, 680, 24):
                    if not (idx == 2 and y == 400):
                        pg.insert_text((72, y), f"Body prose line {y} on page {idx + 1}.", fontsize=10.5)
            doc_ok.save(str(ok_pdf))
            doc_ok.close()
            f_ok, _ = pdf_qa.audit_pdf(ok_pdf)
            self.assertNotIn("IntroPageCap", {f.category for f in f_ok})

            # 2) Flagged: Intro from Page 1 (y=120) to Page 5 (y=200) -> ~4.10 pages
            long_pdf = Path(tmp) / "long_intro.pdf"
            doc_long = fitz.open()
            for idx in range(5):
                pg = doc_long.new_page(width=612, height=792)
                if idx == 0:
                    pg.insert_text((72, 120), "1 Introduction", fontsize=12)
                if idx == 4:
                    pg.insert_text((72, 200), "2 Model Setup", fontsize=12)
                for y in range(150, 680, 24):
                    if not (idx == 4 and y == 200):
                        pg.insert_text((72, y), f"Body prose line {y} on page {idx + 1}.", fontsize=10.5)
            doc_long.save(str(long_pdf))
            doc_long.close()
            f_long, _ = pdf_qa.audit_pdf(long_pdf)
            self.assertIn("IntroPageCap", {f.category for f in f_long})


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

    def test_no_legacy_word_count_prescriptions(self) -> None:
        banned_re = re.compile(r"\b150\s*[–-]\s*210\b|\b1,100\s*[–-]\s*1,800\b")
        for fp in INFORMS_WRITING_DIR.rglob("*.md"):
            txt = fp.read_text(encoding="utf-8", errors="replace")
            m = banned_re.search(txt)
            self.assertIsNone(
                m,
                f"Legacy hardcoded word-count range '{m.group(0) if m else ''}' found in {fp}",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
