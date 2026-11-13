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
- **Length & Exemplar Calibration**: Keep the Abstract **`< 270` words** (checking submission portal text-box limits when uploading) and keep the compiled **Introduction `<= 3` pages**, using the word counts of corresponding sections in recent target-journal exemplars as your primary reference.

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
- `[ENFORCED]` **Class & Spacing**: `\documentclass[opre,dblanonrev]{informs4}` (or `nonblindrev`), `\DoubleSpacedXI`.
- `[ENFORCED]` **Page Cap**: Regular manuscripts **<= 30 pages excluding references** (Lengthy manuscripts `<= 40` pages excluding references, tied to slower review). Target Main Text + Figures/Tables + References `<= 33--35` pages.
- `[ENFORCED]` **Abstract**: Single unstructured paragraph, generally **`< 270` words** (trim if the online portal enforces a `<= 200` box limit), zero equations/symbols, zero citations.
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
- `[ENFORCED]` **Class & Spacing**: `\documentclass[mnsc,dblanonrev]{informs4}`, `\OneAndAHalfSpacedXI` (standard, 33 lines/page) or `\DoubleSpacedXI` (25 lines/page), 11pt, 1-inch margins.
- `[ENFORCED]` **Page Cap (Revisions & Length Discipline)**: **<= 32 pages** at 1.5-spacing or **<= 47 pages** at double-spacing including Main Text + Figures/Tables + References (Electronic Companion excluded). **Fast Track** pathway: **<= 5,000 words** total outside Online Appendix (~7.7% acceptance, binary revise-or-reject).
- `[ENFORCED]` **Abstract**: Single unstructured paragraph, generally **`< 270` words** (trim if the online portal enforces a `<= 250` box limit), zero equations, zero citations.
- `[ENFORCED]` **Keywords**: **3–5 keywords**, comma-separated, lowercase except proper nouns and standard abbreviations (`\KEYWORDS{...}`).
- `[ENFORCED]` **Data and Code Disclosure**: Mandatory disclosure statement/form on initial submission and revisions confirming reproducibility compliance.
- `[PRACTICE]` **Introduction Sub-Headers**: Published MS introductions routinely use bold non-numbered inline paragraph headers (`\noindent\textbf{Summary of Contributions.}`, `\noindent\textbf{Overview of Results.}`) as visual signposts. Literature review sits in Section 1.2 (empirical/applied) or Section 2 (dense theory).
- `[PRACTICE]` **Mechanism-First Theorems**: Surround formal propositions with intuitive comparative statics and boundary conditions; include 2–4 sentence proof sketches when a theorem is counterintuitive or methodologically central.

---

### 3. Manufacturing & Service Operations Management (`msom`)

#### Editorial Inclination & Reviewer Mindset
- **Core question referees ask**: *"Does this paper isolate a real, consequential operational lever in manufacturing or services, and are the takeaways genuinely actionable?"*
- **Voice & Framing**: Grounded, institutional, operationally concrete. Anchor every queue, capacity pool, assortment rule, healthcare triage protocol, or fulfillment lever in real operational mechanics before introducing symbols. Even pure analytical papers cannot treat practice as window-dressing.

#### Enforced Constraints (`[ENFORCED]`) & Practice Norms (`[PRACTICE]`)
- `[ENFORCED]` **Class & Spacing**: `\documentclass[msom,dblanonrev]{informs4}`, `\DoubleSpacedXI` (`<= 33` lines/page, 11pt, 1-inch margins).
- `[ENFORCED]` **Strict Page Cap**: **<= 32 pages ALL-INCLUSIVE** (body + references + tables + figures). **Online Appendix strictly capped at <= 16 pages** on all new submissions!
- `[ENFORCED]` **Three-Part Structured Abstract (`< 270` words target)**: Single flowing paragraph (not bullets), zero math/citations, containing the three mandatory bold inline labels—even for pure theory papers:
  ```latex
  \ABSTRACT{%
    \textbf{Problem definition:} State the operational problem and core tension.
    \textbf{Methodology/results:} Summarize the model or empirical design and headline findings.
    \textbf{Managerial implications:} State who benefits, which operational lever changes, and under what condition.
  }
  ```
- `[ENFORCED]` **Prohibition on Bottom-of-Page Footnotes**: `\footnote{...}` at page bottom is prohibited. Place subsidiary notes parenthetically in text OR convert them cleanly to numbered **endnotes** before References (`\usepackage{endnotes}` + `\let\footnote=\endnote` + `\theendnotes` before `\bibliography`), which published analytical M&SOM articles use regularly.
- `[PRACTICE]` **Managerial Takeaways Balance**: Empirical M&SOM papers typically include a dedicated `Managerial Implications` subsection in the body; analytical M&SOM papers often deliver managerial takeaways inside the structured abstract and Conclusion (avoiding redundant empty body sections).

---

### 4. INFORMS Journal on Computing (`ijoc`)

#### Editorial Inclination & Reviewer Mindset
- **Core question referees ask**: *"What is the exact computational bottleneck, what is new algorithmically or structurally, and does the method clearly beat state-of-the-art solvers/baselines on reproducible benchmarks?"*
- **Voice & Framing**: Direct, algorithmic, OR-meets-CS precision. Purely theoretical papers without substantive computational implementation or benchmarking are out of scope. Avoid generic business-trend openings and avoid telegraphic CS-conference compression.

#### Enforced Constraints (`[ENFORCED]`) & Practice Norms (`[PRACTICE]`)
- `[ENFORCED]` **Class & Spacing**: `\documentclass[ijoc,nonblindrev]{informs4}` (single-column, single-blind review by default), `\DoubleSpacedXI`.
- `[ENFORCED]` **Page Target**: Concise main body **<= 25 pages** (Main Text + Tables/Figures + References), pushing extended instance logs and parameter sweeps to `Online Appendix EC.x`.
- `[ENFORCED]` **Abstract**: Single unstructured paragraph, generally **`< 270` words**, zero equations/citations; state (1) computational challenge, (2) algorithmic/software advance, and (3) empirical speedup or gap reduction.
- `[ENFORCED]` **Code & Data Repository (Dual-DOI `.cd` Policy)**: Every accepted IJOC paper requires an archival companion repository under `https://github.com/INFORMSJoC` receiving its own `.cd` DOI (e.g., `10.1287/ijoc.2024.0938.cd`) cited alongside the paper DOI, with a standardized README (citation, description, installation, replication instructions, results summary). Embed reproducibility pointers directly inside the `Computational Experiments` section rather than hiding them.
- `[PRACTICE]` **Paper Type Adaptation (`Algorithm` vs. `Software`)**:
  - *Algorithm / Method papers*: `Introduction` -> `Formulation & Structural Properties` -> `Algorithm` (numbered `algorithm`/`algpseudocode` environments, never buried in prose) -> `Computational Experiments` (full CPU/RAM, threads, solver versions, time limit, benchmark families, exact optimality-gap formulas) -> `Conclusion`.
  - *Software / Package papers*: Replace theoretical Model/Analysis arcs with `Software Architecture`, `API Design & Features`, `Usage Workflow`, and `Benchmark Validation`.
- `[PRACTICE]` **IJOC Proof-Credibility Rule**: Theory supports computation rather than substituting for it. Pair any main-body complexity, convergence, or cut-validity theorem with a crisp 3–5 sentence proof idea before sending verification to `Online Appendix EC.x`.
