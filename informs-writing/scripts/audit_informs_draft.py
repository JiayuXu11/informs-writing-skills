#!/usr/bin/env python3
"""Hard-blocking INFORMS LaTeX manuscript gatekeeper and anti-AI auditor.

Enforces the Seven Iron Rules across Operations Research (opre), Management
Science (mnsc), M&SOM (msom), and INFORMS Journal on Computing (ijoc):
  1. Disease 1: Notation bloat, orphan symbols, unreferenced numbered equations
  2. Disease 2: Cold-start concepts / headings jumping straight to formal blocks
  3. Disease 3: AI clichés, participial tails, transition glue, prose em-dashes,
                colon-flourish bullets, negative parallelism, Chinglish, word bloat
  4. Disease 4: Defensive caveats immediately discounting results
  5. Disease 5: Raw decimal dumping in prose (precision belongs in booktabs tables)
  6. Disease 6: Definition bloat (>2 formal definitions) and duplicate definitions
  7. Disease 7: Chat / revision-history leakage and unfilled placeholders
Plus Unified Online Appendix (\\ECSwitch), booktabs/threeparttable hygiene,
and journal-specific hard rules.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


class Finding(NamedTuple):
    severity: str  # ERROR | WARN
    category: str
    line: int
    message: str


# ---------------------------------------------------------------------------
# Lexicons & Pattern Tables
# ---------------------------------------------------------------------------

AI_CLICHE_WORDS = (
    r"\b(?:"
    r"delve|delves|delved|delving|"
    r"tapestry|tapestries|"
    r"underscore|underscores|underscored|underscoring|"
    r"pivotal|testament|linchpin|cornerstone|watershed|"
    r"beacon|vibrant|breathtaking|bustling|boasts|"
    r"multifaceted|intricate|intricacies|"
    r"harness|harnessing|harnesses|"
    r"leverage|leverages|leveraged|leveraging|"
    r"foster|fosters|fostering|"
    r"catalyze|catalyzes|spearhead|revolutionize|transcend|"
    r"seamlessly|meticulously|groundbreaking|paradigm[- ]shifting|"
    r"holistic|synergy|synergies|synergistic|"
    r"myriad|plethora|nuanced|profoundly|indelible|"
    r"unprecedented|paramount|ubiquitous|ever[- ]evolving|"
    r"landscape|ecosystems?|realm|"
    r"notably|crucially|importantly|undoubtedly|"
    r"elucidate|elucidates|shed light on|pave the way|bridge the gap|"
    r"play(?:s|ed|ing)? a (?:crucial|pivotal|vital|key|significant) role|"
    r"in conclusion|to summarize"
    r")\b"
)

PARTICIPIAL_TAIL_RE = re.compile(
    r",\s+(?:thereby|thus|hence)?\s*(?:enabling|highlighting|underscoring|"
    r"illustrating|demonstrating|emphasizing|ensuring|fostering|reflecting|"
    r"showcasing|signaling|cementing|solidifying)\b",
    re.IGNORECASE,
)

SENTENCE_INITIAL_GLUE_RE = re.compile(
    r"(?:^|[.!?]\s+)(?:Moreover|Furthermore|Additionally|Consequently|"
    r"Importantly|Notably|Crucially|Interestingly|Significantly)\s*,",
    re.MULTILINE,
)

PROSE_EM_DASH_RE = re.compile(r"(?<!-)---(?!-)|—")

NEGATIVE_PARALLELISM_RE = re.compile(
    r"\bnot\s+(?:only|merely|simply|just)\b[^.!?\n]{1,100}\bbut\s+(?:also\b)?",
    re.IGNORECASE,
)

COLON_FLOURISH_RE = re.compile(
    r"\\item\s*(?:\*\*|\\textbf\{|\\emph\{)[^}:\n]{1,60}:(?:\*\*|\})",
    re.IGNORECASE,
)

CHINGLISH_PATTERNS = [
    (
        re.compile(
            r"\bwith the (?:rapid )?(?:development|advancement|popularization|rise|growth) of\b",
            re.IGNORECASE,
        ),
        "Chinglish opener ('with the rapid development of...'); lead directly with the concrete operational tension.",
    ),
    (
        re.compile(r"\bunder the background of\b", re.IGNORECASE),
        "Chinglish phrase ('under the background of'); replace with the specific operational setting or regulatory regime.",
    ),
    (
        re.compile(r"\baccording to the above (?:analysis|discussion|results)\b", re.IGNORECASE),
        "Vague forward/backward pointer ('according to the above analysis'); cite the exact Proposition/Table.",
    ),
    (
        re.compile(r"\bbased on this,\s+this (?:paper|study)\b", re.IGNORECASE),
        "Chinglish transition ('Based on this, this paper...'); state the specific methodological step directly.",
    ),
    (
        re.compile(r"\b(?:reach|achieve) (?:an )?optimal\b", re.IGNORECASE),
        "Ungrammatical/stiff phrase; use 'attain optimality', 'is optimal', or 'achieve the global optimum'.",
    ),
    (
        re.compile(r"\bit is worth mentioning that\b", re.IGNORECASE),
        "Filler lead-in ('it is worth mentioning that'); delete and state the point directly.",
    ),
    (
        re.compile(r"\bplays? an? (?:important|vital|significant|indispensable) role in\b", re.IGNORECASE),
        "Dead cliché ('plays an important role in'); replace with a concrete causal or structural verb.",
    ),
    (
        re.compile(r"\bin recent years,\s+(?:with the|many|more and more)\b", re.IGNORECASE),
        "Generic throat-clearing opener; start with the concrete decision problem or trade-off.",
    ),
    (
        re.compile(r"\bmore and more\b", re.IGNORECASE),
        "Informal/Chinglish quantifier ('more and more'); use 'increasingly' or state the empirical trend.",
    ),
]

MCCLOSKEY_BLOAT_RE = re.compile(
    r"\b(?:"
    r"as a matter of fact|in a very real sense|needless to say|"
    r"at this point in time|in the final analysis|last but not least|"
    r"in light of the fact that|despite the fact that|due to the fact that|"
    r"it should be noted that|it is interesting to note that|"
    r"needless to emphasize"
    r")\b",
    re.IGNORECASE,
)

DEFENSIVE_CAVEAT_RE = re.compile(
    r"\b(?:"
    r"does not (?:fully|necessarily|completely) (?:establish|prove|capture|account for)|"
    r"cannot (?:fully|conclusively) (?:guarantee|demonstrate|rule out|prove)|"
    r"although we (?:establish|prove|show|demonstrate)[^.]{0,100},\s*(?:this|our|it)\s+(?:does not|cannot|only|merely)|"
    r"should be interpreted with extreme caution|"
    r"remains an open question whether our results (?:apply|generalize|hold)|"
    r"we freely acknowledge that|"
    r"admittedly,\s+(?:our|this)\s+(?:model|assumption|analysis)"
    r")\b",
    re.IGNORECASE,
)

CONTEXT_LEAKAGE_PATTERNS = [
    re.compile(
        r"\b(?:"
        r"unlike the (?:previous|earlier|original) (?:version|draft|manuscript)|"
        r"as (?:requested|suggested|discussed|noted earlier) (?:by you|above|previously)|"
        r"I have (?:updated|revised|fixed|rewritten|corrected|expanded|shortened|addressed)|"
        r"we have (?:updated|revised|corrected) this (?:based on|in response to) your (?:feedback|comment)|"
        r"in the (?:updated|revised) (?:draft|version),?\s+we\s+(?:now|have)|"
        r"per your (?:instruction|request)|"
        r"as an AI\b|here is the revised"
        r")\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:TODO|FIXME|TBD|XXX)\b|\[(?:INSERT|ADD|CITE|AUTHOR|TODO)[^\]]*\]|\\todo\{",
        re.IGNORECASE,
    ),
]

COPULA_AVOIDANCE_RE = re.compile(
    r"\b(?:serves as an?|stands as an?|functions as an?|acts as an?)\b",
    re.IGNORECASE,
)

VAGUE_ATTRIBUTION_RE = re.compile(
    r"\b(?:"
    r"experts (?:argue|note|agree|believe)|"
    r"some (?:scholars|critics|researchers|analysts) (?:suggest|argue|note|claim)|"
    r"many (?:researchers|practitioners) believe|"
    r"observers note|it is widely (?:believed|recognized|acknowledged)"
    r")\b",
    re.IGNORECASE,
)

DECIMAL_DUMP_RE = re.compile(r"\b\d+\.\d{2,}\b(?:\s*%)?")

STANDARD_META_COMMANDS = {
    "abstract", "keywords", "subjectclass", "areaofreview", "history", "author", "title",
    "aff", "email", "thank", "thanks", "maketitle", "ecswitch", "echead", "ectext",
    "begin", "end", "section", "subsection", "subsubsection", "paragraph", "label",
    "ref", "eqref", "cref", "Cref", "autoref", "cite", "citet", "citep", "citealt",
    "citealp", "footnote", "endnote", "theendnotes", "textbf", "textit", "emph",
    "mathrm", "mathbf", "mathbb", "mathcal", "tilde", "hat", "bar", "vec", "frac",
    "sum", "prod", "int", "max", "min", "sup", "inf", "arg", "log", "exp", "Pr",
    "mathbb", "sqrt", "left", "right", "item", "caption", "centering", "toprule",
    "midrule", "bottomrule", "cmidrule", "usepackage", "documentclass", "input",
    "include", "bibliographystyle", "bibliography", "halmos", "Halmos", "qed",
    "url", "href", "texttt", "verb", "color", "textcolor", "nonumber", "notag",
}

STANDARD_SINGLE_CHARS = set("ijkmnltxyzpqrabcde0123456789+-=*/()[]{}.,;:!?<>|&^_'\" ")

# Regex matching common numeric threshold cutoffs or version/section qualifiers
# immediately preceding a decimal number so genuine thresholds are not flagged.
DECIMAL_ALLOW_PREFIX_RE = re.compile(
    r"(?:Section|Sec\.|Table|Tbl\.|Figure|Fig\.|Equation|Eq\.|Theorem|Thm\.|"
    r"Proposition|Prop\.|Lemma|Corollary|Cor\.|Assumption|EC\.|Appendix|v)\s*$",
    re.IGNORECASE,
)
DECIMAL_ALLOW_VALUE_SET = {"0.01", "0.05", "0.10", "0.90", "0.95", "0.99", "0.001"}
PVALUE_CONTEXT_RE = re.compile(r"\bp\s*[<>=]\s*0\.\d{2,}", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Preprocessing & Structure Helpers
# ---------------------------------------------------------------------------

def line_of_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _blank_preserving_newlines(match: re.Match[str]) -> str:
    return re.sub(r"[^\n]", " ", match.group(0))


def strip_latex_comments(text: str) -> str:
    """Remove unescaped % comments while preserving exact line counts."""
    out: list[str] = []
    for line in text.splitlines():
        m = re.search(r"(?<!\\)%", line)
        out.append(line[: m.start()] if m else line)
    return "\n".join(out)


def split_at_ec_switch(text: str) -> tuple[str, str]:
    """Split manuscript into (main_body_and_refs, online_appendix) at \\ECSwitch."""
    idx = text.find(r"\ECSwitch")
    if idx == -1:
        return text, ""
    return text[:idx], text[idx:]


def strip_references_section(text: str) -> str:
    """Blank out bibliography/references tail inside main body to avoid bib false positives."""
    m = re.search(
        r"\\(?:bibliographystyle|bibliography|begin\{thebibliography\}|section\*?\{References\})",
        text,
        re.IGNORECASE,
    )
    if not m:
        return text
    return text[: m.start()] + re.sub(r"[^\n]", " ", text[m.start() :])


def extract_brace_arg(text: str, macro: str) -> tuple[str, int] | None:
    """Extract balanced {...} argument following `\\macro`."""
    m = re.search(r"\\" + re.escape(macro) + r"\s*\{", text)
    if not m:
        return None
    start = m.end()
    depth = 1
    i = start
    while i < len(text) and depth > 0:
        ch = text[i]
        if ch == "\\" and i + 1 < len(text):
            i += 2
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start:i], line_of_offset(text, m.start())
        i += 1
    return None


def extract_prose_without_tables_or_math(main_body: str) -> str:
    """Mask tables, algorithms, math blocks, inline math, URLs, and code spans while preserving newlines."""
    masked = strip_references_section(main_body)
    env_names = (
        r"table\*?|tabular\*?|tabularx|equation\*?|align\*?|alignat\*?|gather\*?|"
        r"multline\*?|eqnarray\*?|cases|algorithm\*?|algorithm2e|algorithmic|"
        r"thebibliography|verbatim|lstlisting"
    )
    masked = re.sub(
        r"\\begin\{(" + env_names + r")\}.*?\\end\{\1\}",
        _blank_preserving_newlines,
        masked,
        flags=re.DOTALL,
    )
    masked = re.sub(r"\$\$.*?\$\$", _blank_preserving_newlines, masked, flags=re.DOTALL)
    masked = re.sub(r"\\\[.*?\\\]", _blank_preserving_newlines, masked, flags=re.DOTALL)
    masked = re.sub(r"(?<!\\)\$[^$\n]+?(?<!\\)\$", _blank_preserving_newlines, masked)
    masked = re.sub(
        r"\\(?:url|href|texttt|cite[tp]?|citeal[tp]|eqref|ref|cref|Cref|label)\{[^}]*\}",
        _blank_preserving_newlines,
        masked,
    )
    masked = re.sub(r"\\verb([^a-zA-Z\s]).*?\1", _blank_preserving_newlines, masked)
    return masked


def mask_conclusion(prose: str) -> str:
    """Blank out Conclusion / Future Work section when testing Disease 4 (Defensive Caveat)."""
    m = re.search(
        r"\\section\*?\{[^}]*(?:Conclusion|Concluding Remarks|Future Work|Limitations and Future)[^}]*\}",
        prose,
        re.IGNORECASE,
    )
    if not m:
        return prose
    return prose[: m.start()] + re.sub(r"[^\n]", " ", prose[m.start() :])


def prose_word_count(main_body: str) -> int:
    prose = extract_prose_without_tables_or_math(main_body)
    prose = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{[^}]*\})?", " ", prose)
    return len(re.findall(r"\b[a-zA-Z]{2,}\b", prose))


# ---------------------------------------------------------------------------
# Individual Audit Checks
# ---------------------------------------------------------------------------

def audit_abstract(main_body: str, journal: str) -> list[Finding]:
    findings: list[Finding] = []
    res = extract_brace_arg(main_body, "ABSTRACT")
    if not res:
        findings.append(
            Finding("ERROR", "Abstract", 1, "Missing \\ABSTRACT{...} block.")
        )
        return findings

    abs_text, line = res
    words = len(re.findall(r"\S+", abs_text))
    if words > 220:
        findings.append(
            Finding(
                "WARN",
                "Abstract",
                line,
                f"Abstract has {words} words (target <= 200 words for INFORMS journals).",
            )
        )
    if "\\cite" in abs_text:
        findings.append(
            Finding(
                "ERROR",
                "Abstract",
                line,
                "Citations inside \\ABSTRACT{...} are prohibited in INFORMS style.",
            )
        )
    if journal == "msom":
        required_parts = [
            "Problem definition",
            "Methodology",
            "Managerial implications",
        ]
        missing = [
            p
            for p in required_parts
            if re.search(re.escape(p), abs_text, re.IGNORECASE) is None
        ]
        if missing:
            findings.append(
                Finding(
                    "ERROR",
                    "MSOM-Abstract",
                    line,
                    f"M&SOM requires structured abstract headings; missing: {', '.join(missing)}.",
                )
            )
    return findings


def audit_journal_rules(main_body: str, journal: str) -> list[Finding]:
    findings: list[Finding] = []
    words = prose_word_count(main_body)

    if journal == "opre":
        if r"\SUBJECTCLASS" not in main_body:
            findings.append(
                Finding("ERROR", "Journal-OR", 1, "Operations Research requires \\SUBJECTCLASS{...}.")
            )
        if r"\AREAOFREVIEW" not in main_body:
            findings.append(
                Finding("ERROR", "Journal-OR", 1, "Operations Research requires \\AREAOFREVIEW{...}.")
            )
        for m in re.finditer(r"\\end\{(theorem|proposition)\}", main_body):
            tail = main_body[m.end() : m.end() + 1200]
            if not re.search(
                r"\\begin\{proof\}|proof\s+sketch|sketch\s+of\s+the\s+proof|"
                r"coupl|decompos|intuition|Online Appendix|EC\.",
                tail,
                re.IGNORECASE,
            ):
                findings.append(
                    Finding(
                        "WARN",
                        "Journal-OR",
                        line_of_offset(main_body, m.start()),
                        f"Headline {m.group(1)} lacks a nearby 3--6 sentence Proof Sketch or Online Appendix EC.x pointer.",
                    )
                )

    elif journal == "mnsc":
        kw = extract_brace_arg(main_body, "KEYWORDS")
        if not kw:
            findings.append(
                Finding("ERROR", "Journal-MS", 1, "Management Science requires \\KEYWORDS{...} with 3--5 keywords.")
            )
        else:
            kw_text, line = kw
            items = [item.strip() for item in re.split(r"[;,]", kw_text) if item.strip()]
            if not (3 <= len(items) <= 5):
                findings.append(
                    Finding(
                        "ERROR",
                        "Journal-MS",
                        line,
                        f"Management Science requires 3--5 keywords; found {len(items)}.",
                    )
                )

    elif journal == "msom":
        for m in re.finditer(r"\\footnote\s*\{", main_body):
            findings.append(
                Finding(
                    "ERROR",
                    "Journal-MSOM",
                    line_of_offset(main_body, m.start()),
                    "M&SOM forbids bottom-of-page \\footnote{...}; convert to \\endnote{...} + \\theendnotes.",
                )
            )

    elif journal == "ijoc" and words >= 250:
        has_algo = bool(
            re.search(r"\\begin\{(?:algorithm|algorithm2e|algorithmic)\}", main_body)
        )
        has_repo = bool(
            re.search(r"INFORMSJoC|\.cd\b|GitHub|repository|companion\s+(?:code|data)", main_body, re.IGNORECASE)
        )
        if not has_algo:
            findings.append(
                Finding(
                    "WARN",
                    "Journal-IJOC",
                    1,
                    "IJOC computational papers normally include a formal algorithm block (algorithm2e/algorithmic).",
                )
            )
        if not has_repo:
            findings.append(
                Finding(
                    "WARN",
                    "Journal-IJOC",
                    1,
                    "IJOC expects Software/Data & Reproducibility repo disclosure (INFORMSJoC Dual-DOI / .cd protocol).",
                )
            )

    return findings


def audit_appendix_policy(full_text: str, main_body: str) -> list[Finding]:
    """Enforce 100% Unified Online Appendix (\\ECSwitch): zero regular \\appendix."""
    findings: list[Finding] = []
    for m in re.finditer(r"\\appendix\b", full_text):
        findings.append(
            Finding(
                "ERROR",
                "AppendixPolicy",
                line_of_offset(full_text, m.start()),
                "Regular \\appendix is forbidden under the 100% Unified Online Appendix rule; use \\ECSwitch and \\ECHead{...}.",
            )
        )
    prose = extract_prose_without_tables_or_math(main_body)
    for m in re.finditer(r"(?<!Online\s)\bAppendix\s+(?:[A-Z]\b|\d+\b)", prose):
        findings.append(
            Finding(
                "ERROR",
                "AppendixPolicy",
                line_of_offset(main_body, m.start()),
                f"Bare '{m.group(0)}' violates Unified Online Appendix naming; use 'Online Appendix EC.x'.",
            )
        )
    return findings


def audit_equation_hygiene(full_text: str, main_body: str) -> list[Finding]:
    """Disease 1: forbid eqnarray and unreferenced numbered displays."""
    findings: list[Finding] = []

    for m in re.finditer(r"\\begin\{eqnarray\*?\}", full_text):
        findings.append(
            Finding(
                "ERROR",
                "EquationHygiene",
                line_of_offset(full_text, m.start()),
                "Legacy 'eqnarray' environment has broken spacing; replace with 'align' or 'align*'.",
            )
        )

    referenced_labels = set(
        re.findall(r"\\(?:eqref|ref|cref|Cref|autoref)\{([^}]+)\}", full_text)
    )
    # Handle comma-separated multi-refs like \cref{eq:a,eq:b}
    expanded_refs: set[str] = set()
    for grp in referenced_labels:
        for item in grp.split(","):
            expanded_refs.add(item.strip())

    numbered_env = r"(equation|align|alignat|gather|multline)"
    for m in re.finditer(
        r"\\begin\{" + numbered_env + r"\}(.*?)\\end\{\1\}",
        main_body,
        flags=re.DOTALL,
    ):
        env_name = m.group(1)
        body = m.group(2)
        line = line_of_offset(main_body, m.start())
        labels: list[str] = []
        for raw_line in body.splitlines():
            if re.search(r"\\(?:nonumber|notag)\b", raw_line):
                continue
            labels.extend(re.findall(r"\\label\{([^}]+)\}", raw_line))
        if not labels:
            findings.append(
                Finding(
                    "ERROR",
                    "EquationHygiene",
                    line,
                    f"Numbered '{env_name}' has no \\label{{...}}; use '{env_name}*' or '\\[...\\]' for unreferenced displays.",
                )
            )
        elif not any(lbl in expanded_refs for lbl in labels):
            findings.append(
                Finding(
                    "ERROR",
                    "EquationHygiene",
                    line,
                    f"Numbered '{env_name}' label(s) {labels} never referenced via \\eqref/\\ref; switch to '{env_name}*'.",
                )
            )
    return findings


def audit_table_hygiene(main_body: str) -> list[Finding]:
    """Enforce booktabs rules: zero \\hline and zero vertical | column separators."""
    findings: list[Finding] = []
    for m in re.finditer(
        r"\\begin\{(tabular\*?|tabularx)\}(?:\{[^}]*\})?\s*\{([^}]*)\}(.*?)\\end\{\1\}",
        main_body,
        flags=re.DOTALL,
    ):
        colspec = m.group(2)
        tbody = m.group(3)
        start_line = line_of_offset(main_body, m.start())
        if "|" in colspec:
            findings.append(
                Finding(
                    "ERROR",
                    "TableHygiene",
                    start_line,
                    f"Vertical rules ('|') in table column spec '{colspec}' violate INFORMS/booktabs formatting.",
                )
            )
        for hm in re.finditer(r"\\hline\b|\\cline\b", tbody):
            findings.append(
                Finding(
                    "ERROR",
                    "TableHygiene",
                    line_of_offset(main_body, m.start(3) + hm.start()),
                    f"Forbidden '{hm.group(0)}' inside table; use \\toprule, \\midrule, \\cmidrule, and \\bottomrule.",
                )
            )
    return findings


def audit_orphan_symbols(main_body: str) -> list[Finding]:
    """Disease 1: flag custom math tokens appearing only once across the main body."""
    findings: list[Finding] = []
    body = strip_references_section(main_body)
    # Strip tables and preamble declarations before counting
    preamble_cut = body.find(r"\begin{document}")
    if preamble_cut != -1:
        body = body[preamble_cut:]

    math_chunks: list[tuple[str, int]] = []
    for m in re.finditer(r"(?<!\\)\$([^$\n]{1,120})(?<!\\)\$", body):
        math_chunks.append((m.group(1), line_of_offset(body, m.start())))

    token_lines: dict[str, list[int]] = {}
    for expr, line in math_chunks:
        macros = re.findall(r"\\([A-Za-z]+)", expr)
        for mc in macros:
            if mc in STANDARD_META_COMMANDS:
                continue
            key = "\\" + mc
            token_lines.setdefault(key, []).append(line)
        sub_tokens = re.findall(r"[A-Za-z]_\{?([A-Za-z0-9]+)\}?", expr)
        for tok in re.finditer(r"\b([A-Za-z](?:_\{?[A-Za-z0-9]+\}?)?)\b", expr):
            sym = tok.group(1)
            if len(sym) == 1 and sym in STANDARD_SINGLE_CHARS:
                continue
            if sym in sub_tokens:
                continue
            token_lines.setdefault(sym, []).append(line)

    orphans = [
        (sym, lines[0])
        for sym, lines in token_lines.items()
        if len(lines) == 1 and not sym.startswith("\\")
    ]
    if len(orphans) > 5:
        sample = ", ".join(f"{s} (L{ln})" for s, ln in orphans[:6])
        findings.append(
            Finding(
                "ERROR",
                "OrphanNotation",
                orphans[0][1],
                f"{len(orphans)} one-off math symbols defined/used only once ({sample}); drop symbol or express in plain English.",
            )
        )
    return findings


def audit_definition_discipline(main_body: str) -> list[Finding]:
    """Disease 2 (cold-start formal blocks) & Disease 6 (definition bloat / duplicates)."""
    findings: list[Finding] = []
    body = strip_references_section(main_body)

    # Disease 2: heading immediately followed by formal block without intuitive prose
    cold_re = re.compile(
        r"\\(?:sub)*section\*?\{[^}]+\}(?:\s*\\label\{[^}]+\})?\s*"
        r"\\begin\{(definition|assumption|theorem|proposition)\}",
        re.MULTILINE,
    )
    for m in cold_re.finditer(body):
        findings.append(
            Finding(
                "ERROR",
                "ColdStartBlock",
                line_of_offset(body, m.start()),
                f"Section heading jumps directly into \\begin{{{m.group(1)}}} with zero intuitive setup prose.",
            )
        )

    # Disease 6: too many formal definitions + duplicate concepts
    defs = list(
        re.finditer(r"\\begin\{definition\}(.*?)\\end\{definition\}", body, flags=re.DOTALL)
    )
    if len(defs) > 2:
        findings.append(
            Finding(
                "ERROR",
                "DefinitionBloat",
                line_of_offset(body, defs[2].start()),
                f"Found {len(defs)} formal \\begin{{definition}} blocks in main body (ceiling <= 2; weave routine terms into prose).",
            )
        )

    seen_terms: dict[str, int] = {}
    for dm in defs:
        dline = line_of_offset(body, dm.start())
        dtext = dm.group(1)
        # Check optional [Title] or \emph/\textbf defined term
        t_match = re.match(r"\s*\[([^\]]+)\]", dtext)
        term = t_match.group(1).strip().lower() if t_match else ""
        if not term:
            em = re.search(r"\\(?:emph|textbf)\{([^}]{2,50})\}", dtext)
            if em:
                term = re.sub(r"\s+", " ", em.group(1).strip().lower())
        if term:
            if term in seen_terms:
                findings.append(
                    Finding(
                        "ERROR",
                        "DuplicateDefinition",
                        dline,
                        f"Concept '{term}' defined multiple times (first at L{seen_terms[term]}).",
                    )
                )
            else:
                seen_terms[term] = dline
    return findings


def _is_allowed_decimal(prose: str, m: re.Match[str]) -> bool:
    val = m.group(0).rstrip("%").strip()
    if val in DECIMAL_ALLOW_VALUE_SET:
        return True
    prefix = prose[max(0, m.start() - 25) : m.start()]
    if DECIMAL_ALLOW_PREFIX_RE.search(prefix):
        return True
    window = prose[max(0, m.start() - 15) : min(len(prose), m.end() + 5)]
    if PVALUE_CONTEXT_RE.search(window):
        return True
    return False


def audit_prose_patterns(main_body: str, journal: str) -> list[Finding]:
    """Diseases 3, 4, 5, 7 plus advisory copula/vague-attribution signals."""
    findings: list[Finding] = []
    prose = extract_prose_without_tables_or_math(main_body)
    non_concl_prose = mask_conclusion(prose)

    # Disease 3: AI clichés
    for m in re.finditer(AI_CLICHE_WORDS, prose, flags=re.IGNORECASE):
        findings.append(
            Finding(
                "ERROR",
                "AICliche",
                line_of_offset(main_body, m.start()),
                f"AI cliché '{m.group(0)}'; replace with concrete operational phrasing.",
            )
        )

    # Disease 3: participial tails
    for m in PARTICIPIAL_TAIL_RE.finditer(prose):
        findings.append(
            Finding(
                "ERROR",
                "ParticipialTail",
                line_of_offset(main_body, m.start()),
                f"Formulaic participial tail '{m.group(0).strip()}'; split or use direct finite verb.",
            )
        )

    # Disease 3: sentence-initial transition glue
    glue_matches = list(SENTENCE_INITIAL_GLUE_RE.finditer(prose))
    if len(glue_matches) > 2:
        findings.append(
            Finding(
                "ERROR",
                "TransitionGlue",
                line_of_offset(main_body, glue_matches[2].start()),
                f"{len(glue_matches)} sentence-initial 'Moreover/Furthermore/Additionally,...' glue openers (limit <= 2 across entire main body).",
            )
        )

    # Disease 3: zero prose em-dashes
    for m in PROSE_EM_DASH_RE.finditer(prose):
        findings.append(
            Finding(
                "ERROR",
                "EmDash",
                line_of_offset(main_body, m.start()),
                "Prose em-dash ('---' or '—') forbidden; rewrite with commas, parentheses, colons, or a second sentence (en-dash '--' is for ranges only).",
            )
        )

    # Disease 3: negative parallelism
    for m in NEGATIVE_PARALLELISM_RE.finditer(prose):
        findings.append(
            Finding(
                "ERROR",
                "NegParallel",
                line_of_offset(main_body, m.start()),
                f"Formulaic negative parallelism ('{m.group(0)}'); state the contribution positively.",
            )
        )

    # Disease 3: colon-flourish bullets
    for m in COLON_FLOURISH_RE.finditer(prose):
        findings.append(
            Finding(
                "ERROR",
                "ColonFlourish",
                line_of_offset(main_body, m.start()),
                "Decorative '**Label:**' bullet pattern; write direct topical prose or concise plain items.",
            )
        )

    # Disease 3: Chinglish calques
    for pat, msg in CHINGLISH_PATTERNS:
        for m in pat.finditer(prose):
            findings.append(
                Finding("ERROR", "Chinglish", line_of_offset(main_body, m.start()), msg)
            )

    # Disease 3: McCloskey verbal bloat
    for m in MCCLOSKEY_BLOAT_RE.finditer(prose):
        findings.append(
            Finding(
                "ERROR",
                "McCloskeyBloat",
                line_of_offset(main_body, m.start()),
                f"Verbal padding '{m.group(0)}'; delete to restore crisp active voice.",
            )
        )

    # Disease 4: defensive caveats outside Conclusion / Future Work
    for m in DEFENSIVE_CAVEAT_RE.finditer(non_concl_prose):
        findings.append(
            Finding(
                "ERROR",
                "DefensiveCaveat",
                line_of_offset(main_body, m.start()),
                f"Defensive post-result hedging ('{m.group(0)}'); state model boundary once in Setup/Conclusion.",
            )
        )

    # Disease 5: raw decimal dumping in prose
    for m in DECIMAL_DUMP_RE.finditer(prose):
        if _is_allowed_decimal(prose, m):
            continue
        findings.append(
            Finding(
                "ERROR",
                "DecimalDump",
                line_of_offset(main_body, m.start()),
                f"Multi-decimal number '{m.group(0)}' in prose; report qualitative magnitude or clean rounded benchmark in prose and keep exact point estimates inside booktabs tables.",
            )
        )

    # Disease 7: chat / revision-history leakage & placeholders (scan full main_body before masking macros)
    clean_full = strip_references_section(main_body)
    for pat in CONTEXT_LEAKAGE_PATTERNS:
        for m in pat.finditer(clean_full):
            findings.append(
                Finding(
                    "ERROR",
                    "ContextLeakage",
                    line_of_offset(main_body, m.start()),
                    f"Chat/revision-history or placeholder leakage ('{m.group(0)}'); manuscript must be 100% standalone.",
                )
            )

    # Advisory WARN checks
    for m in COPULA_AVOIDANCE_RE.finditer(prose):
        findings.append(
            Finding(
                "WARN",
                "CopulaAvoidance",
                line_of_offset(main_body, m.start()),
                f"Inflated copula '{m.group(0)}'; use 'is' or a concrete action verb.",
            )
        )
    for m in VAGUE_ATTRIBUTION_RE.finditer(prose):
        findings.append(
            Finding(
                "WARN",
                "VagueAttribution",
                line_of_offset(main_body, m.start()),
                f"Vague attribution '{m.group(0)}'; cite specific authors with \\citet{{...}}.",
            )
        )
    return findings


def audit_manuscript(text: str, journal: str = "mnsc") -> list[Finding]:
    clean = strip_latex_comments(text)
    main_body, _ec = split_at_ec_switch(clean)

    findings: list[Finding] = []
    findings.extend(audit_abstract(main_body, journal))
    findings.extend(audit_journal_rules(main_body, journal))
    findings.extend(audit_appendix_policy(clean, main_body))
    findings.extend(audit_equation_hygiene(clean, main_body))
    findings.extend(audit_table_hygiene(main_body))
    findings.extend(audit_orphan_symbols(main_body))
    findings.extend(audit_definition_discipline(main_body))
    findings.extend(audit_prose_patterns(main_body, journal))
    findings.sort(key=lambda f: (0 if f.severity == "ERROR" else 1, f.line, f.category))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit an INFORMS LaTeX (.tex) manuscript against hard quality gates."
    )
    parser.add_argument("tex_file", type=Path, help="Path to the .tex manuscript")
    parser.add_argument(
        "--journal",
        choices=("opre", "mnsc", "msom", "ijoc"),
        default="mnsc",
        help="Target INFORMS journal option (default: mnsc)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat WARN findings as blocking exit code 1 as well",
    )
    parser.add_argument(
        "--advisory",
        action="store_true",
        help="Always exit 0 (report findings without blocking)",
    )
    args = parser.parse_args()

    if not args.tex_file.is_file():
        print(f"ERROR: file not found: {args.tex_file}", file=sys.stderr)
        return 2

    raw = args.tex_file.read_text(encoding="utf-8", errors="replace")
    findings = audit_manuscript(raw, journal=args.journal)

    if not findings:
        print(f"PASS: 0 issues found ({args.tex_file.name}, journal={args.journal}).")
        return 0

    errors = sum(1 for f in findings if f.severity == "ERROR")
    warns = sum(1 for f in findings if f.severity == "WARN")
    print(f"AUDIT ({args.tex_file.name}, journal={args.journal}): {errors} ERROR(s), {warns} WARN(s)")
    for f in findings:
        print(f"  [{f.severity}][{f.category}] L{f.line}: {f.message}")

    if args.advisory:
        return 0
    if errors > 0 or (args.strict and warns > 0):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
