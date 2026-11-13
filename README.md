# INFORMS Flagship Journal Writing & Review Skills (`informs-writing-skills`)

Unified `informs4` LaTeX writing, anti-AI prose surgery, referee calibration, and bilingual PDF review-sync skills for **Operations Research (OR)**, **Management Science (MS)**, **Manufacturing & Service Operations Management (M&SOM)**, and **INFORMS Journal on Computing (IJOC)**.

面向 INFORMS 四大旗舰期刊（OR / MS / M&SOM / IJOC）的学术论文写作、反 AI 化润色、审稿口径校准及英文正文快速中文 PDF 审阅同步技能库。

---

## Included Skills

| Skill | Language | Core Capabilities |
| :--- | :--- | :--- |
| **`informs-writing`** | Pure English | `0 -> 1` exemplar-guided drafting (sentence-by-sentence Abstract imitation, Abstract/Intro word-count parity `+/-15%--20%`, arXiv/SSRN/top-journal PDFs), anti-AI prose surgery & 4-pass editing, publication-grade table/figure aesthetics (`visual-design-and-pdf-qa.md`), hard-blocking source + compiled-PDF visual QA gates, unified `informs4` LaTeX + 100% Unified Online Appendix (`\ECSwitch`), 4-journal deltas, referee calibration |
| **`informs-zh-review`** | EN + ZH | Main-text-only EN -> ZH LaTeX/XeLaTeX PDF generation (with visual PDF layout inspection) + bidirectional PDF annotation extraction & synchronized Git-tracked edits back to both `.tex` files |

---

## Two-Layer Journal Matrix (`informs4`)

All four journals share a common field baseline (**100% Unified Online Appendix `\ECSwitch`**, zero regular `\appendix`, `booktabs` + `threeparttable` tables, zero prose em-dashes, calibrated evidence verbs) plus hard journal-specific deltas:

| `informs4` Option | Journal | Abstract & Metadata Rules | Main-Body & Appendix Rules | Editorial Focus |
| :--- | :--- | :--- | :--- | :--- |
| `opre` | *Operations Research* | `\ABSTRACT` + mandatory `\SUBJECTCLASS` + `\AREAOFREVIEW` | ~32–36 pp. single-spaced; `\ECSwitch` + 3–6 sentence body Proof Sketch per headline theorem | Structural rigor, methodological depth, nontrivial payoff |
| `mnsc` | *Management Science* | `\ABSTRACT` (`< 270` words; check portal limit) + 3–5 lowercase `\KEYWORDS` | <= 32 pp. `1.5`-spaced incl. refs; `\ECSwitch`; Data & Code Disclosure section | Cross-functional breadth, causal/mechanism clarity, practical insight |
| `msom` | *M&SOM* | Mandatory 3-part `\ABSTRACT` (`Problem definition`, `Methodology/results`, `Managerial implications`) | <= 32 pp. manuscript; `\ECSwitch` (**16-page target ceiling**); `\endnote` instead of `\footnote` | Practice-grounded operations modeling & managerial relevance |
| `ijoc` | *INFORMS J. on Computing* | Concise `\ABSTRACT` highlighting algorithmic & computational impact | ~30–35 pp. incl. refs; `\ECSwitch`; `algorithm2e` pseudocode + `.cd` **Dual-DOI** `INFORMSJoC` companion repo | OR + CS fusion, complexity/scalability benchmarks, full reproducibility |

---

## Seven Hard-Blocked Iron Rules (`audit_informs_draft.py`)

`informs-writing/scripts/audit_informs_draft.py` exits with code `1` whenever any rule is violated:

1. **Disease 1 — Notation Minimalism & Equation Hygiene**: Prune one-off/orphan symbols; forbid `eqnarray`; allow numbered equations (`equation`/`align`) **only** when referenced via `\eqref`/`\ref`.
2. **Disease 2 — Context-First Introduction**: Never cold-start a technical term, theorem, or `\begin{definition}` directly after a section heading without plain-English intuition.
3. **Disease 3 — Natural, Cadenced Prose**: Block AI cliché words (*delve*, *tapestry*, *pivotal*, *underscore*), participial tails (`..., thereby enabling...`), Chinglish calques (*with the rapid development of...*), prose em-dashes (`---` / `—`), negative parallelisms, decorative `**Label:**` bullets, and McCloskey verbal bloat.
4. **Disease 4 — Result Confidence**: State scope boundaries once in Setup or Conclusion; block defensive hedges immediately discounting proved results.
5. **Disease 5 — Pattern Prose vs. Table Precision**: Keep mechanisms, qualitative directions, and clean benchmarks (`roughly 1%--2%`) in prose; isolate exact 2–3 decimal point estimates inside `booktabs` tables.
6. **Disease 6 — Strict Terminology Discipline**: Ceiling of `<= 2` formal `\begin{definition}` blocks in main body; zero duplicate definitions or synonym cycling across sections.
7. **Disease 7 — Zero Chat / Revision-History Leakage**: Block `"Unlike the previous version..."`, `"I have fixed..."`, or unfilled `TODO`/`[INSERT]` markers inside manuscript files.

---

## Automated Verification CLI

```bash
# 1. Hard-blocking LaTeX & 7-Disease audit (use --advisory for non-blocking scan)
python informs-writing/scripts/audit_informs_draft.py path/to/main.tex --journal mnsc

# 2. Paragraph craft, evidence-verb calibration, and rhythm/burstiness check
python informs-writing/scripts/check_prose_craft.py path/to/section.tex --section intro --strict

# 3. Cross-section contract drift, Abstract/Intro length parity & Unified Online Appendix placement
python informs-writing/scripts/audit_manuscript_contract.py path/to/main.tex --journal opre --exemplar-abstract-words <N_abs> --exemplar-intro-words <N_intro>
python informs-writing/scripts/audit_manuscript_contract.py --place-results items.txt --journal ijoc

# 4. Compiled-PDF visual layout, whitespace, overlap & glyph integrity audit
python informs-writing/scripts/check_pdf_layout.py path/to/main.pdf --render-flagged /tmp/pdf_qa

# 5. Run full automated unit test suite
python informs-writing/tests/test_informs_skills.py -v
```

---

## Quick Installation

Copy or symlink `informs-writing` and `informs-zh-review` into your agent skills directory (`~/.gemini/config/skills/` by default):

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
