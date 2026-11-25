# Workflow B: Surgical Rewriting, De-AI & Notation Slimming (`1 -> N`)

Use this workflow when revising existing English drafts, AI-generated text, Chinglish/Chinese-logic notes, or full `.tex` manuscripts.

---

## Non-Negotiable Editing & Preservation Contract (`conorbronsdon` + `or-ms-writing`)

1. **Protected Regions**: Never corrupt equations, inequality bounds, `\label`, `\ref`, `\eqref`, `\cite`, table numbers, or code/URLs unless the user explicitly requested a notation or data update.
2. **Respect Clean Human Prose**: If a sentence or paragraph is already clear, concrete, and free of AI/Cold-Start/Drift defects, leave it untouched. Never change wording merely to prove edits occurred.
3. **Never Inject Fake Humanizer Tics**: Do NOT inject artificial staccato fragments, fake personal asides (`"I've seen..."`), performed candor (`"let's be honest"`), or manufactured contrarianism.
4. **Never Upgrade Claims**: Never invent significance, optimality, causality, magnitudes, or citations. If a factual detail or citation anchor is missing, narrow the claim or flag the gap for the user.
5. **Convergence Ceiling <= 2 Passes**: Complete all ordered passes cleanly in Pass 1; perform at most one targeted Pass 2 if static checks uncover residual violations. Never loop indefinitely.

---

## Step 1: Triage & Git Checkpoint

1. Run `git status` in the manuscript directory. If uncommitted baseline changes exist, create a checkpoint (`checkpoint: pre-rewrite baseline`) or track cleanly before editing.
2. Select Tier matching the user's requested granularity (never redesign a whole paper when only asked to fix one paragraph):
   - **Tier 1 (Micro / Paragraph Polish)**: Prose sounds stiff, translated, AI-generated, defensive, or decimal-heavy.
   - **Tier 2 (Cognitive, Definition & Notation Slimming)**: Draft dumps symbols early, drops cold-start concepts, duplicates definitions, or embeds mechanical algebra in the body.
   - **Tier 3 (Section / Full-Manuscript Calibration)**: Cross-section drift, wrong journal rules (`opre`/`mnsc`/`msom`/`ijoc`), or body page overrun.

---

## Step 2: Execute Ordered Diagnostic Passes (Logic -> Notation -> Craft -> Journal)

Always fix **logic, missing definitions, and symbol bloat BEFORE polishing prose**:

### Pass 1: Cognitive Onboarding, Storyline Bridges, Definition Lock & Dependency Repair
- **Fix Cold-Start Concepts & Front-to-Back Linear Readability (Disease 2)**: Run the **Front-to-Back Linear Reading Test** from Sentence 1 of the Abstract through the middle of the paper assuming zero knowledge of later sections; replace or immediately explain in plain operational English any paper-specific label, acronym, or niche term on first appearance (especially in Abstract and Introduction). Insert `Why -> Intuition -> Definition -> Canonical Term` immediately before any unfamiliar concept, assumption, or theorem block, and ensure no `\begin{theorem}` or `\begin{definition}` sits naked directly under a section heading.
- **Repair Section-to-Section & Proposition-to-Proposition Storyline Bridges**: Check that each section opens by linking what the prior section resolved to the next open question, and that consecutive propositions/theorems are connected by analytical bridges explaining *why* we prove the next proposition within the paper's storyline (never stack results like bricks).
- **Collapse Duplicate Definitions & Lock Terminology (Disease 6)**: Merge overlapping definitions of the same object into one crisp first-use definition; convert gratuitous `\begin{definition}` blocks into inline prose (strictly `<= 2` formal `Definition` blocks in main body); replace cycling synonyms (*shortfall / gap / deficit*) with one locked canonical term across all sections.
- **Check Paragraph Dependencies**: Verify actors, timing, benchmark, and identification variation precede any result or robustness table relying on them (run the `Paragraph-Reshuffle`, `Treadmill`, and `Front-to-Back Linear Reading` tests from [section-and-lane-architecture.md](./section-and-lane-architecture.md)).

### Pass 2: Notation De-Bloating & Unified Online Appendix Split
- **Prune Orphan & Early Math (Disease 1)**: Strip symbols from the Abstract; strip non-essential subscripted notation from Intro; replace single-use inline symbols `$x_k$` in Model/Results with plain English nouns; remove any upfront glossary table to `Online Appendix EC.x`.
- **Unnumber Unreferenced Displays**: Switch un-`\eqref`'d `equation`/`align` environments to `equation*`/`align*` (or `\nonumber`) and replace any deprecated `eqnarray`.
- **Compress Heavy Derivations**: Keep only `Starting Object -> Load-Bearing Move -> Resulting Object` in the main text; move routine algebra, constants, KKT cases, and helper lemmas under `\ECSwitch` (`Online Appendix EC.x`).
- **Enforce 100% Unified Online Appendix**: Convert any regular `\appendix` or bare `Appendix A` citation into `\ECSwitch` + `\ECHead` + `Online Appendix~\ref{ec:...}`. Ensure `opre`/`ijoc` headline theorems keep a 3–6 sentence body Proof Sketch.

### Pass 3: Anti-AI Surgery, Verb Calibration & Chinglish Reconstruction
Apply [human-craft-and-anti-ai.md](./human-craft-and-anti-ai.md):
1. **Purge Chat, Diff-Anchored & Revision Leakage (Disease 7)**: Strip all meta-text about prior drafts, bug fixes, or prompts (*"Unlike the previous version..."*, *"We have corrected..."*, *"In this revised model..."*, *"As requested..."*) so the text reads timelessly.
2. **Eliminate Defensive Self-Sabotage & False Concessions (Disease 4)**: Strip post-result disclaimers (`"does not fully capture..."`, `"while challenges remain"`, `"not without limitations"`); move scope conditions positively upfront (`"Under stationary arrivals..."`) and genuine future avenues to Conclusion.
3. **Replace Numeric Clutter & Table/Figure Readouts with Trends (Disease 5)**: Strip both multi-decimal dumps (`"1.32% and 0.87%"`) and 1-decimal point-by-point figure/table transcripts (`"from 9.3 at L=1 to 4.4 at L=2, 2.1 at L=3, and 0.6 at L=5"`). Narrate qualitative trends, regime crossovers, and mechanisms, keeping at most 1--2 rounded headline anchors per paragraph and letting the table or figure carry exact values.
4. **Rebuild Chinglish & Weak Spines (Disease 3)**: Rebuild translated drafts from `{Actor, Verb, Object, Condition}`; clothe every naked `This` (`This bound...`); eliminate 3+ noun piles, 6+ preposition chains, AI crutch vocabulary, copula avoidance, negative parallelism, `-ing` participial tails, sentence-initial `Moreover/Furthermore`, em-dashes, frequent explanatory parentheticals, colon flourish headers, and decorative triplets. Calibrate evidence verbs (`characterize/establish/bound` vs `document/estimate/identify/is consistent with`).

### Pass 4: Preserve LaTeX Integrity & Journal Rules
- Verify zero `\hline` or vertical `|` bars inside tables (`booktabs` + `threeparttable`).
- Enforce exact target-journal rules in [journals-informs-matrix.md](./journals-informs-matrix.md) (`opre`: `<= 200`-word single-paragraph abstract with zero math/citations, double-anonymous body & E-Companion, `\SUBJECTCLASS`/`\AREAOFREVIEW`, `<= 30` pp regular / `<= 40` pp lengthy / `<= 20` pp Focused Technical or Context & Challenge limits; `mnsc`: `<= 250`-word single-paragraph abstract, `3–5` lowercase keywords, double-anonymous review, no initial page cap but invited revisions `<= 32` pp at 1.5-spacing or `<= 47` pp double-spaced excl. EC, Data & Code Disclosure + AsCollected.org URL; `msom`: 3-part structured abstract `<= 300` words, `<= 32` pp ALL-INCLUSIVE + `<= 16` pp online supplement, double-anonymous body & supplement, zero `\footnote` [use `\endnote` + `\theendnotes`], COI/related-work & AI-use disclosures; `ijoc`: single-blind `nonblindrev`, single-paragraph abstract `< 270`w target / `<= 300`w cap, `3–5` keywords, `<= 25` pp incl. refs/tables/graphs + `<= 10` pp online supplement, numbered `algorithm` + `INFORMSJoC` `.cd` repo reproducibility + proceedings-extension disclosure; compiled Introduction `<= 3` pages across all journals).

---

## Step 3: "If The Draft Feels Weird" Quick Triage (`or-ms-writing`)

| Symptom | Fast Surgical Fix |
| :--- | :--- |
| Reads like a checklist / slot-fill | Drop unused story beats; keep only primary burden + warrant |
| Feels dry after stripping AI words | Don't add hype—restore the missing *analytical relation* (definition, benchmark, threshold, or mechanism) |
| Three-adjective stack (`robust, scalable, efficient`) | Collapse to the single exact property or split into separate proven claims |
| Moves by `we first ... we then ... finally` | Replace itinerary narration with object/dependency movement |
| Starts with `This enables / This allows` | Name the exact inequality, policy, variation, or assumption doing the work |
| Long `of / for / in / under` pre-verb pile | Promote actor, theorem, policy, or estimator to grammatical subject |
| Reads like translated Chinese | Extract intended relation privately; rebuild English sentence from scratch |
| Feels like a grant pitch (`pivotal`, `novel insight`) | Replace praise with decision, metric, theorem, or estimate magnitude |
| Too informal / blog-like | Name the formal construct, estimand, policy class, or comparator—don't inflate adjectives |
| Appendix carries the whole paper | Move headline theorem, benchmark, interpretation, and 3–6 sentence proof sketch back to body |

---

## Step 4: Automated Audit Gate, Compiled-PDF QA & Git Commit

1. For single passages or sections:
   ```bash
   python "<skill_dir>/scripts/check_prose_craft.py" <passage.txt> --section <intro|model|results|conclusion|paragraph>
   ```
2. For full `.tex` manuscripts:
   ```bash
   python "<skill_dir>/scripts/audit_informs_draft.py" <manuscript.tex> --journal <opre|mnsc|msom|ijoc>
   python "<skill_dir>/scripts/audit_manuscript_contract.py" <manuscript.tex> --journal <opre|mnsc|msom|ijoc>
   ```
3. Compile the updated `.tex` to PDF whenever TeX is available, run the visual PDF layout checker, and inspect flagged pages with `read_file` to rule out garbled glyphs, oversized blank bands, overlapping lines, or margin overflows ([visual-design-and-pdf-qa.md](./visual-design-and-pdf-qa.md)):
   ```bash
   python "<skill_dir>/scripts/check_pdf_layout.py" <manuscript.pdf> --render-flagged /tmp/pdf_qa
   ```
4. Resolve every flagged `[ERROR]` (and relevant `[WARN]`), verify clean exit `0`, commit atomically (`git add <files> && git commit -m "revise(<scope>): <concise summary>"`), and summarize edits briefly alongside the commit hash.
