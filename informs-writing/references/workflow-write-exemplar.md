# Workflow A: Exemplar-Guided Paper Writing (`0 -> 1`)

Use this workflow when drafting a new paper, abstract, introduction, model, or empirical/computational section from a **core idea, rough notes, model formulation, or theorem/empirical outline**.

Never write an INFORMS paper from generic LLM instincts. Anchor the macro flow, paragraph roles, and syntactic cadence in 2–3 closely matched target-journal papers before writing LaTeX, and apply Cochrane's **Triangular Lead** (put the finding upfront, draft Abstract LAST from the finished Introduction).

---

## Step 1: Lock the Paper Spine & Lane (5-Minute Alignment)

Before searching or drafting, confirm these anchors with the user (skip only items already specified):
1. **Target Journal**: `opre`, `mnsc`, `msom`, or `ijoc` (loads exact deltas from [journals-informs-matrix.md](./journals-informs-matrix.md)).
2. **Research Lane**: Select matching blueprint from [section-and-lane-architecture.md](./section-and-lane-architecture.md) (analytical theory, applied DP/OR, algorithm/`ijoc` software, online learning, archival DiD/IV/RDD, field/lab experiment, construct measurement, or structural counterfactual).
3. **Core Tension / Bottleneck**: What real operational friction, identification threat, or mathematical obstacle breaks incumbent practice?
4. **Central Object & Spine Results**: The one portable formal/empirical object and 1–3 headline theorems, policies, algorithms, or treatment effects.
5. **Primary Benchmark / Comparator**: First-best, myopic/static rule, fluid limit, commercial MIP solver, or control group.

---

## Step 2: Exemplar Discovery & Open-Access PDF Retrieval

Locate 2–3 recent published papers (last 5–8 years) in the **target journal** and **matching lane**.

1. Search INFORMS PubsOnline / Google Scholar metadata via `search_web`.
2. When the published PDF is paywalled, legally fetch the open-access working paper / preprint PDF:
   - `"<Exact Paper Title>" site:arxiv.org`
   - `"<Exact Paper Title>" site:ssrn.com`
   - `"<Exact Paper Title>" filetype:pdf`
   - `"<Author Last Name>" "<Short Title>" pdf` (author faculty homepages)
   Also read any local exemplar PDFs supplied by the user.
3. **Read Targeted Sections**: Inspect the exact sections matching what you are drafting (e.g., Intro + Model Setup) via `read_file` or PyMuPDF (`fitz`). Record verified claims only (follow Citation Close-Reading rules in [section-and-lane-architecture.md](./section-and-lane-architecture.md)).

---

## Step 3: Multi-Level Extraction (Structure, Cadence, Boundaries)

Extract three layers from the exemplars before touching `.tex`:

### Layer 1: Macro Architecture & Online Appendix Split
- Section sequence, subsection depth, where Related Literature lives (§1.2 vs §2), and what proofs/logs move to `Online Appendix EC.x`.
- Target length allocation (remember `opre` <= 30 pp excl. refs, `mnsc` <= 32 pp at 1.5x, `msom` <= 32 pp ALL-INCLUSIVE + 16 pp EC, `ijoc` <= 25 pp).

### Layer 2: Paragraph-by-Paragraph Role Blueprint
Build a compact blueprint mapping the exemplars' argument dependency onto the user's Paper Spine (do NOT force every paragraph into an identical 5-part formula; match the passage's actual burden):

| Para # | Primary Burden | Opening Anchor / Subject | Core Move / Warrant | Notation Cap | Closing Landing |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P1 | Concrete setting & friction | Real operator, firm, or system | Why current rule fails | **0 symbols** | Crisp operational question or tension |
| P2 | Stream gap / technical hurdle | Prior stream or benchmark | What existing analysis omits | **0 symbols** | Why the gap is non-trivial |
| P3 | Research question & setup | `We study...` / `We ask...` | Object, lever, design, benchmark | **0–1 scalar** | Preview of core trade-off & finding |
| ... | ... | ... | ... | ... | ... |

### Layer 3: Syntactic Cadence & Sentence Skeletons (Taste & Boundaries)
Steal the **grammatical skeleton and rhythm**, never content phrasing:
- *Setting & Friction*: *"In many [systems], [actor] chooses [decision] before observing [shock]."*
- *Cross-Stream Positioning*: *"[Stream A] characterizes [X] under [condition], whereas [our setting] introduces [Y]."*
- *Concept Onboarding*: *"In [setting], [difficulty] arises because [reason]. To address this, we say a policy is [term] if [intuition/formula]."*
- *Result Packaging*: *"When [condition holds], Theorem 1 establishes that [policy] reduces [metric] by roughly [magnitude] relative to [benchmark] (Table 2)."*
- *Display Framing*: *"The objective in (1) balances immediate [A] against expected future [B]."*

**Guardrails**: Never copy unique content strings (>= 8 content words), unverified citations, or a living scholar's personal catchphrases; keep prose concrete and calm.

---

## Step 4: Blueprint Approval -> Section-by-Section LaTeX Drafting

1. **Confirm Blueprint First**: Show the concise Layer 2 table (plus planned Section Headings) to the user for quick alignment unless the user explicitly asked to draft directly.
2. **Draft in `informs4` LaTeX**:
   - Base on [informs4-master.tex](./templates/informs4-master.tex) (`informs4` + `natbib` + `informs2014` + `booktabs` + `threeparttable`).
   - Draft the **Introduction early**, revise as the body sharpens, and extract/polish the **Abstract LAST** so zero contract drift occurs between Abstract, Body, and Conclusion.
   - Enforce **all 7 Iron Rules**: zero orphan symbols, Just-in-Time symbol naming, unreferenced displays unnumbered, 4-beat onboarding before unfamiliar concepts, concrete SVO + calibrated verbs, positive upfront scope (zero defensive caveats), rounded patterns in prose + 2-decimal precision in `booktabs` tables, one locked canonical term per concept (`<= 2` formal `\begin{definition}` blocks), and timeless standalone prose.
   - Enforce **100% Unified Online Appendix (`\ECSwitch`)**: Zero regular `\appendix`; draft complete proofs/helper lemmas/secondary tables cleanly under `\ECSwitch` + `\ECHead{...}` (respecting M&SOM's 16-page cap), and give every `opre`/`ijoc` headline theorem a 3–6 sentence body Proof Sketch.

---

## Step 5: Automated Gate Check, Contract Verification & Git Commit

1. Run pre-flight `git status` if not already tracked, then run the hard-blocking LaTeX audit:
   ```bash
   python "<skill_dir>/scripts/audit_informs_draft.py" <manuscript.tex> --journal <opre|mnsc|msom|ijoc>
   ```
2. For full-paper drafts, also run cross-section contract drift check:
   ```bash
   python "<skill_dir>/scripts/audit_manuscript_contract.py" <manuscript.tex> --journal <opre|mnsc|msom|ijoc>
   ```
3. Fix every flagged error or warning, verify clean exit code `0`, and commit atomically:
   `git add <core_tex_and_bib> && git commit -m "draft(<section>): write <section> aligned with <journal> exemplars"`
