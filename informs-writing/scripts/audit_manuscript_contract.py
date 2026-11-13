#!/usr/bin/env python3
"""Cross-section manuscript contract auditor and Unified Online Appendix placer.

Contract mode:
  Parses Abstract, Intro, Related Literature, Model/Design, Results, Conclusion,
  and Online Appendix (\\.tex, .md, or .txt) and flags:
    - Claim-strength escalation (Abstract/Conclusion stronger than Results)
    - Missing comparators on improvement claims in Abstract
    - Cross-section synonym-family terminology drift
    - Headline quantitative magnitude drift between Abstract and Results
    - Uninterpreted Online Appendix pointers

Placement mode (`--place-results`):
  Classifies one-item-per-line theorems, proofs, tables, and robustness checks
  under the 100% Unified Online Appendix (\\ECSwitch / Online Appendix EC.x) rule.
  Never recommends regular \\appendix for any INFORMS journal.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


class ContractFinding(NamedTuple):
    severity: str  # ERROR | WARN
    category: str
    section: str
    message: str


SYNONYM_FAMILIES = {
    "buyer": ["customer", "consumer", "buyer", "client", "shopper"],
    "intermediary": ["platform", "marketplace", "intermediary", "exchange"],
    "method": ["algorithm", "heuristic", "solver", "procedure"],
    "agent": ["worker", "driver", "gig-worker", "contractor", "courier"],
}

COMPARATOR_CUES = re.compile(
    r"\b(?:relative to|compared (?:to|with)|versus|vs\.?|over|benchmark|baseline|"
    r"status quo|myopic|first-best|no-information|single-sourcing|uniform pricing|"
    r"state-of-the-art|fifo|fcfs|greedy)\b",
    re.IGNORECASE,
)

IMPROVEMENT_CLAIM_RE = re.compile(
    r"\b(?:outperforms?|improves?|reduces?|increases?|raises?|lowers?|dominates?|beats?|"
    r"speeds? up|faster|higher|lower)\b",
    re.IGNORECASE,
)

STRONG_UNIVERSAL_RE = re.compile(
    r"\b(?:always|universally|guarantees?|guaranteed|strictly dominates?|proves?|proven)\b",
    re.IGNORECASE,
)

QUALIFIED_EMPIRICAL_RE = re.compile(
    r"\b(?:is consistent with|correlates?|suggests?|associated with|conditional on|"
    r"under assumption|local average|reduced-form|in our sample)\b",
    re.IGNORECASE,
)


def strip_tex_comments(raw: str) -> str:
    return "\n".join(
        ln[: re.search(r"(?<!\\)%", ln).start()] if re.search(r"(?<!\\)%", ln) else ln
        for ln in raw.splitlines()
    )


def _extract_brace_block(text: str, macro: str) -> str:
    m = re.search(r"\\" + re.escape(macro) + r"\s*\{", text)
    if not m:
        return ""
    start = m.end()
    depth = 1
    i = start
    while i < len(text) and depth > 0:
        if text[i] == "\\" and i + 1 < len(text):
            i += 2
            continue
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start:i]
        i += 1
    return ""


def _classify_heading(title: str) -> str:
    t = title.lower()
    if "abstract" in t:
        return "Abstract"
    if "intro" in t:
        return "Intro"
    if "related" in t or "literature" in t or "background" in t:
        return "Related"
    if any(k in t for k in ("model", "setting", "design", "data", "identification", "formulation", "algorithm", "prelimin")):
        return "Model/Design"
    if any(k in t for k in ("result", "analysis", "main", "experiment", "computational", "empirical", "finding", "structural")):
        return "Results"
    if any(k in t for k in ("conclu", "discussion", "implication", "future")):
        return "Conclusion"
    if "online appendix" in t or "e-companion" in t or "ec." in t:
        return "Online Appendix"
    return "Body"


def parse_sections(raw: str) -> dict[str, str]:
    """Parse LaTeX or Markdown manuscript into canonical sections."""
    is_latex = bool(
        re.search(r"\\(?:documentclass|begin\{document\}|section|ABSTRACT)\b", raw)
    )
    clean = strip_tex_comments(raw) if is_latex else raw
    sections: dict[str, list[str]] = {
        "Abstract": [],
        "Intro": [],
        "Related": [],
        "Model/Design": [],
        "Results": [],
        "Conclusion": [],
        "Online Appendix": [],
    }

    abs_tex = _extract_brace_block(clean, "ABSTRACT")
    if abs_tex:
        sections["Abstract"].append(abs_tex)

    if r"\ECSwitch" in clean:
        main_part, ec_part = clean.split(r"\ECSwitch", 1)
        sections["Online Appendix"].append(ec_part)
    else:
        main_part = clean

    heading_re = re.compile(
        r"(?:\\(?:section|subsection|ECHead)\*?\{([^}]+)\}|^#{1,2}\s+(.+)$)",
        re.MULTILINE,
    )
    matches = list(heading_re.finditer(main_part))
    if not matches:
        return {k: "\n".join(v).strip() for k, v in sections.items()}

    for idx, m in enumerate(matches):
        title = (m.group(1) or m.group(2) or "").strip()
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(main_part)
        bucket = _classify_heading(title)
        if bucket in sections:
            sections[bucket].append(main_part[start:end])

    return {k: "\n".join(v).strip() for k, v in sections.items()}


def audit_contract(
    raw: str,
    journal: str = "mnsc",
    exemplar_abs_words: int | None = None,
    exemplar_intro_words: int | None = None,
) -> tuple[dict[str, int], list[ContractFinding]]:
    sections = parse_sections(raw)
    inventory = {k: len(re.findall(r"\b[a-zA-Z0-9-]+\b", v)) for k, v in sections.items()}
    findings: list[ContractFinding] = []

    abs_txt = sections["Abstract"]
    intro_txt = sections["Intro"]
    results_txt = sections["Results"]
    concl_txt = sections["Conclusion"]

    # 1. Claim-strength escalation (Abstract / Intro / Conclusion stronger than Results)
    if results_txt:
        results_qualified = bool(QUALIFIED_EMPIRICAL_RE.search(results_txt)) and not bool(
            STRONG_UNIVERSAL_RE.search(results_txt)
        )
        if results_qualified:
            for sec_name, sec_txt in (("Abstract", abs_txt), ("Intro", intro_txt), ("Conclusion", concl_txt)):
                m = STRONG_UNIVERSAL_RE.search(sec_txt)
                if m:
                    findings.append(
                        ContractFinding(
                            "ERROR",
                            "ClaimEscalation",
                            sec_name,
                            f"{sec_name} uses universal/deductive claim '{m.group(0)}' while Results presents qualified/empirical evidence.",
                        )
                    )

        # Direct contradiction: Results explicitly uses correlation/suggests while Conclusion asserts proves/guarantees
        if re.search(r"\b(proves?|guarantees?)\b", concl_txt, re.IGNORECASE) and not re.search(
            r"\b(?:theorem|proposition|lemma|corollary|proof)\b", results_txt, re.IGNORECASE
        ):
            findings.append(
                ContractFinding(
                    "ERROR",
                    "ClaimEscalation",
                    "Conclusion",
                    "Conclusion asserts 'prove/guarantee' without corresponding formal theorem/proposition in Results.",
                )
            )

    # 2. Missing comparator in Abstract improvement claims
    if abs_txt and IMPROVEMENT_CLAIM_RE.search(abs_txt) and not COMPARATOR_CUES.search(abs_txt):
        findings.append(
            ContractFinding(
                "WARN",
                "MissingComparator",
                "Abstract",
                "Abstract makes an improvement/comparison claim without naming the baseline or benchmark comparator.",
            )
        )

    # 3. Cross-section synonym-family terminology drift
    full_body = " ".join([abs_txt, intro_txt, sections["Model/Design"], results_txt, concl_txt]).lower()
    body_tokens = re.findall(r"\b[a-z][a-z-]+\b", full_body)
    for fam, variants in SYNONYM_FAMILIES.items():
        present = [v for v in variants if body_tokens.count(v) >= 2]
        if len(present) >= 3:
            findings.append(
                ContractFinding(
                    "WARN",
                    "TerminologyDrift",
                    "Manuscript",
                    f"Disease 6 ({fam} family): manuscript rotates {present}; unify on one canonical noun.",
                )
            )

    # 4. Headline percentage drift between Abstract/Intro and Results
    pct_pat = re.compile(r"\b(\d+(?:\.\d+)?)\s*(?:\\?%|percent\b)", re.IGNORECASE)
    if abs_txt and results_txt:
        abs_pcts = set(pct_pat.findall(abs_txt))
        res_pcts = set(pct_pat.findall(results_txt))
        if abs_pcts and res_pcts and not (abs_pcts & res_pcts):
            findings.append(
                ContractFinding(
                    "WARN",
                    "MagnitudeDrift",
                    "Abstract/Results",
                    f"Abstract cites percentage(s) {sorted(abs_pcts)}% not matching Results figure(s) {sorted(res_pcts)}%.",
                )
            )

    # 5. Uninterpreted Online Appendix pointers
    for sec_name, sec_txt in sections.items():
        if sec_name == "Online Appendix":
            continue
        for m in re.finditer(
            r"\.\s*(?:See|Details are in|Deferred to)\s+(?:Online\s+)?Appendix\s+(?:EC\.?\d+|[A-Z])\s*\.",
            sec_txt,
            re.IGNORECASE,
        ):
            findings.append(
                ContractFinding(
                    "WARN",
                    "EmptyECPointer",
                    sec_name,
                    f"Empty pointer '{m.group(0).strip()}'; briefly state the proof idea or verification takeaway before pointing to Online Appendix EC.x.",
                )
            )

    # 6. Regular Appendix leak inside section headers
    if re.search(r"\\appendix\b", raw):
        findings.append(
            ContractFinding(
                "ERROR",
                "AppendixPolicy",
                "Structure",
                "Manuscript contains \\appendix; convert to Unified Online Appendix (\\ECSwitch + \\ECHead).",
            )
        )

    # 7. Exemplar Abstract / Intro word-count parity and internal length balance
    abs_wc = inventory["Abstract"]
    intro_wc = inventory["Intro"]
    if exemplar_abs_words and exemplar_abs_words > 0 and abs_wc > 0:
        rel_diff = abs(abs_wc - exemplar_abs_words) / exemplar_abs_words
        if rel_diff > 0.20:
            findings.append(
                ContractFinding(
                    "WARN",
                    "WordCountParity",
                    "Abstract",
                    f"Abstract word count ({abs_wc}w) deviates {rel_diff * 100:.0f}% from exemplar benchmark ({exemplar_abs_words}w; target within +/-20%).",
                )
            )
    if exemplar_intro_words and exemplar_intro_words > 0 and intro_wc > 0:
        rel_diff = abs(intro_wc - exemplar_intro_words) / exemplar_intro_words
        if rel_diff > 0.20:
            findings.append(
                ContractFinding(
                    "WARN",
                    "WordCountParity",
                    "Intro",
                    f"Introduction word count ({intro_wc}w) deviates {rel_diff * 100:.0f}% from exemplar benchmark ({exemplar_intro_words}w; target within +/-20%).",
                )
            )
    if sum(inventory.values()) >= 800 and abs_wc > 0 and intro_wc > 0:
        if intro_wc < 3 * abs_wc or intro_wc < 500:
            findings.append(
                ContractFinding(
                    "WARN",
                    "LengthBalance",
                    "Abstract/Intro",
                    f"Introduction ({intro_wc}w) is disproportionately short relative to Abstract ({abs_wc}w); target ~6x--11x Abstract length (~1,100--1,800w).",
                )
            )
        elif intro_wc > 2600:
            findings.append(
                ContractFinding(
                    "WARN",
                    "LengthBalance",
                    "Abstract/Intro",
                    f"Introduction ({intro_wc}w) is disproportionately long (>2,600w); tighten motivation so core results keep budget.",
                )
            )

    return inventory, findings


def classify_result_item(line: str, journal: str) -> tuple[str, str]:
    """Classify one result/proof/table item under Unified Online Appendix rules."""
    low = line.lower()

    if journal == "ijoc" and any(k in low for k in ("code", "github", "docker", "instance", "dataset", "solver script", "benchmark file")):
        return (
            "COMPANION_REPO (.cd)",
            "Place in INFORMSJoC companion repo (dual DOI); cite concisely in Software & Data section.",
        )

    if any(k in low for k in ("robustness", "placebo", "sensitivity", "alternative spec", "auxiliary lemma", "technical lemma", "full proof", "proof of", "tuning", "ablation", "hyperparameter", "appendix")):
        note = "Defer to Unified Online Appendix (\\ECSwitch -> Online Appendix EC.x)."
        if journal == "msom":
            note += " Watch M&SOM 16-page EC ceiling."
        return "ONLINE_APPENDIX_EC", note

    if any(k in low for k in ("headline", "main theorem", "proposition 1", "main table", "baseline", "mechanism", "algorithm", "identification")) or re.search(
        r"\b(?:theorem|proposition)\s+\d+\b", low
    ):
        note = "Keep in Main Body (conveys core theorem, table, or identification intuition)."
        if journal in {"opre", "ijoc"} and any(k in low for k in ("theorem", "proposition")):
            note += " Pair with a 3--6 sentence Proof Sketch in body; full derivation -> Online Appendix EC.x."
        return "MAIN_BODY", note

    return (
        "ONLINE_APPENDIX_EC",
        "Default to Unified Online Appendix (Online Appendix EC.x) unless essential to the core story.",
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit cross-section contract drift or classify Online Appendix placement."
    )
    parser.add_argument("target", help="Path to .tex/.md/.txt manuscript, or item list with --place-results ('-' for stdin)")
    parser.add_argument(
        "--journal",
        choices=("opre", "mnsc", "msom", "ijoc"),
        default="mnsc",
        help="Target INFORMS journal (default: mnsc)",
    )
    parser.add_argument(
        "--place-results",
        action="store_true",
        help="Read one item per line and emit MAIN_BODY vs. ONLINE_APPENDIX_EC placement plan",
    )
    parser.add_argument(
        "--exemplar-abstract-words",
        type=int,
        default=None,
        help="Exemplar Abstract word count target for +/-20%% parity check",
    )
    parser.add_argument(
        "--exemplar-intro-words",
        type=int,
        default=None,
        help="Exemplar Introduction word count target for +/-20%% parity check",
    )
    parser.add_argument("--strict", action="store_true", help="Exit 1 on WARN as well as ERROR")
    parser.add_argument("--advisory", action="store_true", help="Always exit 0")
    args = parser.parse_args()

    if args.target == "-":
        raw = sys.stdin.read()
        name = "<stdin>"
    else:
        p = Path(args.target)
        if not p.is_file():
            print(f"ERROR: file not found: {p}", file=sys.stderr)
            return 2
        raw = p.read_text(encoding="utf-8", errors="replace")
        name = p.name

    if args.place_results:
        print(f"PLACEMENT PLAN (journal={args.journal}, rule=100% Unified Online Appendix \\ECSwitch):")
        for idx, item in enumerate(raw.splitlines(), start=1):
            stripped = item.strip()
            if not stripped or stripped.startswith("#"):
                continue
            bucket, rationale = classify_result_item(stripped, args.journal)
            print(f"  {idx:02d}. [{bucket}] {stripped}\n      -> {rationale}")
        return 0

    inventory, findings = audit_contract(
        raw,
        journal=args.journal,
        exemplar_abs_words=args.exemplar_abstract_words,
        exemplar_intro_words=args.exemplar_intro_words,
    )
    inv_str = ", ".join(f"{k}={w}w" for k, w in inventory.items() if w > 0)
    print(f"INVENTORY ({name}, journal={args.journal}): {inv_str or 'no explicit section headers detected'}")

    if not findings:
        print("PASS: 0 contract drift issues found.")
        return 0

    errs = sum(1 for f in findings if f.severity == "ERROR")
    warns = sum(1 for f in findings if f.severity == "WARN")
    print(f"CONTRACT AUDIT: {errs} ERROR(s), {warns} WARN(s)")
    for f in findings:
        print(f"  [{f.severity}][{f.category}][{f.section}] {f.message}")

    if args.advisory:
        return 0
    if errs > 0 or (args.strict and warns > 0):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
