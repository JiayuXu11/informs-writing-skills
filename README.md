# INFORMS Flagship Journal Writing & Review Skills (`informs-writing-skills`)

Unified `informs4` LaTeX writing, anti-AI prose surgery, multi-model blind peer-review iteration, and bilingual PDF review-sync skills for **Operations Research (OR)**, **Management Science (MS)**, **Manufacturing & Service Operations Management (M&SOM)**, and **INFORMS Journal on Computing (IJOC)**.

面向 INFORMS 四大旗舰期刊（OR / MS / M&SOM / IJOC）的学术论文写作、反 AI 化润色、多模型干净上下文盲审迭代提分及英文正文快速中文 PDF 审阅同步技能库。

---

## Included Skills

| Skill | Language | Core Capabilities |
| :--- | :--- | :--- |
| **`informs-writing`** | Pure English | `0 -> 1` exemplar-guided drafting (sentence-by-sentence Abstract imitation, section word-count parity `+/-15%--20%`, arXiv/SSRN/top-journal PDFs), anti-AI prose surgery & 4-pass editing (minimal explanatory parentheticals, trend-first numeric prose, storyline & proposition bridges, front-to-back Abstract/Intro readability), publication-grade table/figure aesthetics (`visual-design-and-pdf-qa.md`), hard-blocking source + compiled-PDF visual QA gates, unified `informs4` LaTeX + 100% Unified Online Appendix (`\ECSwitch`), official 4-journal submission rules |
| **`informs-zh-review`** | EN + ZH | Main-text-only EN -> ZH LaTeX/XeLaTeX PDF generation (with visual PDF layout inspection) + bidirectional PDF annotation extraction & synchronized Git-tracked edits back to both `.tex` files |
| **`informs-review-loop`** | Pure English | Iterative multi-model blind peer-review & selective revision loop for first submissions: spawns diverse clean-context Reviewer agents across distinct model families (e.g., Claude, Gemini, GPT) reading ONLY the compiled PDF, triages feedback by first-submission Impact vs. Effort (`P0/P1/P2/P3`, deferring non-foundational heavy extensions to R&R), recompiles, and loops until **all reviewers >= Major Revision AND >= 1 reviewer >= Minor Revision** |

---

## Two-Layer Journal Matrix (`informs4`)

All four journals share a common field baseline (**100% Unified Online Appendix `\ECSwitch`**, zero regular `\appendix`, `booktabs` + `threeparttable` tables, zero prose em-dashes, calibrated evidence verbs) plus verified official journal-specific submission rules:

| `informs4` Option | Journal | Review & Abstract Rules | Main-Body & Appendix Rules | Editorial Focus & Hard Policies |
| :--- | :--- | :--- | :--- | :--- |
| `opre` | *Operations Research* | **Double-anonymous** (body + EC); single-paragraph `\ABSTRACT` (`<= 200` words, zero math/citations) + `\SUBJECTCLASS` + `\AREAOFREVIEW` | `<= 30` pp. regular / `<= 40` pp. lengthy / `<= 20` pp. Focused Technical & Context/Challenge (double-spaced 11pt, 1-in margins, excl. refs); `\ECSwitch` posted as-is without copyediting + 3–6 sentence body Proof Sketch | High contribution-to-length ratio; structural rigor, methodological depth, nontrivial payoff |
| `mnsc` | *Management Science* | **Double-anonymous**; single-paragraph `\ABSTRACT` (`<= 250` words, zero math/citations) + 3–5 lowercase `\KEYWORDS` | Initial: no hard cap (succinct; DE may reject excessive length). Invited revisions: `<= 32` pp. at `1.5`-spacing (33 lines/p) or `<= 47` pp. double-spaced (25 lines/p), 11pt 1-in margins, excl. EC | Fast Track discontinued; mandatory Data & Code Disclosure + Data Editor check + AsCollected.org URL; USD 79 submission fee (waivers available) |
| `msom` | *M&SOM* | **Double-anonymous** (body + supplement); mandatory 3-part structured `\ABSTRACT` (`<= 300` words: `Problem definition`, `Methodology/results`, `Managerial implications`) | Strictly `<= 32` pp. ALL-INCLUSIVE (refs, tables, figures, in-doc appendices); separate online supplement **`<= 16` pp.** on new submissions; `\endnote` instead of `\footnote` | Practice-grounded operations modeling; COI/related-work & transparent AI-use disclosures |
| `ijoc` | *INFORMS J. on Computing* | **Single-blind (`nonblindrev`)**; single-paragraph `\ABSTRACT` (`< 270`w target, `<= 300`w cap) + 3–5 `\KEYWORDS` | Strictly `<= 25` pp. incl. refs, tables, graphs (+ up to `10` pp. appendices; >2 pp. in online supplement); `algorithm2e` pseudocode + key proof sketch | OR + CS fusion; `INFORMSJoC` GitHub `.cd` **Dual-DOI** companion repo; conference proceedings-extension disclosure |

---

## Seven Hard-Blocked Iron Rules (`audit_informs_draft.py`)

`informs-writing/scripts/audit_informs_draft.py` exits with code `1` whenever any hard rule is violated (plus advisory `WARN` checks for prose craft):

1. **Disease 1 — Notation Minimalism & Equation Hygiene**: Prune one-off/orphan symbols; forbid `eqnarray`; allow numbered equations (`equation`/`align`) **only** when referenced via `\eqref`/`\ref`.
2. **Disease 2 — Context-First Onboarding & Storyline Bridges**: Never cold-start technical terms, paper-specific jargon (especially at first appearance in Abstract/Intro), theorems, or `\begin{definition}` blocks without plain-English intuition; bridge sections and consecutive propositions/theorems along the paper's storyline (`UnbridgedResult` check).
3. **Disease 3 — Natural, Cadenced Prose**: Block AI cliché words (*delve*, *tapestry*, *pivotal*, *underscore*), participial tails (`..., thereby enabling...`), Chinglish calques (*with the rapid development of...*), prose em-dashes (`---` / `—`), negative parallelisms, decorative `**Label:**` bullets, and McCloskey verbal bloat; minimize explanatory parenthetical glosses (`ParentheticalGloss` check).
4. **Disease 4 — Result Confidence**: State scope boundaries once in Setup or Conclusion; block defensive hedges immediately discounting proved results.
5. **Disease 5 — Trend-First Prose vs. Table/Figure Precision**: Narrate qualitative trends, regime crossovers, and mechanisms with at most 1–2 rounded headline anchors per paragraph—never transcribe tables or figures point by point (`NumericClutter` + `DecimalDump` checks); keep exact estimates inside `booktabs` tables and figures.
6. **Disease 6 — Strict Terminology Discipline**: Ceiling of `<= 2` formal `\begin{definition}` blocks in main body; zero duplicate definitions or synonym cycling across sections.
7. **Disease 7 — Zero Chat / Revision-History Leakage**: Block `"Unlike the previous version..."`, `"I have fixed..."`, or unfilled `TODO`/`[INSERT]` markers inside manuscript files.

---

## Automated Verification CLI

```bash
# 1. Hard-blocking LaTeX & 7-Disease audit (use --advisory for non-blocking scan)
python informs-writing/scripts/audit_informs_draft.py path/to/main.tex --journal mnsc

# 2. Paragraph craft, evidence-verb calibration, parenthetical gloss & numeric clutter check
python informs-writing/scripts/check_prose_craft.py path/to/section.tex --section intro --strict

# 3. Cross-section contract drift, Abstract/Intro length parity & Unified Online Appendix placement
python informs-writing/scripts/audit_manuscript_contract.py path/to/main.tex --journal opre --exemplar-abstract-words <N_abs> --exemplar-intro-words <N_intro>
python informs-writing/scripts/audit_manuscript_contract.py --place-results items.txt --journal ijoc

# 4. Compiled-PDF visual layout, whitespace, overlap & glyph integrity audit
python informs-writing/scripts/check_pdf_layout.py path/to/main.pdf --render-flagged /tmp/pdf_qa

# 5. Evaluate a multi-model blind peer-review round & check stopping criterion
python informs-review-loop/scripts/evaluate_review_round.py path/to/review_loop --round 1

# 6. Run full automated unit test suites
python informs-writing/tests/test_informs_skills.py -v
python informs-review-loop/tests/test_review_loop.py -v
```

---

## Quick Installation

Copy or symlink `informs-writing`, `informs-zh-review`, and `informs-review-loop` into your agent skills directory (`~/.gemini/config/skills/` by default):

### Windows (PowerShell)

```powershell
.\scripts\install.ps1
```

### macOS / Linux

```bash
bash scripts/install.sh
```

Or pass a custom target path as the first argument to either script.

---

## Acknowledgments

This skill suite synthesizes best practices and structural inspirations from:
- [hanlulong/econ-writing-skill](https://github.com/hanlulong/econ-writing-skill) (notation minimalism, `booktabs` + `siunitx` table discipline, Cochrane/McCloskey craft, identification blueprints, referee responses)
- [iik1/academic_writing_skills](https://github.com/iik1/academic_writing_skills) (two-layer Field Baseline + 4-Journal Deltas architecture, AI cliché cleaning)
- [jmf-enigma/or-ms-writing-skill](https://github.com/jmf-enigma/or-ms-writing-skill) (calibrated evidence verbs, concrete noun anchors, `check_paragraph` / manuscript contract audit design, reviewer calibration)
- [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) (source-fidelity editing contract, protected regions, negative parallelism / copula / rhythm heuristics)
