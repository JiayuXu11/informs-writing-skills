# Human Craft, Anti-AI Surgery & Style Imitation Guide

Use this reference to prevent and eliminate all **7 AI Writing Diseases**, rebuild Chinglish or translated passages from first principles, calibrate OR/MS evidence verbs and prepositions, and pass source-fidelity preservation checks during rewrites.

---

## Editing & Source-Fidelity Contract (Non-Negotiable for Rewrites)

1. **Preserve Protected Spans**: Never alter mathematical formulas, inequalities, parameter assumptions, `\label`/`\ref`/`\eqref`/`\cite` keys, numerical table cells, or direct data quotes during style polishing.
2. **Never Upgrade Evidence or Fabricate Specifics**: Clarifying prose MUST NOT invent causal identification, statistical significance, optimality guarantees, parameter ranges, sample sizes, citations, or artificial numeric improvements. If an anchor is missing (e.g., an unattributed `"studies show"`), flag the gap rather than inventing a reference.
3. **Never Inject Fake "Humanizer" Fingerprints**: Do NOT manufacture artificial personality—no fake staccato sentence fragments, fabricated anecdotes (`"on my desk"`), performed candor (`"let's be honest"`), or unrequested contrarian hooks (`"everyone thinks X, but they're wrong"`). Plain, accurate field prose is the target.
4. **Preserve Clean Human Prose (Convergence Ceiling <= 2 Passes)**: Leave already crisp, human-written sentences untouched. Run at most two rewrite passes (initial cleanup + targeted verification fix), then stop cleanly.

---

## Disease 1: Notation Bloat & Symbol Soup (`ERROR`)

**Diagnosis**: Assigning symbols to one-off nouns out of habit, dumping a symbol glossary at the start of Section 3, leaving numbered equations that are never `\eqref`-cited, or dragging symbols into Abstracts and Introductions.

- **Zero-Orphan Rule**: A symbol earns its ink ONLY if it is manipulated in displayed math, indexed across sums/sets, or referenced in a theorem/proposition. Refer to everything else in plain English.
- **Zero Abstract Math; Near-Zero Intro Math**: Abstracts contain zero `$...$` symbols and zero citations. Introductions avoid subscripted math (at most 1–2 scalar parameters like discount factor $\delta$ if strictly needed for intuition).
- **Just-in-Time Onboarding**: Never open the Model section with a notation dump. Define each symbol in the sentence immediately preceding or following the display that uses it, giving it a clear English name (`the holding cost $h$`, not bare `$h$`). Place any comprehensive Notation Table in `Online Appendix EC.x`.
- **Cochrane's Equation-Numbering Rule**: Number ONLY equations referenced via `\eqref{...}` (or `\cref{...}`). Use `equation*`/`align*` for unreferenced displays.

*Bad (AI)*: "Consider a platform $\mathcal{P}$ serving buyers $\mathcal{B}$ and sellers $\mathcal{S}$ over horizon $T$, where seller $i \in \mathcal{S}$ picks $p_i \in [0,\bar{p}]$ and faces signal $\sigma_i \in \Sigma$." ($\mathcal{P},\mathcal{B},\bar{p},\Sigma$ never reappear.)
*Good (Human)*: "A platform matches buyers and sellers over $T$ periods. Before arrivals occur, each seller $i \in \{1,\dots,n\}$ observes a private signal $s_i$ and posts a price $p_i$."

---

## Disease 2: Cold-Start / Context-Blind Definitions (`ERROR`)

**Diagnosis**: Treating a non-standard property, technical condition, or construct as self-explanatory before telling the reader why it exists or what it means intuitively, or dropping `\begin{theorem}` / `\begin{definition}` immediately below a section heading with zero setup.

- **4-Beat Onboarding Chain**:
  `1. Motivation (Why the difficulty arises) -> 2. Plain Intuition -> 3. Formal Definition -> 4. Canonical Term`.
- **Adjacent-Reviewer Bridge**: Explain cross-field technical objects once at first consequential use so an adjacent-subfield OR/MS referee can trust why the condition appears (see [manuscript-contract-and-reviewer-calibration.md](./manuscript-contract-and-reviewer-calibration.md)).

*Bad (AI)*: "We impose cross-moment regularity $\mathbb{E}[X_t Y_t] \le \kappa \sigma_t$. Under cross-moment regularity, Algorithm 1 achieves sublinear regret."
*Good (Human)*: "In online pricing with censored feedback, demand shocks and exploration noise can reinforce one another when price adjustments are slow. To prevent rare high-variance bursts from dominating the sample average, we require the covariance between demand noise and feature shocks to stay bounded relative to the exploration scale ($\mathbb{E}[X_t Y_t] \le \kappa \sigma_t$, termed *cross-moment regularity*). Under this condition, Algorithm 1 achieves..."

---

## Disease 3: Stiff Prose, Translated Syntax, Miscalibrated Verbs & AI Tells (`ERROR`)

### A. Concrete Subject-Verb Spine & Gopen-Swan Old-Before-New Craft
- **One Sentence, One Job**: Do not pack setting, variation, estimand, mechanism, and boundary into one breathless clause. Split before polishing.
- **Concrete Subjects**: Replace abstract fillers (`the framework`, `the analysis`, `this paper`, `it is important to note that`) with concrete actors (`the retailer`, `Theorem 1`, `the fluid relaxation`, `Table 2`).
- **Break Noun Piles**: Replace 3+ stacked abstract nouns (`platform information disclosure strategy optimization framework`) with `who chooses what under which constraint` (`when the platform withholds demand forecasts from competing sellers`).
- **Prune Preposition Chains**: When a long sentence carries 6+ prepositions or 3+ `of` phrases before the verb, promote one noun phrase to subject or active verb.
- **Old-Before-New Principle**: Open each sentence on an object the reader already holds from the prior sentence; land the new insight or technical term in the **stress position at the end** of the sentence.
- **Clothe Every Naked `This`**: Never open a sentence with bare `"This shows..."`, `"This enables..."`, or `"This allows..."`. Name the noun (`"This coupling inequality bounds..."`, `"This delay creates price variation..."`).
- **5-Slot Result Sentence Shape** (adapt flexibly, never mechanically): `[Condition/Regime] + [Object/Policy] + [Metric] + [Named Benchmark] + [Mechanism/Boundary]`.

### B. Calibrated Evidence & Mathematical Verb Dictionary (`jmf-enigma/or-ms-writing`)
Never claim more than the evidence supports:

| Lane / Support Type | Exact Calibrated Verbs | Forbidden Overclaims / Miscalibrations |
| :--- | :--- | :--- |
| **Mathematical Theory** | `characterize` (policies, thresholds, equilibria), `establish` (theorems, bounds, rates), `prove` (lemmas, theorems), `derive` (duals, FOCs, expressions), `reduce` (state space, DP), `verify` (KKT, IC/IR), `bound` (gap, regret) | `"prove"` from simulation alone; `"validate"` from a toy numerical example |
| **Empirical / Archival / DiD / IV** | `document` (descriptive patterns), `estimate` (coefficients, elasticities), `identify` (only with credible ID/randomization), `test`, `preserve` (sign/magnitude in robustness), `suggest`, `is consistent with` | `"prove"` for regression results; `"identify"` for pure correlation; bare `"significant"` without statistical vs economic |
| **Experimental / Behavioral** | `randomly assign`, `elicit` (beliefs, WTP), `measure` (calibration, attention), `detect` (treatment contrast, spillover), `separate` (channels) | `"eliminate endogeneity"` unless design supports it; confounding ITT with TOT |
| **Algorithms & Simulation** | `formulate`, `construct`, `decompose`, `relax`, `benchmark`, `evaluate`, `scale` | `"outperform existing methods"` without naming metric, baseline solver, and instance family |

### C. Noun Anchors & Idiomatic OR/MS Prepositions
- **Anchor Vague Nouns**: Never write bare `framework`, `mechanism`, `insight`, `strategy`, `efficiency`, or `robustness`. Specify *cost vs allocative vs computational efficiency*, *robust to [alternative specification]*, or *choose a pricing policy* (avoid `optimize the strategy` / `decision-making`).
- **Preposition Rules**: `effect ON` (not *to*); `robust TO` (not *for*); `sensitive TO` (not *for*); `improve RELATIVE TO` / `compared WITH` (not *improved than*); `increase IN [metric] BY [amount] FOR [subgroup] WHEN [condition]`; `UNDER [assumption/regime]`; `DRIVEN BY [mechanism]`; `CONSISTENT WITH`; `ABSTRACT FROM`. Use `in which` for models/regimes (`"a market in which sellers..."`), reserving `where` for spatial or physical locations.

### D. Chinese-Logic (Chinglish) & McCloskey "Delete on Sight" Table
Do NOT polish translated English word by word—extract `{Actor, Action, Object, Warrant, Condition}` and write fresh English:

| Chinglish / McCloskey Bloat | Native INFORMS Replacement |
| :--- | :--- |
| `under the background of ...` / `with the development of ...` | Delete; open with the concrete operational friction or policy rule |
| `has an important influence on` | `affects`, `shifts`, `alters`, `amplifies`, or `reduces` |
| `according to the model` / `it can be seen that` | Make `Theorem 1`, `Proposition 2`, or `Table 3` the subject |
| `based on the above analysis` / `to a certain extent` / `has certain` | State the exact regime, bound, or conditional comparison |
| `managerial enlightenment` / `optimize decision-making` | Name who acts, what control changes (`set prices`), and under what condition |
| `put forward a model` / `conduct/make research on` | `develop a model` / `formulate`; `study` / `examine` / `estimate` |
| `It is worth/should be noted that` / `A comment is in order` | Delete opener and state the point directly |
| `It is easy to show that` / `In other words` | Show the 1-line move, or say it cleanly the first time |
| `Results are reported in Table X` | `Table X reports...` (active tables as grammatical subjects) |

### E. Exhaustive Anti-AI Blocklist & Technical Carve-Outs
1. **2023+ AI Crutch Vocabulary & Self-Praise**: Ban `delve, underscore, pivotal, paramount, vital, crucial (hype), intricate, multifaceted, nuanced, tapestry, realm, landscape, journey, harness, leverage (verb), utilize, unlock, foster, bolster, garner, showcase, boast, seamless, holistic, comprehensive (self-praise), novel (self-label), groundbreaking, cutting-edge, state-of-the-art, shed light on, pave the way`.
2. **Copula Avoidance (`ec-copula-sense`)**: Replace inflated press-release substitutes (`serves as, acts as, stands as, functions as, features, boasts, represents`) with plain `is` or `has` unless naming an actual formal role.
3. **Participial Result Tails**: Ban `", highlighting the importance of..."`, `", underscoring..."`, `", demonstrating..."`, `", paving the way for..."`. State the result cleanly; give the implication its own sentence.
4. **Sentence-Initial Transition Glue**: Never start sentences or paragraphs with `Moreover,`, `Furthermore,`, `Additionally,`, `Ultimately,`, `Overall,`, `In essence,`, `Indeed,`, or `That said,`. Link via object continuity (`Because`, `When`, `Unlike`).
5. **Punctuation & Structural Tics**:
   - **Zero Prose Em-Dashes (`---` / `—`)**: Replace with commas, parentheses, or a period. *(Carve-out: numeric en-dash ranges `2019--2023` or `1\%--2\%` pass cleanly.)*
   - **Zero Colon Flourish Labels**: Ban `Key insight:`, `Takeaway:`, `Proof idea:`, `The bottom line:`, `Contribution:`. *(Carve-out: formal `Definition 1:`, math notation `$f: X \to Y$`, and M&SOM's three mandatory `\ABSTRACT` headers pass cleanly.)*
   - **Negative Parallelism & Invented Mirrors**: Ban staged `"It is not X, it is Y"` / `"not merely X, but Y"` stacks and asymmetric invented contrast pairs (`"false precision rather than genuine accuracy"`). State the positive claim directly or contrast two real terms of art.
   - **Rule-of-Three & List Inflation**: Keep three-item lists strictly for genuine distinct mechanisms or assumptions—ban decorative adjective triads (`"robust, scalable, and efficient framework"`). Never dump 5+ verb-less bullet NPs.
   - **Moral-Adjective & Ontological Slop**: Never attach moral adjectives (`honest`, `faithful`, `truthful`, `genuine`) to curves, bounds, or outputs. Never write `"the assumption stops being true"`—write `"the assumption breaks down"` or `"fails to hold"`. Cut unverifiable universal quantifiers (`"every real-world retailer"`).
   - **Vague Attributions & Filler Hedges**: Replace `"numerous studies"` or `"experts believe"` with exact `\cite{...}` keys or counts. Cut hollow intensifiers (`very, quite, really, basically, essentially, dramatically, arguably, to some extent`).
   - **Rhythm & Burstiness**: Vary sentence lengths across 8–26 words (avoid 5+ consecutive medium 16-word sentences of nearly identical length, and never start 3+ consecutive sentences with the exact same non-article word).
   - **Technical Context Carve-Outs**: Never mechanically purge statistical/optimization terms of art (`robust standard errors`, `robust optimization`, `Markovian landscape`, `convexity`), provided the surrounding noun phrase is precise.

---

## Disease 4: Defensive / Self-Sabotaging Caveats (`ERROR`)

**Diagnosis**: Undermining your own theorem or empirics immediately after stating it (`"Although we establish Theorem 1, this does not fully explain..."`, `"not without limitations"`, `"while challenges remain"`). AI uses false concession pairs to feign balance without weighing evidence.

- **Positive Upfront Scope Rule**: State validity positively via explicit conditions BEFORE or INSIDE the claim (*"When demand satisfies increasing failure rate, Theorem 1 shows..."*).
- **Constructive Conclusion Extensions**: Reserve genuine model boundaries for constructive future-research extensions in the Conclusion—never apologize in Section 1, 3, or 4.

*Bad (AI)*: "Theorem 1 establishes that the threshold policy is optimal. However, our model assumes stationary demand and therefore cannot fully capture real-world pricing dynamics."
*Good (Human)*: "When demand is stationary and competitor prices are fixed, Theorem 1 establishes that a threshold policy is optimal. Section 6 extends the policy class to Markov-modulated arrivals."

---

## Disease 5: Raw Decimal Dumping in Prose (`ERROR`)

**Diagnosis**: Reading regression/benchmark table cells aloud inside narrative paragraphs (`"increases profit by 1.32%, cuts cost by 0.87%, and reduces stockouts by 4.19%"`).

- **Harmonized INFORMS Rule (Pattern Prose + Table Precision)**: Narrative prose in the Abstract, Introduction, and Results communicates **causal/economic mechanisms, named benchmarks, and clean rounded orders of magnitude or ranges** (`roughly 1%--2%`, `nearly a third`, `cuts solve time roughly threefold`), citing specific papers/counts instead of vague gestures (`"various studies"`). Keep exact 2–3 decimal point estimates and standard errors inside `booktabs` tables! *(Carve-out: `p = 0.012` / $\alpha$-cutoffs `0.05` and section numbers `Section 3.2` pass cleanly.)*

*Bad (AI)*: "Our policy increases profit by 1.32% under low volatility, 2.47% under medium volatility, and 4.83% under high volatility."
*Good (Human)*: "The profit advantage of the adaptive policy scales steeply with demand volatility, rising from roughly 1%--2% in stable regimes to nearly 5% under high volatility (Table 2)."

---

## Disease 6: Definition Abuse, Formal `Definition` Bloat & Terminological Drift (`ERROR`)

**Diagnosis**: Wrapping routine variables/metrics inside numbered `\begin{definition}` blocks, re-defining the same object across sections with different wording, or cycling synonyms (`fulfillment gap`, `allocation shortfall`, `service deficit`) for stylistic variety.

- **One Concept = One Definition = One Canonical Name**: Define each object **once** at first consequential use, record its canonical term in a manuscript Terminology Registry, and repeat that exact term everywhere—even 3× in one paragraph (`ec-stable-terms`).
- **Cap `\begin{definition}` at <= 2**: Define routine primitives, KPIs, and regimes inline in prose. Reserve numbered `\begin{definition}` blocks solely for 1–2 foundational, newly coined theoretical constructs across the entire main text.

---

## Disease 7: Chat-Context, Diff-Anchored & Revision-History Leakage (`ERROR`)

**Diagnosis**: Letting author–LLM chat turns, PDF margin instructions, debugging history, or diff-anchored commentary leak into manuscript prose (`"Unlike the previous version..."`, `"In this revised model..."`, `"We have corrected..."`, `"As requested..."`, `"Note: ..."`).

- **Timeless Standalone Manuscript Rule**: Every journal reader has ZERO access to your prompt history, coauthor chat, or earlier drafts. Delete all version-comparison and edit-history narration; state the final model, theorem, or empirical spec cleanly as if written that way from day one. Leave unfilled placeholders (`[AUTHOR: ...]`, `[TODO]`) strictly out of finished files. *(For Point-by-Point Referee Response letters—kept strictly separate from the manuscript—see [manuscript-contract-and-reviewer-calibration.md](./manuscript-contract-and-reviewer-calibration.md).)*
