#!/usr/bin/env python3
"""Paragraph craft, evidence-verb calibration, and AI-scent analyzer for INFORMS prose.

Supports plain text, Markdown, or LaTeX passages via file path or stdin (`-`).
Checks evidence-verb calibration, unanchored overloaded terms, noun piles,
preposition/`of` chains, weak abstract subjects, naked `This` openers,
rhythm/burstiness uniformity, negative parallelism, false concessions,
copula avoidance, synonym drift, and AI prose tells.
"""
from __future__ import annotations

import argparse
import math
import re
import sys
from pathlib import Path
from typing import NamedTuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


class CraftIssue(NamedTuple):
    severity: str  # ERROR | WARN
    category: str
    location: str
    message: str


OVERLOADED_TERMS = {
    "identification",
    "endogeneity",
    "efficiency",
    "equilibrium",
    "heterogeneity",
    "robustness",
    "mechanism",
    "welfare",
    "channel",
    "selection",
    "tractability",
}

ANCHOR_WORDS = {
    # Actors
    "firm", "firms", "seller", "sellers", "buyer", "buyers", "platform", "platforms",
    "worker", "workers", "driver", "drivers", "hospital", "hospitals", "patient",
    "patients", "supplier", "suppliers", "retailer", "retailers", "manufacturer",
    "carrier", "dispatcher", "planner", "manager", "managers", "customer", "customers",
    "agent", "agents", "bidder", "bidders",
    # Decisions & operational levers
    "price", "prices", "pricing", "inventory", "stock", "capacity", "schedule",
    "scheduling", "routing", "dispatch", "matching", "allocation", "ordering",
    "order", "bid", "bids", "wage", "wages", "fee", "fees", "commission", "lead",
    "replenishment", "cutoff", "batching", "entry", "exit", "disclosure",
    # Frictions & formal/empirical anchors
    "delay", "congestion", "shortage", "stockout", "queue", "waiting", "variance",
    "uncertainty", "cost", "costs", "margin", "profit", "surplus", "welfare",
    "instrument", "Variation", "variation", "shock", "experiment", "rct", "theorem",
    "proposition", "lemma", "corollary", "algorithm", "bound", "data", "sample",
    "regression", "estimator", "panel", "fixed", "effect", "effects",
}

ABSTRACT_NOUN_SUFFIX_RE = re.compile(
    r"^[a-z]{4,}(?:tion|sion|ment|ness|ity|ance|ence|ship|ism)$", re.IGNORECASE
)

PREPOSITIONS = {
    "of", "in", "on", "for", "to", "with", "by", "from", "through", "between",
    "among", "under", "over", "via", "across", "within", "without", "toward",
    "towards", "against", "into", "onto",
}

NAKED_THIS_RE = re.compile(
    r"^(?:This|That|These)\s+(?:shows|suggests|indicates|demonstrates|proves|"
    r"establishes|implies|reveals|confirms|highlights|means|leads|results|"
    r"creates|causes|enables|allows)\b",
    re.IGNORECASE,
)

WEAK_SUBJECT_RE = re.compile(
    r"^(?:There (?:is|are|exist|exists)|It is (?:important|worth|clear|interesting|notable|evident) (?:to note )?that|"
    r"The (?:present )?(?:paper|study|model|analysis|approach|framework) (?:provides|presents|offers|exhibits|achieves))\b",
    re.IGNORECASE,
)

COPULA_AVOIDANCE_RE = re.compile(
    r"\b(?:serves as an?|stands as an?|functions as an?|acts as an?)\b",
    re.IGNORECASE,
)

NEG_PARALLEL_RE = re.compile(
    r"\bnot\s+(?:only|merely|simply|just)\b[^.!?\n]{1,100}\bbut\s+(?:also\b)?",
    re.IGNORECASE,
)

FALSE_CONCESSION_RE = re.compile(
    r"\b(?:certainly|admittedly|undeniably|to be sure)\b[^.!?\n]{1,90}\b(?:yet|however|nonetheless|nevertheless)\b",
    re.IGNORECASE,
)

PROSE_EM_DASH_RE = re.compile(r"(?<!-)---(?!-)|—")

ADJ_TRIPLET_RE = re.compile(
    r"\b[a-z]{4,}(?:al|ive|ic|ous|ary|ory)\s*,\s*[a-z]{4,}(?:al|ive|ic|ous|ary|ory)\s*(?:,\s*)?and\s+[a-z]{4,}(?:al|ive|ic|ous|ary|ory)\b",
    re.IGNORECASE,
)

SYNONYM_DRIFT_GROUPS = [
    ("buyer-term", ["customer", "consumer", "buyer", "end-user", "client"]),
    ("platform-term", ["platform", "marketplace", "intermediary"]),
    ("firm-term", ["firm", "company", "enterprise", "organization"]),
    ("solver-term", ["algorithm", "heuristic", "solver", "procedure", "routine"]),
]

CHINGLISH_RE = re.compile(
    r"\b(?:with the (?:rapid )?(?:development|growth|rise) of|"
    r"under the background of|"
    r"it is worth mentioning that|"
    r"plays? an? (?:important|vital|pivotal|key) role in|"
    r"more and more)\b",
    re.IGNORECASE,
)


def clean_text_for_prose(raw: str) -> str:
    """Strip LaTeX comments, display math, tables, and commands to leave readable prose."""
    lines = []
    for ln in raw.splitlines():
        m = re.search(r"(?<!\\)%", ln)
        lines.append(ln[: m.start()] if m else ln)
    txt = "\n".join(lines)
    txt = re.sub(
        r"\\begin\{(equation\*?|align\*?|tabular\*?|tabularx|algorithm\*?|algorithm2e)\}.*?\\end\{\1\}",
        " ",
        txt,
        flags=re.DOTALL,
    )
    txt = re.sub(r"\$\$.*?\$\$|\\\[.*?\\\]", " ", txt, flags=re.DOTALL)
    txt = re.sub(r"(?<!\\)\$[^$\n]+?(?<!\\)\$", " Xmath ", txt)
    txt = re.sub(r"\\(?:cite[tp]?|citeal[tp]|eqref|ref|cref|Cref|label)\{[^}]*\}", " [Ref] ", txt)
    txt = re.sub(r"\\(?:section|subsection|subsubsection|paragraph)\*?\{([^}]*)\}", r"\n\n\1.\n", txt)
    txt = re.sub(r"\\(?:textbf|textit|emph|text)\{([^}]*)\}", r"\1", txt)
    txt = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?", " ", txt)
    txt = re.sub(r"[{}]", " ", txt)
    return txt


def split_paragraphs(txt: str) -> list[str]:
    paras = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", txt)]
    return [p for p in paras if len(p.split()) >= 5]


def split_sentences(para: str) -> list[str]:
    # Protect common abbreviations before splitting
    safe = re.sub(
        r"\b(Fig|Eq|Sec|Tab|Thm|Prop|Cor|App|al|e\.g|i\.e|vs|Dr|Prof)\.",
        r"\1<DOT>",
        para,
    )
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\[])", safe)
    return [p.replace("<DOT>", ".").strip() for p in parts if len(p.split()) >= 2]


def analyze_prose(raw: str, section: str = "paragraph") -> list[CraftIssue]:
    issues: list[CraftIssue] = []

    # Pre-cleaning checks for prose em-dash (outside % comments / math)
    nocomment = "\n".join(
        ln[: re.search(r"(?<!\\)%", ln).start()] if re.search(r"(?<!\\)%", ln) else ln
        for ln in raw.splitlines()
    )
    nomath = re.sub(r"\$\$.*?\$\$|\\\[.*?\\\]|(?<!\\)\$[^$\n]+?(?<!\\)\$", " ", nocomment, flags=re.DOTALL)
    for m in PROSE_EM_DASH_RE.finditer(nomath):
        ln_no = nomath.count("\n", 0, m.start()) + 1
        issues.append(
            CraftIssue(
                "ERROR",
                "EmDash",
                f"L{ln_no}",
                "Prose em-dash ('---' or '—') forbidden; rewrite cleanly with commas, colons, or split sentences.",
            )
        )

    cleaned = clean_text_for_prose(raw)
    paras = split_paragraphs(cleaned)
    all_words_lower = re.findall(r"\b[a-z][a-z-]+\b", cleaned.lower())

    # Whole-passage synonym-drift check
    for fam, terms in SYNONYM_DRIFT_GROUPS:
        used = [t for t in terms if all_words_lower.count(t) >= 1]
        if len(used) >= 3:
            issues.append(
                CraftIssue(
                    "WARN",
                    "SynonymDrift",
                    "passage",
                    f"Rotating {fam} synonyms {used}; pick one canonical term and use it consistently.",
                )
            )

    # Whole-passage Chinglish check
    for m in CHINGLISH_RE.finditer(cleaned):
        issues.append(
            CraftIssue(
                "ERROR",
                "Chinglish",
                "passage",
                f"Chinglish phrasing '{m.group(0)}'; replace with concrete operational English.",
            )
        )

    for p_idx, para in enumerate(paras, start=1):
        loc = f"P{p_idx}"
        para_tokens = set(re.findall(r"\b[a-zA-Z]+\b", para.lower()))

        # Overloaded terms without nearby concrete anchor
        for term in sorted(OVERLOADED_TERMS):
            if term in para_tokens and not (para_tokens & {w.lower() for w in ANCHOR_WORDS}):
                issues.append(
                    CraftIssue(
                        "WARN",
                        "UnanchoredTerm",
                        loc,
                        f"Overloaded term '{term}' appears without a concrete actor, decision, friction, or data anchor in the paragraph.",
                    )
                )

        # Negative parallelism, false concessions, copula avoidance, triplets
        for m in NEG_PARALLEL_RE.finditer(para):
            issues.append(
                CraftIssue(
                    "ERROR",
                    "NegParallel",
                    loc,
                    f"Formulaic negative parallelism ('{m.group(0)}'); state the claim directly.",
                )
            )
        for m in FALSE_CONCESSION_RE.finditer(para):
            issues.append(
                CraftIssue(
                    "WARN",
                    "FalseConcession",
                    loc,
                    f"Rhetorical false concession ('{m.group(0)}'); cut throat-clearing and state the mechanism cleanly.",
                )
            )
        for m in COPULA_AVOIDANCE_RE.finditer(para):
            issues.append(
                CraftIssue(
                    "WARN",
                    "CopulaAvoidance",
                    loc,
                    f"Inflated copula '{m.group(0)}'; use 'is' or a concrete action verb.",
                )
            )
        for m in ADJ_TRIPLET_RE.finditer(para):
            issues.append(
                CraftIssue(
                    "WARN",
                    "AdjectiveTriplet",
                    loc,
                    f"Decorative adjective triplet ('{m.group(0)}'); keep at most one high-information modifier.",
                )
            )

        sents = split_sentences(para)
        sent_lengths: list[int] = []
        openers: list[str] = []

        for s_idx, sent in enumerate(sents, start=1):
            sloc = f"{loc}.S{s_idx}"
            words = re.findall(r"\b[A-Za-z][A-Za-z'-]*\b", sent)
            sent_lengths.append(len(words))
            if words:
                openers.append(words[0].lower())

            lower_sent = sent.lower()

            # Evidence-verb calibration (empirical data vs theorem)
            if section in {"results", "intro", "paragraph"}:
                has_empirical = bool(
                    re.search(r"\b(data|sample|regression|estimate|estimates|survey|empirical|panel|dataset)\b", lower_sent)
                )
                has_theorem = bool(re.search(r"\b(theorem|proposition|lemma|corollary|proof)\b", lower_sent))
                if has_empirical and not has_theorem and re.search(r"\b(proves?|guarantees?|conclusively establishes?)\b", lower_sent):
                    issues.append(
                        CraftIssue(
                            "ERROR",
                            "EvidenceCalibration",
                            sloc,
                            "Do not use deductive math verbs ('prove', 'guarantee') for empirical estimates; use 'document', 'estimate', 'identify', or 'is consistent with'.",
                        )
                    )

            # Naked 'This' opener
            if NAKED_THIS_RE.match(sent):
                issues.append(
                    CraftIssue(
                        "WARN",
                        "NakedThis",
                        sloc,
                        "Naked 'This/That/These <verb>' opener leaves the referent ambiguous; insert a concrete noun ('This capacity bound implies...').",
                    )
                )

            # Weak abstract subject
            if WEAK_SUBJECT_RE.match(sent):
                issues.append(
                    CraftIssue(
                        "WARN",
                        "WeakSubject",
                        sloc,
                        "Abstract/expletive opener ('There is...', 'It is important...', 'The model provides...'); promote the concrete actor or variable to subject.",
                    )
                )

            # 3+ consecutive abstract noun pile
            streak = 0
            pile_tokens: list[str] = []
            for w in words:
                if ABSTRACT_NOUN_SUFFIX_RE.match(w):
                    streak += 1
                    pile_tokens.append(w)
                    if streak >= 3:
                        issues.append(
                            CraftIssue(
                                "WARN",
                                "AbstractNounPile",
                                sloc,
                                f"Abstract noun cluster ({' '.join(pile_tokens[-3:])}); unpack with active verbs.",
                            )
                        )
                        break
                else:
                    streak = 0
                    pile_tokens = []

            # Preposition density & 'of' chains
            prep_count = sum(1 for w in words if w.lower() in PREPOSITIONS)
            of_chain = re.findall(r"\bof\s+(?:the\s+|a\s+|an\s+)?[a-z-]+\s+of\s+(?:the\s+|a\s+|an\s+)?[a-z-]+\s+of\b", lower_sent)
            if prep_count >= 7 or of_chain:
                issues.append(
                    CraftIssue(
                        "WARN",
                        "PrepositionChain",
                        sloc,
                        f"Dense prepositional nesting ({prep_count} prepositions); break into two crisp clauses.",
                    )
                )

        # Paragraph rhythm & burstiness check
        if len(sent_lengths) >= 4:
            mean_len = sum(sent_lengths) / len(sent_lengths)
            if mean_len > 0:
                stdev = math.sqrt(sum((x - mean_len) ** 2 for x in sent_lengths) / len(sent_lengths))
                cv = stdev / mean_len
                if cv < 0.20:
                    issues.append(
                        CraftIssue(
                            "WARN",
                            "LowBurstiness",
                            loc,
                            f"Uniform robotic sentence cadence (lengths={sent_lengths}, CV={cv:.2f}); vary short punchy verdicts with analytical sentences.",
                        )
                    )

        # Same-opener 3-run
        for i in range(len(openers) - 2):
            if openers[i] == openers[i + 1] == openers[i + 2]:
                issues.append(
                    CraftIssue(
                        "WARN",
                        "RepetitiveOpeners",
                        loc,
                        f"Three consecutive sentences start with '{openers[i]}'; vary sentence openings.",
                    )
                )
                break

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analyze paragraph craft, verb calibration, and AI-writing rhythm."
    )
    parser.add_argument("input", help="Path to text/.tex file or '-' for stdin")
    parser.add_argument(
        "--section",
        choices=("intro", "related", "model", "results", "conclusion", "paragraph"),
        default="paragraph",
        help="Section context for verb calibration (default: paragraph)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 if any ERROR or WARN issue is found",
    )
    parser.add_argument(
        "--advisory",
        action="store_true",
        help="Always exit 0 even when ERRORs are present",
    )
    args = parser.parse_args()

    if args.input == "-":
        raw = sys.stdin.read()
        label = "<stdin>"
    else:
        p = Path(args.input)
        if not p.is_file():
            print(f"ERROR: file not found: {p}", file=sys.stderr)
            return 2
        raw = p.read_text(encoding="utf-8", errors="replace")
        label = p.name

    issues = analyze_prose(raw, section=args.section)
    if not issues:
        print(f"PASS: 0 craft issues in {label} (section={args.section}).")
        return 0

    errs = sum(1 for i in issues if i.severity == "ERROR")
    warns = sum(1 for i in issues if i.severity == "WARN")
    print(f"CRAFT ({label}, section={args.section}): {errs} ERROR(s), {warns} WARN(s)")
    for i in issues:
        print(f"  [{i.severity}][{i.category}] {i.location}: {i.message}")

    if args.advisory:
        return 0
    if errs > 0 or (args.strict and warns > 0):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
