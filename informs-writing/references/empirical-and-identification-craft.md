# Empirical, Experimental & Structural Identification Craft (`mnsc` & `msom`)

Use this reference when drafting or revising quantitative empirical, behavioral/field-experimental, causal ML, or structural estimation manuscripts for **Management Science (`mnsc`)** and **M&SOM (`msom`)**. Never force theorem-and-proof terminology onto empirical sections—the **estimating design, construct validity, or identification equation** IS the model.

---

## 1. Data & Institutional Setting (Cochrane Rule: Answer Questions Before Asked)

1. **First-Sentence Rule**: Name the exact dataset/partner organization, sample period, geographic/operational scope, and unit of observation in the opening sentence of the Data section.
2. **Sample Construction & Cleaning Transparency**: Detail inclusion/exclusion filters, merge keys and match rates, missing-data rules, winsorization cutoffs, and final sample sizes in prose (summary counts in prose; step-by-step attrition waterfall in a `booktabs` table or `Online Appendix EC.x`). Never hide material sample restrictions in footnotes (and footnotes are prohibited in M&SOM).
3. **Plain-English Variables & Construct Validation**: Use readable variable labels (`Order Fulfilled Within 24 Hours`, never `fulfill_24h_flg`). When measuring latent constructs (calibration, managerial inattention, seller quality, task complexity), establish the four-link chain BEFORE interpreting regressions:
   `Construct Meaning -> Operational Elicitation / Observation -> Displayed Formula -> Coefficient Interpretation`.
4. **Descriptive & Balance Tables**: Include summary statistics ($N$, mean, SD, min/p25/p75/max) in the body. For RCTs and quasi-experiments, show covariate balance prominently near the design rather than burying it.

---

## 2. Identification-by-Design Exposition Blueprints

State the economic source of exogenous variation BEFORE writing regression algebra:

### A. Randomized Controlled Trials & Field Experiments (SUTVA / ITT / LATE)
- **Randomization & Balance**: Detail assignment level, stratification blocks, and randomization checks.
- **Compliance & Estimands**: Foreground **Intent-to-Treat (ITT)** as the primary conservative estimand; present **LATE / 2SLS** using assignment as an instrument for take-up clearly separated afterward. Report take-up rates explicitly.
- **Primary Threats**: Explicitly diagnose differential attrition, Hawthorne/demand effects, and **network/marketplace spillovers (SUTVA)**—especially critical in platform, queueing, and supply-chain field experiments. Cite pre-analysis plan registry IDs in the Introduction if pre-registered.

### B. Difference-in-Differences & Event Studies (`DiD`)
- **Institutional Shock**: Lead with the policy rollout, platform rule change, or disruption that creates treatment variation.
- **Parallel Trends & No Anticipation**: Devote a dedicated paragraph to the *economic* plausibility of parallel counterfactual paths (not merely `"pre-trends are insignificant"`). Explain what shocks hit both groups and why treatment timing is unrelated to outcome trends.
- **Mandatory Event-Study Plot**: Normalize $t = -1$ to zero, show at least 3–4 pre-periods, interpret dynamic ramp-up vs fade-out, and report **Rambachan–Roth HonestDiD** bounds against potential parallel-trend violations.
- **Staggered Treatment Timing**: Address TWFE negative-weight contamination directly (**Goodman-Bacon 2021** decomposition). Present both standard TWFE and heterogeneity-robust estimators (**Callaway & Sant'Anna 2021**, **Sun & Abraham 2021**, or **de Chaisemartin & D'Haultfoeuille 2020**), and use the robust estimator for the main event-study plot. Explain any divergence between TWFE and robust estimates.

### C. Instrumental Variables (`IV`) & Shift-Share / Bartik
- **Upfront Naming**: Name the instrument and economic source of variation in Section 1.
- **Relevance**: Report effective $F$-statistic (**Montiel Olea & Pflueger 2013**) or Kleibergen–Paap $F$ (do NOT rely solely on old $F > 10$ heuristics). If weak/moderate, report **Anderson–Rubin** confidence intervals and **Lee et al. (2022) $tF$** adjustments.
- **Exclusion & Monotonicity**: Dedicate a full paragraph to defending why the instrument affects outcomes *only* through the endogenous variable, characterize who the **compliers** are (distinguishing **LATE** from ATE), and explain why IV differs from OLS (selection vs measurement error vs local compliance).
- **Shift-Share / Bartik**: Explicitly state whether identification comes from **exogenous initial shares** (Goldsmith-Pinkham, Sorkin, & Swift 2020) or **quasi-random shocks** (Borusyak, Hull, & Jaravel 2022), plus leave-one-out sensitivity.

### D. Regression Discontinuity (`RDD`)
- **Running Variable & Plot**: Name the assignment score and cutoff upfront; make the binned **RD plot** Figure 1.
- **Manipulation & Smoothness**: Show **McCrary / Cattaneo–Jansson–Ma** density test at the threshold, rule out confounding policy jumps at the same cutoff, report local-polynomial estimates with optimal bandwidth (**Calonico, Cattaneo, & Titiunik**), show bandwidth sensitivity, and address **local-to-cutoff** external validity. For fuzzy RDD, display both first-stage jump and reduced-form jump.

### E. Structural Estimation & Counterfactuals (`mnsc` / `msom`)
- **Model as Measurement Device**: Show clearly which variation in the data identifies which structural primitives (preferences, switching costs, search frictions, beliefs). Do not leave identification hidden inside maximum-likelihood equations.
- **Validation Before Counterfactuals**: Demonstrate in-sample fit AND out-of-sample or holdout validation before interpreting counterfactual policy welfare/profit simulations. Keep what is *observed in data*, *estimated structurally*, and *simulated counterfactually* visibly distinct.

### F. Causal Machine Learning (Double ML / Causal Forests)
- State clearly whether ML serves **prediction, heterogeneous treatment effects (Causal Forests; Wager & Athey 2018)**, or **high-dimensional nuisance control (Double/Debiased ML; Chernozhukov et al. 2018)**. Detail **honest sample-splitting / cross-fitting** and benchmark against transparent parametric specifications.

---

## 3. Inference, Magnitudes, Bad Controls, Mechanisms & Null Results

1. **Avoid Bad Controls**: Never include post-treatment intermediate outcomes (e.g., controlling for order volume when treatment changes order volume and price) as regression covariates—they induce selection bias rather than isolating direct effects (Angrist & Pischke §3.2.3).
2. **Standard Error Clustering & Few Clusters**: Cluster at the level of treatment assignment/correlation, and state the clustering level in every table note. When clusters `< ~40` (or unbalanced), supplement asymptotic SEs with **wild cluster bootstrap** (Cameron, Gelbach, & Miller 2008) or **randomization inference**.
3. **Specification Progression & Oster Bounds**: Build regression columns from parsimonious (basic controls/FEs) to full controls so readers see coefficient movement and $R^2$ change; report **Oster (2019)** selection bounds rather than claiming coefficient stability alone proves exogeneity.
4. **Prose Magnitudes vs Table Precision (Harmonized with Iron Rule 5)**:
   - Interpret **economic significance** relative to the dependent variable's sample mean, SD, or an operational cost benchmark (*"a shift equal to roughly one-fifth of the baseline cancellation rate"*).
   - Keep exact multi-decimal coefficients (`0.384*** (0.091)`) strictly inside `booktabs` tables; state clean rounded patterns and orders of magnitude in prose.
5. **Testing Mechanisms (Not Speculating)**: Structure mechanism subsections rigorously: *(1) Channel M predicts subgroup/proxy shift Z -> (2) Test Z empirically -> (3) Separate M from rival explanations*. When a channel is only suggestive, use `suggests` or `is consistent with`, never `"proves"`.
6. **Multiple Testing & Informative Null Results**: Apply **Holm / Benjamini–Hochberg / Anderson sharpened FDR $q$-values** when testing multiple outcomes or post-hoc subgroups. Frame null findings via tight **confidence intervals and statistical power** (*"we can rule out effects larger than roughly 2% of baseline throughput"*) rather than misinterpreting $p > 0.10$ as zero effect.
7. **Reproducibility Packages (`mnsc` Data & Code Disclosure)**: Maintain clean `data/raw/`, `data/analysis/`, `code/`, `results/` separation with one config path script and a table-to-script manifest (`Table 2 -> code/table2_main.do`), referencing availability cleanly as required by `mnsc` and `ijoc`.
