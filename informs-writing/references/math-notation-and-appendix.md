# Mathematical Hygiene, Theorem Packaging & Unified Online Appendix

Use this reference when structuring a Model section, auditing symbols, writing derivations or proof sketches, designing `booktabs` tables and vector figures, or deciding what moves to the Unified Online Appendix (`\ECSwitch`).

---

## 1. Minimalist Modeling & Notation Hygiene

1. **Simplest Insightful Model (Glaeser & Varian Rule)**: Use the minimal horizon, agent count, and state space that isolates the economic or algorithmic mechanism. Every added layer of generality that leaves qualitative mechanics unchanged obscures causality and triggers referee pushback.
2. **Plain-English Setup Before Math**: Describe the physical operating setting, agents, sequence of events (timing), information asymmetry, feasible actions, and benchmark in ordinary English prose BEFORE introducing formal equations.
3. **Letter & Subscript Discipline**:
   - **Latin** for observables, states, decisions, and indices ($x_t, p_i, q, N, T$).
   - **Greek** for structural parameters, dual multipliers, thresholds, and rates ($\lambda, \mu, \theta, \alpha, \gamma$).
   - **Calligraphic / Blackboard** ($\mathcal{S}, \mathcal{F}_t, \mathbb{E}$) strictly when sets, action spaces, or filtrations are indexed or manipulated. Order subscripts consistently from smallest/fastest to largest/slowest unit ($Y_{it}, x_{ijt}$).
   - Define every symbol with its English name (`the unit holding cost $h$`), not just `$h$`, at the moment an upcoming display uses it (Just-in-Time). Place any master notation table in `Online Appendix EC.x`.
4. **Numbered Equation Discipline (`econ-writing-skill` Rule)**:
   - Number **ONLY** equations explicitly referenced via `\eqref{...}` or `\cref{...}` (`\begin{equation*}`, `\begin{align*}`, or `\nonumber`).
   - **Never** use deprecated `\begin{eqnarray}`.
   - Never display trivial verbal identities (e.g., `"total revenue equals price times quantity"`) as centered displays.

---

## 2. Body Display Choreography & Three-Checkpoint Derivations

### The 5 Legitimate Jobs of a Main-Text Display
Every displayed equation in the body must perform one of five jobs (otherwise turn it into inline prose or move it to `Online Appendix EC.x`):
1. **System Dynamics**: State transitions, arrival/demand laws, conservation or queue evolution.
2. **Decision Problem / Estimand**: Objective, constraints, policy class, benchmark problem, or causal estimating equation.
3. **Analysis Surrogate**: Lagrangian relaxation, fluid limit, convex surrogate, regret decomposition, or sufficient statistic.
4. **Headline Result**: Characterization formula, closed-form threshold, approximation ratio, or regret bound.
5. **Proof Checkpoint**: One load-bearing decomposition or inequality inside a main-body proof sketch.

### Prose Framing & Display Density
- Never drop a bare display followed only by a `where ...` variable list. Tell the reader what the equation computes or balances BEFORE or immediately AFTER it.
- Never stack **3+ consecutive displays** without explanatory prose telling the reader what transformed between steps (exception: a cohesive system of constraints).
- **Three-Checkpoint Main-Text Derivations**: When transforming a formulation (primal -> dual, DP -> Bellman index, regret -> estimation + control), show only three beats in the body:
  `1. Starting Object -> 2. Load-Bearing Move -> 3. Resulting Object`
  Send intermediate constants, KKT algebra, Taylor expansions, and repeated case splits to `Online Appendix EC.x`.

---

## 3. Assumptions, Theorem Packaging & Subfield Proof Moves

### Three-Part Assumption Discipline
Place standing assumptions close to the model component they govern, numbered concisely (`Assumption 1`), specifying:
1. Formal mathematical condition.
2. Plain economic or operational interpretation.
3. Analytical role (e.g., *preserves convexity*, *rules out boundary degeneracy*, *prevents demand-shock explosion*, *identifies the marginal buyer*). Never write ontological slop like `"the assumption stops being true"`—write `"breaks down"` or `"fails to hold"`.

### Spare Result Labels & Formal `Definition` Cap
- Use bare labels (`\begin{theorem}`) or brief noun descriptors (`\begin{theorem}[Regret Upper Bound]`, `\begin{proposition}[Threshold Policy]`). Never put full-sentence claims inside `[...]` titles!
- Cap `\begin{definition}` blocks at **<= 2 across the entire main body**; define all standard metrics, policies, and regimes inline in prose with one locked canonical name.

### The 4-Part Local Result Package
1. **Setup Bridge (1–2 sentences)**: Name the comparison, policy class, or theorem type (`existence, uniqueness, monotonicity, threshold structure, comparative static, approximation ratio, regret rate`).
2. **Formal Statement**: Self-contained primitives, parameter ranges, policy class, and comparator—state scope conditions positively upfront!
3. **Operational / Economic Interpretation (2–4 sentences)**: Explain the qualitative trade-off, which parameter shifts the regime threshold, and why the mechanism moves in that direction.
4. **Post-Result Proof Convention + Conclusion-First Pointer**:
   - **Short illuminating proof** (`<= 10` lines): Keep directly in the body via `\begin{proof} ... \Halmos \end{proof}`.
   - **`opre` & `ijoc` Headline Results (Mandatory Proof Sketch)**: Write a literal, 3–6 sentence ordinary-prose proof sketch naming the core mathematical bottleneck and load-bearing technique, closing with a conclusion-first pointer: *"The complete proof, including the boundary-case verification in Lemma EC.2, is provided in Online Appendix~\ref{ec:proofs}."*
   - **`mnsc` & `msom` Routine / Long Proofs**: Either follow the same conclusion-first interpretation + `Online Appendix~\ref{ec:proofs}` pointer (default), or use a crisp `Proof.` one-line venue pointer when the manuscript adopts that convention—provided full interpretation precedes or follows in nearby body prose.

### Literal Proof Verbs & Subfield Proof Moves
Use plain proof verbs (`construct, decompose, relax, couple, bound, compare, apply, combine, verify`), never `"by some algebra"`, `"it is easy to see"`, or dramatic flourish (`"an elegant trick"`):
- **Optimization**: feasibility -> upper/lower bound -> candidate construction -> KKT/duality -> tightness.
- **Dynamic Programming**: Bellman recursion -> structural preservation (concavity/submodularity) -> contraction/induction -> threshold policy -> comparative statics.
- **Mechanism Design**: IC/IR envelope reduction -> monotonicity -> virtual surplus -> allocation/payment construction -> ironing/boundary checks.
- **Revenue Management / Pricing**: hazard-rate / demand regularity -> FOC / markup characterization -> benchmark gap -> welfare contrast.
- **Online Learning / Bandits**: high-probability confidence event -> regret decomposition -> concentration step -> epoch tuning -> lower bound.

---

## 4. Unified Online Appendix (`\ECSwitch`) & Placement Map

This skill enforces a **100% Unified Online Appendix policy**: ZERO regular `\appendix` inside the main manuscript across all four INFORMS journals (`opre`, `mnsc`, `msom`, `ijoc`). Main Text + Figures/Tables + References end strictly BEFORE `\ECSwitch` so page caps are cleanly respected (`opre` <= 30 pp excl. refs, `mnsc` <= 32 pp at 1.5x, `msom` <= 32 pp all-inclusive + **EC <= 16 pp**, `ijoc` <= 25 pp).

| Content Type | Main Body Role | Unified Online Appendix (`\ECSwitch`) Role |
| :--- | :--- | :--- |
| **Headline Theorem / Estimate** | Complete statement, interpretation, metric, comparator, 3–6 sentence proof sketch (`opre`/`ijoc` mandatory) | Full proof, helper lemmas, boundary regimes, constants (`Online Appendix EC.1`) |
| **Core Model / Formulation** | Operating setting, timing, key displays, standing assumptions | Complete notation table, equivalent reformulations, assumption sufficient checks |
| **Central Derivation** | `Start -> Key Move -> Resulting Object` checkpoint | Step-by-step algebra, KKT complementary slackness, induction cases |
| **Algorithm (`ijoc`/`opre`)** | Core `algorithm` pseudocode, complexity/validity guarantee, main benchmarks | Helper subroutines, tuning grids, instance-by-instance solver logs |
| **Empirical Design / Robustness** | Preferred spec, identification defense, primary validity-threatening checks | Variable dictionary, balance/attrition details, placebo suites, secondary subgroup cuts |
| **Scope Extensions** | 1-paragraph takeaway ONLY if the mechanism shifts materially | Full extended model formulation, generalized proofs, sensitivity sweeps |

- **Separate Submission Split (Option B)**: If an accepted portal requires uploading the Electronic Companion as a standalone file (`online_appendix.pdf`), move everything from `\ECSwitch` into `online_appendix.tex` using `\documentclass[<journal>,...]{informs4}` + `\usepackage{xr}` (`\externaldocument{main}`) so `Theorem 1`, `(1)`, and `Online Appendix EC.1` numbers remain exact.

---

## 5. Publication-Grade `booktabs` Tables & Vector Figures

### Table Rules (`booktabs` + `threeparttable` + `siunitx`)
- **NEVER** use `\hline` or vertical column lines `|`. Use strictly `\toprule`, `\midrule`, `\bottomrule`, and `\cmidrule(lr){...}` for column groups.
- **Decimal Alignment & Consistent Precision**: Report 2–3 meaningful decimal places cleanly via `S[table-format=1.2]` (`siunitx`) or fixed formatting; show standard errors in parentheses beneath coefficients; place sample sizes $N$, fixed effects, R-squared/gaps, hardware/time limits, and plain-English variable definitions inside `\begin{tablenotes}` so every table stands alone.
- Every numerical pattern highlighted in prose must appear in the table, and every table must be interpreted by patterns in the body without reading rows aloud cell by cell (Iron Rule 5).

```latex
\begin{table}[t]
\centering
\begin{threeparttable}
\caption{Performance Comparison Across Demand Volatility Regimes}\label{tab:main}
\begin{tabular}{lcccc}
\toprule
 & \multicolumn{2}{c}{Low Volatility} & \multicolumn{2}{c}{High Volatility} \\
\cmidrule(lr){2-3} \cmidrule(lr){4-5}
Policy & Profit Gain (\%) & Stockout Rate (\%) & Profit Gain (\%) & Stockout Rate (\%) \\
\midrule
Static Benchmark & 0.00 & 8.42 & 0.00 & 15.18 \\
Adaptive Policy  & 1.32 & 6.95 & 4.83 & 10.74 \\
                 & (0.14) & (0.28) & (0.21) & (0.41) \\
\bottomrule
\end{tabular}
\begin{tablenotes}\small
\item \textit{Notes:} Profit gains are measured relative to the static newsvendor benchmark over $1{,}000$ out-of-sample test paths. Bootstrap standard errors appear in parentheses.
\end{tablenotes}
\end{threeparttable}
\end{table}
```

### Figure Rules (Schwabish / Tufte Principles)
- Export publication figures as **vector PDF** (matplotlib `bbox_inches="tight"`, R `ggsave`, Stata `graph export fig.pdf, replace`)—avoid blurry PNG/JPG unless showing photos/maps.
- Use `subcaption` for side-by-side panels (`0.48\textwidth`), keep uniform widths across the paper, label curves directly on the plot instead of bloated legends whenever legible, and avoid thin dotted lines that vanish in print.
- **No Table-vs-Figure Duplication**: Present each quantitative comparison in EITHER a table (exact regressions/benchmarks) OR a figure (time trends, event studies, RD jumps, policy thresholds, non-linear curves)—not both in the main body.
