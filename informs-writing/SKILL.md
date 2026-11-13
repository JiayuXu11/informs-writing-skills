---
name: informs-writing
description: >-
  Write, structure, rewrite, and polish academic manuscripts in LaTeX (informs4)
  for INFORMS flagship journals: Operations Research (OR), Management Science (MS),
  Manufacturing & Service Operations Management (M&SOM), and INFORMS Journal on
  Computing (IJOC). Use when drafting a paper or section from a core idea via
  exemplar papers (arXiv/SSRN/top-journal PDFs), rewriting drafts to remove AI
  prose patterns, pruning excessive notation and redundant definitions, fixing
  context-blind concepts and revision-history leakage, formatting with informs4.cls
  and Online Appendix conventions, or calibrating manuscripts to OR, MS, M&SOM,
  or IJOC editorial preferences.
---

# INFORMS Flagship Journal Writing & Editing (`informs-writing`)

Write, structure, rewrite, and referee-harden academic manuscripts for **Operations Research (`opre`)**, **Management Science (`mnsc`)**, **Manufacturing & Service Operations Management (`msom`)**, and **INFORMS Journal on Computing (`ijoc`)** in unified `informs4` LaTeX.

---

## Core Operational Principles

1. **Git Version Tracking First**: Before substantive drafting or rewriting, confirm the workspace is Git-initialized with `.gitignore` from [latex-gitignore.txt](./templates/latex-gitignore.txt) (check with `git status`; initialize if needed). Commit clean checkpoints per section or revision pass (e.g., `draft(intro): outline and first pass`, `polish(model): prune unused notation`) so every prose and equation edit is auditable and reversible.
2. **Source-Fidelity & Protected-Regions Contract**: Preserve every factual claim, theorem statement, parameter symbol, assumption label, table number, `\cite{...}`, `\ref{...}`, `\eqref{...}`, and `.tex` macro. Never invent citations, proofs, robustness checks, or fake "humanizer" tics. Treat code, LaTeX math (`$...$`, `\[...\]`, `equation`, `align`), `booktabs` tables, and verbatim quotes as protected regions unless doing an explicit mathematical notation audit.
3. **Silent 4-Pass Discipline (`<= 2` Iterative Passes)**: Diagnose internally and execute cleanly without narrating process steps inside manuscript prose. Stop after at most two focused revision passes per section unless the user requests an additional pass; never over-scrub domain-standard mathematical prose into conversational fluff.
4. **Pure Reader-Facing English**: Target manuscript prose has zero memory of chat prompts, LLMs, or earlier drafts. Never leak meta-commentary (*"Unlike the previous version..."*, *"As requested..."*) or template placeholders (`TODO`, `FIXME`, `[INSERT ...]`) into `.tex` files.
5. **Visual Aesthetics & Compiled-PDF QA**: Never judge typography, tables, or figures from `.tex` source alone. Build crisp `booktabs` tables (`@{}...@{}`, `\arraystretch`, `\cmidrule(lr)`) and vector figures sized for `8–10 pt` labels, compile the PDF whenever a TeX engine is available, run `scripts/check_pdf_layout.py`, and visually inspect flagged pages via `read_file` to catch blank voids, overlaps, margin overflows, or garbled glyphs.

---

## Modes & Reference Routing

Select the primary mode matching the user's request, load **only** the relevant reference modules below, and follow their procedures step-by-step:

| Mode | When to Use | Load These References First |
| :--- | :--- | :--- |
| **Mode A: `0 -> 1` Drafting via Exemplars** | Starting from a core idea, problem, or outline; retrieving legal arXiv/SSRN/faculty-page PDFs to mirror section pacing, sentence-by-sentence Abstract architecture, Abstract/Intro word-count parity (`+/-15%--20%`), theorem-to-prose ratios, and paragraph cadence. | [workflow-write-exemplar.md](./references/workflow-write-exemplar.md), [section-and-lane-architecture.md](./references/section-and-lane-architecture.md), [journals-informs-matrix.md](./references/journals-informs-matrix.md) |
| **Mode B: Anti-AI Rewriting & Prose Surgery** | Polishing an AI-generated or stiff human draft; pruning notation bloat; fixing cold-start concepts, defensive caveats, raw decimal dumping, definition drift, or chat leakage. | [workflow-rewrite-deai.md](./references/workflow-rewrite-deai.md), [human-craft-and-anti-ai.md](./references/human-craft-and-anti-ai.md), [math-notation-and-appendix.md](./references/math-notation-and-appendix.md) |
| **Mode C: Referee Calibration, Contract Audit & Journal Retargeting** | Checking cross-section claim consistency, calibrating evidence verbs, preparing identification specs, converting a working paper for submission, or answering referees. | [manuscript-contract-and-reviewer-calibration.md](./references/manuscript-contract-and-reviewer-calibration.md), [empirical-and-identification-craft.md](./references/empirical-and-identification-craft.md), [journals-informs-matrix.md](./references/journals-informs-matrix.md) |

Supporting resources (cross-mode):
- Visual design standards (tables, vector figures) & compiled-PDF layout triage: [visual-design-and-pdf-qa.md](./references/visual-design-and-pdf-qa.md)
- Master `informs4` LaTeX skeleton (all 4 journals + unified `\ECSwitch`): [informs4-master.tex](./templates/informs4-master.tex)

---

## Seven Hard-Blocked Iron Rules

`scripts/audit_informs_draft.py` enforces these rules as hard-blocking `ERROR` gates (exit code `1`):

1. **Disease 1 — Notation Minimalism & Equation Hygiene**: Define only symbols reused across multiple expressions or carrying substantive economic/operational meaning. Every display equation, subscript, and parameter must earn its keep. Number **only** equations referenced via `\eqref`/`\ref`; use `align*`/`\[...\]` otherwise; forbid `eqnarray`.
2. **Disease 2 — Context-First Introduction**: Never cold-start a technical term, stylized setting, `\begin{definition}`, `\begin{theorem}`, or notation before intuitive motivation and operational meaning in plain English.
3. **Disease 3 — Natural, Cadenced Scholarly English**: Eliminate AI vocabulary clichés (*delve*, *tapestry*, *underscore*, *pivotal*, *moreover/furthermore* crutches), participial tail clauses (`..., thereby enabling...`), Chinglish calques (*with the rapid development of...*), prose em-dashes (`---` / `—`), decorative colon-label bullets, and negative parallelisms (*not merely X, but Y*). Use concrete actor-verb-object sentences.
4. **Disease 4 — Result Confidence (No Defensive Caveats)**: State structural limits cleanly once inside Scope / Model Setup or Future Work. Never undermine a theorem, managerial insight, or empirical finding right after presenting it (*"Although we prove X, this does not fully establish..."*).
5. **Disease 5 — Pattern Prose vs. Table Precision**: Narrate economic mechanisms, orders of magnitude, clean rounded benchmarks (`roughly 1%--2%`, `nearly threefold`), and qualitative comparative statics in prose; keep exact 2--3 decimal point estimates, standard errors, and confidence intervals inside `booktabs` tables (using `threeparttable` + `siunitx`, zero `\hline`, zero vertical `|`).
6. **Disease 6 — Strict Terminology Discipline**: Define each core construct exactly once; use one canonical term and symbol consistently throughout the paper (no synonym cycling across `Abstract`, `Introduction`, `Model`, `Results`, and `Conclusion`).
7. **Disease 7 — Zero Chat / Revision-History Leakage**: Never write *"Unlike the previous draft"*, *"I have corrected"*, *"per reviewer feedback"*, or unfilled bracket/TODO placeholders inside any manuscript file. Keep referee response letters in separate standalone documents.

---

## Two-Layer Journal Baseline & Deltas (`informs4`)

Full specifications live in [journals-informs-matrix.md](./references/journals-informs-matrix.md). Summary baseline + binding journal deltas:

- **Shared Baseline (All 4 Journals)**: Unified `informs4.cls` (`nonblindrev` for review, `blindrev` / double-anonymous where required); **100% Unified Online Appendix (`\ECSwitch`)** with **zero** regular `\appendix` in the main body; `booktabs` + `threeparttable` tables (`\toprule`, `\midrule`, `\bottomrule`); **zero** prose em-dashes (en-dash `--` reserved strictly for numeric/page ranges); calibrated evidence verbs (`characterize`, `establish`, `bound`, `document`, `identify`, `estimate`, `is consistent with`).

| Option | Journal | Abstract & Keywords | Main-Body Length Norm | Appendix & Proof Policy | Editorial Signature & Hard Rules |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `opre` | **Operations Research** | Single-block `\ABSTRACT` + `\SUBJECTCLASS` + `\AREAOFREVIEW` | ~32–36 pp. single-spaced (`<= 35` pp. target incl. refs) | 100% `\ECSwitch` (`Online Appendix EC.x`); pair headline theorems with 3–6 sentence body Proof Sketch | Rigor + surprising methodological or structural payoff; no orphaned formal results |
| `mnsc` | **Management Science** | Single-block `\ABSTRACT` (<= 200 words) + 3–5 lowercase `\KEYWORDS` + `\HISTORY` | <= 32 pp. (`1.5`-spaced `informs4` single-col incl. refs) | 100% `\ECSwitch` | Broad cross-functional significance; Data & Code Disclosure section; clear practical/managerial insight |
| `msom` | **M&SOM** | Mandatory 3-part structured `\ABSTRACT` (`Problem definition`, `Methodology/results`, `Managerial implications`) | <= 32 pp. manuscript | 100% `\ECSwitch` (**16-page target ceiling** for EC) | Endnotes (`\theendnotes`) instead of bottom-of-page `\footnote`; tight end-to-end operations grounding |
| `ijoc` | **INFORMS J. on Computing** | Concise single-block `\ABSTRACT` + problem/computational impact | ~30–35 pp. incl. refs | 100% `\ECSwitch` (`Online Appendix EC.x`); algorithmic complexity + key proof sketch in body | OR + CS fusion; formal `algorithm2e` pseudocode; `.cd` **Dual-DOI** Software & Data companion repo protocol (`INFORMSJoC`) |

---

## Automated Quality Gate (Run Before Every Final Handoff)

Run all three verification scripts from the skill root (or pass full paths to your manuscript `.tex` / text):

1. **Hard LaTeX & AI-Disease Gate** (exits `1` on any hard `ERROR`; pass `--advisory` for non-blocking inspection):
   ```bash
   python scripts/audit_informs_draft.py path/to/main.tex --journal mnsc
   ```
2. **Paragraph Craft, Verb Calibration & Rhythm Check** (supports file path or `stdin`, `--section`, `--strict`):
   ```bash
   python scripts/check_prose_craft.py path/to/section.tex --section intro --strict
   ```
3. **Cross-Section Contract Drift, Exemplar Length Parity & Online Appendix Placement** (`.tex` or `.md`/`.txt`):
   ```bash
   python scripts/audit_manuscript_contract.py path/to/main.tex --journal opre --exemplar-abstract-words 180 --exemplar-intro-words 1450
   python scripts/audit_manuscript_contract.py --place-results items.txt --journal ijoc
   ```
4. **Compiled-PDF Visual Layout, Whitespace & Glyph Gate** (always inspect rendered PNGs via `read_file`):
   ```bash
   python scripts/check_pdf_layout.py path/to/main.pdf --render-flagged /tmp/pdf_qa
   ```

After all source and PDF gates pass cleanly, stage changed `.tex` files and create a descriptive Git commit before delivering the updated manuscript.
