# Manuscript Contract, Cross-Field Reviewer Calibration & Referee Responses

Use this reference when auditing or revising an entire manuscript, calibrating cross-disciplinary passages for `mnsc`/`msom`/`opre`, compressing a working paper to meet journal page caps, or drafting a Point-by-Point Referee Response Letter.

---

## 1. The 7-Field Paper Contract (`or-ms-writing`)

Every full INFORMS manuscript makes an implicit contract across sections. Audit all seven fields before polishing prose (mark a field N/A rather than inventing a comparator or managerial use the evidence does not support):

1. **Central Object**: The decision problem, construct, equilibrium, estimator, algorithm, or theorem family the paper studies.
2. **Headline Claim**: The single strongest claim an informed referee can verify from the body results.
3. **Comparator**: Current practice, static/myopic benchmark, offline oracle, commercial MIP solver, or control arm.
4. **Metric / Estimand**: Profit, total cost, consumer surplus, regret, competitive/approximation ratio, optimality gap, or ATT/LATE.
5. **Credibility Source**: Formal proof, natural/randomized variation, structural identification, out-of-sample validation, or reproducible benchmark suite.
6. **Boundary**: Exact assumptions, policy class, parameter regime, sample window, or hardware/time budget under which the claim holds.
7. **Consequence**: Which operational decision, bound, or methodological practice changes conditional on that boundary.

### How Each Section Transports the Contract (Without Copy-Pasting)
- **Abstract**: Compresses `{Object, Evidence, Headline Result, Comparator/Metric, Scope Boundary}` into math-free prose.
- **Introduction**: Motivates why the object matters and why standard approaches fail; previews credibility and findings upfront.
- **Model / Empirical Design**: Operationalizes exact actors, timing, constraints/variation, and benchmark.
- **Results**: Discharges the contract under fixed metric and comparator, separating headline claims from mechanisms and robustness.
- **Conclusion**: Interprets broader relevance and constructive future extensions **without widening** the policy class, population, or causal strength established in Results.
- **Online Appendix (`\ECSwitch`)**: Supplies proofs, helper lemmas, and secondary checks **without** being the first place a theorem's meaning or estimator's validity is explained.

---

## 2. Detecting & Fixing 9 Material Contract Drifts

Run `python "<skill_dir>/scripts/audit_manuscript_contract.py" <manuscript.tex> --journal <...>` and inspect the output for these nine defects before doing sentence polish:

1. **Object Drift**: Abstract promises `"dynamic assortment optimization"` while Model studies static single-product pricing.
2. **Comparator Drift**: Theorem benchmarks against a static rule, but Abstract claims superiority over `"all existing adaptive algorithms"`.
3. **Metric Drift**: Results analyze gross revenue, while Conclusion claims `"higher firm profit"` or `"consumer welfare"`.
4. **Evidence Drift**: Numerical simulations become `"empirical validation"` or OLS associations become `"causal impacts"`.
5. **Boundary Drift**: Results proved for affine/two-stage policies silently turn into unrestricted `"optimal policy"` claims in the Abstract/Conclusion.
6. **Magnitude Drift**: Rounded ranges, sample sizes, regret rates, or gap reductions contradict exact values in Results tables.
7. **Mechanism Drift**: Suggestive heterogeneity (`is consistent with`) escalates into `"proves the mechanism"`.
8. **Terminology Drift (Violates Iron Rule 6)**: Switching between *fulfillment gap*, *allocation shortfall*, and *service deficit* for the same quantity, or re-defining a concept in a later section.
9. **Appendix Dependence**: Body drops a theorem or robustness claim (`"see Online Appendix EC.3"`) with zero interpretation or proof checkpoint in the main text.

---

## 3. Cross-Field Reviewer Calibration (`or-ms-writing`)

Assume your referee is a sharp scholar in an **adjacent INFORMS subfield**, not an insider in every technique your paper combines:
- Write so an **OM empirical referee** follows a structural or game-theoretic model, an **econometrics referee** trusts operational institutional details, a **theory referee** follows algorithmic benchmarks, and an **OR referee** follows CS complexity/concentration notation.
- **3-Tier Knowledge Boundary**:
  1. *Assume*: Shared OR/MS fundamentals (convexity, Bellman equations, Nash equilibrium, OLS/2SLS, big-$O$ notation).
  2. *Bridge Once (4-Beat Chain)*: Any cross-field construct (e.g., Honest Causal Forest, Benders warm-start cuts, cross-moment regularity, incentive compatibility under delayed feedback)—bridge once into plain operational English, lock one canonical term, and preserve it.
  3. *Defer Verification*: KKT algebra, concentration tail constants, sensitivity grids -> `Online Appendix EC.x`.

### Locally Define These 11 Overloaded Terms Before Relying on Them
Never use these words without local disambiguation:
`causal` | `optimal` *(global vs within policy class $\Pi$ vs asymptotic)* | `equilibrium` *(Bayesian Nash vs stationary vs mean-field)* | `robust` *(distributionally robust vs statistically stable to alternative controls)* | `identification` *(econometric variation vs parameter uniqueness)* | `efficiency` *(cost vs allocative/Pareto vs runtime vs estimator variance)* | `fairness` *(group parity vs proportional vs envy-free)* | `welfare` *(total vs consumer surplus vs platform+worker)* | `learning` *(Bayesian vs bandit vs gradient vs human on-the-job)* | `platform` *(actor vs marketplace rule)* | `data-driven` *(nonparametric SAA vs contextual ML vs feature-based policy)*.

Also keep narrow outcome nouns separate: **demand**, **arrival rate**, **purchase incidence**, **adoption**, **conversion**, **engagement**, **surplus**, **profit**, and **revenue**.

---

## 4. Simulated 3-Referee Pre-Submission Audit & Page Compression

### Three-Referee Checklists
- **Referee 1 (Methodologist)**: Are assumptions explicit with analytical roles? Do proofs/designs genuinely establish every theorem/estimand? Are SE clusters, weak-IV/pre-trend tests, or solver baselines rigorous? Do all main-text proofs have sketches (`opre`/`ijoc`) and complete `Online Appendix EC.x` verification?
- **Referee 2 (Field Expert)**: Is the core trade-off/lever consequential for OR/MS? Are 3–5 closest papers engaged fairly and accurately (content-verified)? Are effect sizes economically/operationally meaningful relative to baselines?
- **Referee 3 (Writing Critic)**: Zero AI tells, zero orphan symbols, `<= 2` formal `Definition` blocks, zero prose decimal dumps, zero defensive caveats, zero chat/revision-history leakage, clean `booktabs` tables, and adherence to page cap?

### Working-Paper-to-Journal Compression Order
When trimming a bloated working paper to hit `opre` (30 pp), `mnsc` (32 pp 1.5x), `msom` (32 pp all-incl. + 16 pp EC), or `ijoc` (25 pp) caps, cut strictly in this sequence:
1. Redundant motivational paragraphs (throat-clearing openers).
2. Secondary literature tangents that do not define your departure.
3. Mechanical algebra, constants, and KKT verifications -> `Online Appendix EC.x` (leaving `Start -> Key Move -> Resulting Object`).
4. Secondary robustness tables and extra instance tables -> summarize patterns cleanly in prose and move full tables to `Online Appendix EC.x` (keeping validity-critical checks in body).
5. Redundant prose restatements repeating Abstract -> Intro -> Results -> Conclusion verbatim.

---

## 5. Point-by-Point Referee Response & Revision Letters

**Critical Isolation Rule (Iron Rule 7)**: All revision-log language (`"In response to Reviewer 2..."`, `"Unlike the previous version..."`, `"We have updated Theorem 1..."`) belongs **strictly inside the Response Letter**—ZERO trace of it may ever enter the `.tex` manuscript!

### Response Letter Structure
1. **Respectful Cover Summary (<= 1 page)**: Thank the Department/Area Editor, Associate Editor, and referees; summarize the 2–4 major structural revisions made across the paper (without defensiveness).
2. **Comment-by-Comment Format**:
   - Quote each referee comment verbatim (numbered `R1.1`, `R1.2`, ...).
   - **Direct Answer** first (agree + action taken, or respectful, evidence-backed clarification when declining a change).
   - **Exact Manuscript Action & Location**: State *(a) what changed*, *(b) exact section/page/table location (e.g., "Section 4.2, p. 14; Online Appendix EC.3")*, and *(c) brief excerpt or summary of new result/robustness check*.
3. **Auditability Invariant**: Clearly distinguish **completed revisions** implemented in the resubmitted `.tex` from future scope boundaries; never exaggerate what a new test or lemma proves.
