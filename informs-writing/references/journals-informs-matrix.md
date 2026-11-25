# INFORMS Field Baseline & Four-Journal Matrix (`opre`, `mnsc`, `msom`, `ijoc`)

Use this two-layer reference whenever calibrating a manuscript's framing, voice, section architecture, abstract, metadata, or page budget to INFORMS flagship journals:
1. **Part I (Shared INFORMS Field Baseline)** establishes the common ABS 4*/4 OR/MS norms across all four journals.
2. **Part II (Four-Journal Deltas)** records ONLY the `[ENFORCED]` hard constraints and `[PRACTICE]` editorial inclinations where **Operations Research (`opre`)**, **Management Science (`mnsc`)**, **M&SOM (`msom`)**, or **IJOC (`ijoc`)** diverge. Journal deltas override the field baseline wherever they conflict.

All four journals share `informs4.cls`, `informs2014.bst`, `(Author Year)` `natbib` citations with zero comma between surname and year, and this skill's **100% Unified Online Appendix** rule (`\ECSwitch` + `\ECHead`, referenced as `Online Appendix EC.1`, etc.).

---

## Part I: Shared INFORMS Field Baseline

### 1. Canonical Macro Architecture
INFORMS papers do NOT share a single mandatory template; section structure follows the paper's evidence lane:
- **Analytical / Theory**: `Introduction` (motivation, gap, contributions, roadmap) -> `Model Setup` -> `Analysis & Main Results` (or problem-specific thematic sections) -> `Extensions` -> `Numerical Study` (optional) -> `Conclusion` -> `References` -> `Online Appendix (\ECSwitch)`.
- **Computational / Algorithmic**: `Introduction` -> `Problem Formulation` -> `Structural Properties` -> `Algorithm Design` -> `Computational Experiments` -> `Conclusion` -> `References` -> `Online Appendix (\ECSwitch)`.
- **Empirical / Experimental**: `Introduction` -> `Institutional Setting & Conceptual Framework` -> `Data & Empirical Strategy` -> `Main Results` -> `Mechanisms & Robustness` -> `Discussion & Conclusion` -> `References` -> `Online Appendix (\ECSwitch)`.

Related Literature lives either inside Section 1 (typical for OR and empirical/applied MS) or as a standalone Section 2 (common in dense theory). A separate free-standing `Discussion` section is rare in analytical OR/MS; interpretive discussion integrates beside results or inside the Conclusion.

### 2. Voice, Person & Verb Tense
- **Authorial Voice**: Use first-person plural **active `"we"`** (`"we study"`, `"we characterize"`, `"we estimate"`) throughout problem framing, modeling choices, algorithms, and interpretation. Reserve passive voice strictly for procedural data/sampling steps where the actor is irrelevant (`"observations were restricted to..."`, `"standard errors are clustered at..."`).
- **Tense Convention**:
  - **Timeless Present**: Problem setup, definitions, algorithm steps, formal theorem statements, literature results (`"Cachon and Swinney (2011) show..."`), and analytical interpretation.
  - **Simple Past**: Execution of empirical data collection, sample construction, field experiments, and estimation runs (`"we collected"`, `"we randomly assigned"`, `"we trained"`).
- **Zero Throat-Clearing**: Never open Section 1 with `"In recent years, there has been growing interest in..."` or `"With the advent of..."`. Open immediately with the operational decision, institutional puzzle, or formal bottleneck.

### 3. Argumentation & Literature Engagement
- **Introduction Progression (CARS Model)**:
  1. *Establish Territory*: Concrete operational, economic, or computational phenomenon (anchor in a named system, friction, or puzzle).
  2. *Establish Niche*: Synthesize prior streams and show where existing models, proofs, or designs break down or disagree. Frame prior work generously (`"While X characterizes Y under full information, it abstracts from..."`) rather than adversarially.
  3. *State Research Question*: Crisp question or objective within the first 2–3 paragraphs.
  4. *Preview Credibility & Findings*: Summarize main theorems/estimates with clean qualitative mechanisms and rounded orders of magnitude (Cochrane's triangular lead: never bury the main finding on page 20).
  5. *Position Contributions*: Enumerate 2–3 genuinely distinct contributions (theoretical, methodological, empirical, managerial) and end with a concise landmark roadmap only if helpful.
- **Citation Density Curve & Paraphrase Norm**:
  - *Intro / Related Work*: High citation density, organized conceptually by **research stream** (never a chronological `"Smith (2018) showed X. Jones (2020) showed Y."` list).
  - *Model / Methods*: Moderate density citing established formulations, estimators, and identification precedents.
  - *Results / Proofs*: Minimal external citations; self-referential.
  - **Zero Direct Quotations**: OR/MS cites strictly by paraphrase and positioning; direct block quotes are absent.
  - **Formatting**: `(Author Year)` or `Author (Year)`; multiple citations separated by commas `(Levi et al. 2015, Besbes and Zeevi 2020)`.
- **Length & Exemplar Calibration**: Enforce exact journal Abstract ceilings (**`<= 200` words for `opre`**, **`<= 250` words for `mnsc`**, **`<= 300` words for `msom`** structured abstract, and **`< 270` words** generally for `ijoc`) and keep the compiled **Introduction `<= 3` pages**, using the word counts of corresponding sections in recent target-journal exemplars as your primary reference.

### 4. Subgenre-Calibrated Epistemic Caution
- **Theoretical / Mathematical Claims**: Verbal hedges (`might`, `seems`, `perhaps`) do NOT belong in theorem exposition. Express qualification strictly via explicit assumptions, parameter regimes, and comparators (`"Under Assumption 2, Proposition 1 establishes..."`).
- **Empirical / Applied Claims**: State identified ITT/ATT/LATE estimates directly, reserve `"suggests"` / `"is consistent with"` for non-uniquely identified channels, and qualify external validity concretely (`"within our partnering fulfillment centers"`). Use `"to the best of our knowledge"` only when asserting a genuinely first formal treatment, never as filler.

---

## Part II: Four-Journal Hard Constraints & Editorial Deltas

### 1. Operations Research (`opre`)

#### Editorial Inclination & Reviewer Mindset
- **Core question referees ask**: *"What is mathematically or methodologically non-trivial here, and why do existing formulations, bounds, or proof techniques fall short?"*
- **Voice & Framing**: Rigorous, crisp, method-forward. Do not pad the Introduction with generic business-school rhetoric. Lead with the structural, stochastic, optimization, queueing, game-theoretic, or algorithmic hurdle and let the formal object carry the paper.

#### Enforced Constraints (`[ENFORCED]`) & Practice Norms (`[PRACTICE]`)
- `[ENFORCED]` **Template, Class & Formatting**: Official INFORMS LaTeX template (`\documentclass[opre,dblanonrev]{informs4}`, or legacy `informs3.cls` / Overleaf *"Template for Operations Research"* with `opre` option), **11pt font, double-spaced (`\DoubleSpacedXI`), 1-inch margins**, with built-in main-text + E-Companion (`\ECSwitch`) support. Submit online via *Operations Research* ScholarOne Manuscripts (`https://pubsonline.informs.org/page/opre/submission-guidelines`).
- `[ENFORCED]` **Page Limits (Strict Contribution-to-Length Ratio)**: Editors evaluate contribution-to-length strictly; manuscripts exceeding limits are considered only in extraordinary circumstances:
  - **Regular Manuscripts**: **`<= 30` pages** (excluding references).
  - **Lengthy Manuscripts**: **`<= 40` pages** (excluding references; typically slower review).
  - **Focused Technical Papers**: **`<= 20` pages** (excluding references).
  - **Context and Challenge Papers**: **`<= 20` pages**.
  Move long proofs, supplementary data, and technical details into the **Electronic Companion (E-Companion / Online Appendix)** instead of overflowing main-body page limits.
- `[ENFORCED]` **Abstract**: Strictly **1 single paragraph**, **`<= 200` words**, **zero mathematical formulas/symbols**, and **zero citations**.
- `[ENFORCED]` **Double-Anonymous (Double-Blind) Submission**: Initial submissions MUST fully anonymize **both the main manuscript and the E-Companion**. Remove author names, affiliations, acknowledgments, funding/grant details, and identifying first-person self-citations (cite your own prior work neutrally in the third person).
- `[ENFORCED]` **E-Companion Camera-Ready Policy**: Upon acceptance, INFORMS publishes the E-Companion online directly as the author-submitted PDF **without copyediting or re-typesetting**; ensure clean final layout, spacing, and typography before submission.
- `[ENFORCED]` **Generative AI Policy**: AI tools cannot be listed as authors and cannot be used for peer review or editorial decisions (reviewers and editors remain bound by strict confidentiality).
- `[ENFORCED]` **Post-Abstract Metadata Block** (in exact order before `\maketitle`):
  1. `\KEYWORDS{...}`
  2. `\SUBJECTCLASS{...}` using official INFORMS OR/MS taxonomy in lowercase (e.g., `inventory/production: stochastic; dynamic programming: Markov`)—never substitute JEL codes.
  3. `\AREAOFREVIEW{...}` using an official OR area (e.g., `Operations and Supply Chains`, `Optimization`, `Revenue Management`).
- `[PRACTICE]` **Section Numbering**: Three-level decimal numbering (`1`, `1.1`, `1.1.1`). Embed `1.2 Related Literature` inside Section 1 unless the survey is unusually large.
- `[PRACTICE]` **OR Proof-Credibility Rule (Unified Online Appendix)**: Under our 100% Unified Online Appendix rule (`\ECSwitch`), every headline theorem or proposition in `opre` MUST include a concise **3–6 sentence ordinary-prose Proof Sketch** in the main body naming the mathematical bottleneck and load-bearing technique (e.g., coupling, Lagrangian dual, fluid scaling, martingale concentration) before pointing to `Online Appendix EC.x`.
- `[PRACTICE]` **Affiliations & Acknowledgments**: Author ORCIDs in `\ARTICLEAUTHORS` are common in final versions (`nonblindrev`); keep `\ACKNOWLEDGMENT` to 1–3 sentences thanking anonymous referees and the associate editor by role.

---

### 2. Management Science (`mnsc`)

#### Editorial Inclination & Reviewer Mindset
- **Core question referees ask**: *"What is the sharp economic, behavioral, or managerial tension here, and why should a cross-departmental Management Science reader care?"*
- **Voice & Framing**: Cross-functional business-school flagship (OM, Strategy, Finance, Economics, IS, Marketing, Behavioral Decision Making). Narrowly technical OR/CS papers lacking a compelling economic mechanism or institutional stake risk desk rejection. Write so an area editor outside your immediate subfield immediately grasps why existing intuition fails.

#### Enforced Constraints (`[ENFORCED]`) & Practice Norms (`[PRACTICE]`)
- `[ENFORCED]` **Class & Formatting**: `\documentclass[mnsc,dblanonrev]{informs4}`, minimum **1.5-spacing** (`\OneAndAHalfSpacedXI`, 33 lines/page) or **double-spacing** (`\DoubleSpacedXI`, 25 lines/page), **11pt font, 1-inch margins** all around. Submit via *Management Science* ScholarOne Manuscripts (`https://pubsonline.informs.org/page/mnsc/submission-guidelines`).
- `[ENFORCED]` **Page Limits (Initial vs. Invited Revisions; Fast Track Discontinued)**:
  - **Initial (first-round) submissions**: **No formal page limit**, though manuscripts must be succinct and Department Editors may reject excessively long papers.
  - **Invited revisions**: Strictly **`<= 32` pages** at 1.5-spacing (33 lines/page) **OR `<= 47` pages** at double-spacing (25 lines/page). Online appendices / E-Companions do **not** count toward this page limit.
  - **Fast Track removed**: The former 5,000-word Fast Track submission option has been officially discontinued; all manuscripts follow standard review.
- `[ENFORCED]` **Abstract**: Single unstructured paragraph, strictly **`<= 250` words**, zero mathematical formulas/symbols, and zero citations.
- `[ENFORCED]` **Keywords**: **3–5 keywords** (comma-separated, lowercase except proper nouns and standard abbreviations in `\KEYWORDS{...}` and ScholarOne Attributes).
- `[ENFORCED]` **Double-Anonymous (Double-Blind) Review**: Initial review files must be fully anonymized—omit any identifying title page from the review manuscript, and scrub author names, affiliations, acknowledgments, funding/grant details, and identifying first-person self-citations.
- `[ENFORCED]` **Online Appendix / E-Companion Policy**: Excluded from the revision page limit; upon acceptance, upload as a **separate PDF** that is published online **as-is without copyediting**, so authors must verify final polish themselves.
- `[ENFORCED]` **Data and Code Disclosure & AsCollected.org Provenance**:
  - Mandatory compliance certification and Data and Code Disclosure Form at submission; accepted papers undergo **Data Editor** replication verification (or must document a formal NDA/proprietary-data exception plan at submission).
  - Submissions involving data, code, experiments, surveys, simulations, or observational datasets must create a project record on **AsCollected.org** and supply the project URL during ScholarOne submission.
- `[ENFORCED]` **Submission Fee & Generative AI Policy**:
  - **Submission fee (effective August 1, 2025)**: **USD 79** per original submission to support reproducibility verification (waived for current INFORMS members, authors from World Bank low-/lower-middle-income countries, and honor-based financial hardship without extra justification).
  - **Generative AI policy**: Generative AI tools may assist manuscript preparation, but **AI/ML tools cannot be listed as authors**; authors bear full responsibility for accuracy, originality, and integrity (reviewers report suspected AI-introduced factual errors to the AE/DE).
- `[PRACTICE]` **Introduction Sub-Headers**: Published MS introductions routinely use bold non-numbered inline paragraph headers (`\noindent\textbf{Summary of Contributions.}`, `\noindent\textbf{Overview of Results.}`) as visual signposts. Literature review sits in Section 1.2 (empirical/applied) or Section 2 (dense theory).
- `[PRACTICE]` **Mechanism-First Theorems**: Surround formal propositions with intuitive comparative statics and boundary conditions; include 2–4 sentence proof sketches when a theorem is counterintuitive or methodologically central.

---

### 3. Manufacturing & Service Operations Management (`msom`)

#### Editorial Inclination & Reviewer Mindset
- **Core question referees ask**: *"Does this paper isolate a real, consequential operational lever in manufacturing or services, and are the takeaways genuinely actionable?"*
- **Voice & Framing**: Grounded, institutional, operationally concrete. Anchor every queue, capacity pool, assortment rule, healthcare triage protocol, or fulfillment lever in real operational mechanics before introducing symbols. Even pure analytical papers cannot treat practice as window-dressing.

#### Enforced Constraints (`[ENFORCED]`) & Practice Norms (`[PRACTICE]`)
- `[ENFORCED]` **Template, Class & Submission Portal**: Must use the official M&SOM LaTeX (`\documentclass[msom,dblanonrev]{informs4}` or legacy `informs3.cls`, `\DoubleSpacedXI`, `<= 33` lines/page, 11pt font, 1-inch margins) or Word style files. Submit electronically via ScholarOne Manuscripts (`https://mc.manuscriptcentral.com/msom`; guidelines at `https://pubsonline.informs.org/page/msom/submission-guidelines`); cycle-time tracking starts only once all metadata, files, and disclosures are fully uploaded.
- `[ENFORCED]` **Strict All-Inclusive Page Cap & Online Supplement Cap**:
  - **Main manuscript**: Strictly **`<= 32` pages ALL-INCLUSIVE** (abstract, main text, all references, tables, figures, and any in-document appendices) when typeset in the official M&SOM style.
  - **Online supplement / E-Companion**: Submitted as a separate supporting document, capped at **`<= 16` pages** on all new submissions.
- `[ENFORCED]` **Double-Anonymous (Double-Blind) Review**: Initial submissions must fully anonymize **both the main manuscript and the online supplement**—remove author names, affiliations, acknowledgments, funding/grant details, and identifying first-person self-citations.
- `[ENFORCED]` **Mandatory Structured Abstract (`<= 300` words)**: Single flowing paragraph (not bullets), strictly **`<= 300` words**, zero math/citations, containing the three canonical bold inline labels—even for pure theory papers *(older/alternate variants occasionally include `Academic/practical relevance:` or split `Methodology:` and `Results:`, but the 3-part layout below is standard in current published articles)*:
  ```latex
  \ABSTRACT{%
    \textbf{Problem definition:} State the operational problem and core tension.
    \textbf{Methodology/results:} Summarize the model or empirical design and headline findings.
    \textbf{Managerial implications:} State who benefits, which operational lever changes, and under what condition.
  }
  ```
- `[ENFORCED]` **Prohibition on Bottom-of-Page Footnotes**: Traditional `\footnote{...}` at page bottom is prohibited. Weave essential remarks directly into the main text OR convert subsidiary notes cleanly to numbered **endnotes** placed right before References (`\usepackage{endnotes}` + `\let\footnote=\endnote` + `\theendnotes` before `\bibliography`), which published analytical M&SOM articles use regularly.
- `[ENFORCED]` **Disclosures, Reproducibility & Generative AI Policy**:
  - **COI & related-work disclosure**: Disclose potential conflicts of interest, funding sources, and any prior or concurrent related work in the cover letter and submission forms.
  - **Data & reproducibility**: Empirical, computational, and simulation studies must provide clear documentation, data availability statements, or replication materials to support verification.
  - **Generative AI policy**: Authors may use generative AI tools to assist drafting, editing, or analysis, but **AI tools cannot be listed as authors**; authors bear full responsibility for accuracy, originality, and integrity and must **transparently disclose AI tool usage** (e.g., in acknowledgments or a disclosure statement). Reviewers and editors are strictly prohibited from uploading manuscripts to public or training-based generative AI tools.
- `[PRACTICE]` **Managerial Takeaways Balance**: Empirical M&SOM papers typically include a dedicated `Managerial Implications` subsection in the body; analytical M&SOM papers often deliver managerial takeaways inside the structured abstract and Conclusion (avoiding redundant empty body sections).

---

### 4. INFORMS Journal on Computing (`ijoc`)

#### Editorial Inclination & Reviewer Mindset
- **Core question referees ask**: *"What is the exact computational bottleneck, what is new algorithmically or structurally, and does the method clearly beat state-of-the-art solvers/baselines on reproducible benchmarks?"*
- **Voice & Framing**: Direct, algorithmic, OR-meets-CS precision. Purely theoretical papers without substantive computational implementation or benchmarking are out of scope. Avoid generic business-trend openings and avoid telegraphic CS-conference compression.

#### Enforced Constraints (`[ENFORCED]`) & Practice Norms (`[PRACTICE]`)
- `[ENFORCED]` **Template, Spacing & Single-Blind Review**: `\documentclass[ijoc,nonblindrev]{informs4}` (single-column, **single-blind / single-anonymous review**—reviewers see authors' identities while reviewers remain anonymous; verify current ScholarOne prompt in case of future policy changes), 11pt font, standard margins, `\DoubleSpacedXI` (or `\OneAndAHalfSpacedXI` per template defaults). Submit via ScholarOne (`https://pubsonline.informs.org/page/ijoc/submission-guidelines`) with editable equations/tables/figures and zero tracked changes.
- `[ENFORCED]` **Page Limits (Main Body + Appendices)**:
  - **Main manuscript**: Strictly **`<= 25` pages** inclusive of all references, tables, and graphs (exceptions require Area Editor approval).
  - **Appendices / Online Supplement**: Up to **10 additional pages** permitted; appendices longer than 2 pages must be placed in an online supplement / E-Companion (`\ECSwitch`, `EC.x` numbering).
- `[ENFORCED]` **Abstract & Keywords**: Single unstructured paragraph, zero equations/formulas, zero citations, concise (`< 270` words target, `<= 300` words ceiling) stating (1) computational challenge, (2) algorithmic/software advance, and (3) empirical speedup or gap reduction; accompanied by **3–5 keywords** (`\KEYWORDS{...}` and ScholarOne Attributes).
- `[ENFORCED]` **Software & Data Reproducibility Policy (`INFORMSJoC` GitHub + `.cd` Dual-DOI)**: For computational/software papers, releasing research code and data is a **condition of final acceptance** (supply comparable simulated/surrogate data if datasets are proprietary). Archive via the official **INFORMSJoC** GitHub organization (`https://github.com/INFORMSJoC`; author guide `https://informsjoc.github.io/`, 8-digit tracking repo `XXXX.YYYY`, forked and coordinated with the AE, frozen on acceptance with its own `.cd` companion DOI, containing `README.md`, `LICENSE`, and `AUTHORS`). Embed reproducibility pointers directly inside the `Computational Experiments` section.
- `[ENFORCED]` **Conference Proceedings Extension & Ethics/AI Policies**: Papers previously published in refereed conference proceedings must **substantially extend** the prior work (extended methods, proofs, or broader algorithmic/computational contributions) with explicit disclosure and supplemental comparison material. Follow INFORMS ethics, COI, and AI policies (no AI authorship; full author responsibility).
- `[PRACTICE]` **Paper Type Adaptation (`Algorithm` vs. `Software`)**:
  - *Algorithm / Method papers*: `Introduction` -> `Formulation & Structural Properties` -> `Algorithm` (numbered `algorithm`/`algpseudocode` environments, never buried in prose) -> `Computational Experiments` (full CPU/RAM, threads, solver versions, time limit, benchmark families, exact optimality-gap formulas) -> `Conclusion`.
  - *Software / Package papers*: Replace theoretical Model/Analysis arcs with `Software Architecture`, `API Design & Features`, `Usage Workflow`, and `Benchmark Validation`.
- `[PRACTICE]` **IJOC Proof-Credibility Rule**: Theory supports computation rather than substituting for it. Pair any main-body complexity, convergence, or cut-validity theorem with a crisp 3–5 sentence proof idea before sending verification to `Online Appendix EC.x`.
