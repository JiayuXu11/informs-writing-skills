# Section Architecture, Lane Blueprints & Citation Close-Reading

Use this reference when choosing titles, structuring sections across different OR/MS research lanes, organizing paragraphs, testing passage logic, or auditing Related Work citations. The core rule from full-text INFORMS close reading is simple: **structure follows evidence dependency, never a rigid one-size-fits-all template**.

---

## 1. Title Craft (Cochrane / INFORMS Precision)

- Keep titles concise (**<= 12 words** ideal, `<= 15` upper bound) and informative to an adjacent-subfield scholar in one glance.
- **Name Object + Lever/Mechanism + Setting/Outcome**, not methodology fluff:
  - *Empirical / Field*: `"Delayed Price Updates and Demand Estimation: Evidence from Retail Analytics"` or `"The Impact of [Lever] on [Outcome]: Evidence from [Setting]"`.
  - *Theory / Applied OR*: `"Adaptive Assortment Optimization Under Censored Demand"` or `"Unit Commitment Without Commitment"`.
  - *Computational / IJOC*: `"Branch-and-Price for Multi-Compartment Vehicle Routing with Stochastic Demands"`.
- **Avoid**: `"A Study on..."`, `"On Various Factors..."`, `"An Empirical Investigation of..."`, or method-only labels (`"A Difference-in-Differences Analysis of..."`) unless inventing the estimator itself.

---

## 2. Eight Lane-Specific Macro Architectures

Match section titles and sequence to what persuades a referee in your specific lane (use concrete object-naming noun headings—never rhetorical placeholders like `Motivation`, `Story`, `Key Takeaway`, or `Our Approach`):

1. **Analytical Theory (Queueing, Game Theory, Mechanism Design, Pricing)**:
   `1. Introduction` -> `2. Related Literature` *(or §1.2)* -> `3. Model Setup` (physical timing, agents, information, objective, benchmark) -> `4. Equilibrium / Policy Characterization` -> `5. Extensions` *(only if mechanism/scope shifts meaningfully)* -> `6. Conclusion` -> `Online Appendix (\ECSwitch)`.
2. **Applied Dynamic Programming & Stochastic Control (OR / M&SOM)**:
   `1. Introduction` *(with §1.2 Related Literature)* -> `2. System Model & Operating Constraints` *(plain operational workflow before matrices)* -> `3. Lagrangian Relaxation & Dual Bounds` -> `4. Implementable Policies & Optimality Guarantees` -> `5. Numerical Study` -> `6. Conclusion` -> `Online Appendix (\ECSwitch)`.
3. **Optimization & Algorithms (`opre` / `ijoc` Method Papers)**:
   `1. Introduction` -> `2. Problem Formulation & Structural Properties` -> `3. Exact / Decomposition Algorithm` *(numbered `algorithm` pseudocode)* -> `4. Computational Experiments` *(hardware, solver versions, time limits, instance suites, ablation)* -> `5. Conclusion` -> `Online Appendix (\ECSwitch)`.
4. **Software & Package Papers (`ijoc` Dual-DOI Track)**:
   `1. Introduction` -> `2. Package Architecture & Data Structures` -> `3. Core Algorithmic Components & API Design` -> `4. Computational Benchmarks & Usage Examples` *(including `.cd` replication details)* -> `5. Conclusion` -> `Online Appendix (\ECSwitch)`.
5. **Online Learning, Bandits & Prescriptive Analytics**:
   `1. Introduction` -> `2. Problem Formulation & Oracle Benchmark` -> `3. Regret Lower Bound` *(when hardness motivates policy design)* -> `4. Policy Construction & Finite-Sample Guarantees` -> `5. Case Study / Simulations` -> `6. Conclusion` -> `Online Appendix (\ECSwitch)`.
6. **Quasi-Experimental Empirical OM (DiD, IV, RDD, Archival)**:
   `1. Introduction` -> `2. Institutional Setting & Conceptual Predictions` -> `3. Data & Sample Construction` -> `4. Empirical Strategy & Identification` -> `5. Main Results` -> `6. Mechanisms & Alternative Explanations` -> `7. Robustness Tests` *(validity-critical checks in body; secondary cuts in EC)* -> `8. Conclusion` -> `Online Appendix (\ECSwitch)`.
7. **Behavioral / Field Experiments**:
   `1. Introduction` -> `2. Conceptual Framework & Experimental Design` *(arms, randomization unit, protocol)* -> `3. Data, Balance & Attrition` -> `4. Treatment Effects` -> `5. Mechanism Tests & Follow-Up Experiments` -> `6. Discussion & Conclusion` -> `Online Appendix (\ECSwitch)`.
8. **Structural Estimation & Counterfactuals**:
   `1. Introduction` -> `2. Institutional Setting & Descriptive Facts` -> `3. Structural Model` -> `4. Identification & Estimation` -> `5. Model Fit & Out-of-Sample Validation` -> `6. Counterfactual Analysis` -> `7. Conclusion` -> `Online Appendix (\ECSwitch)`.

---

## 3. Heading Discipline & Paragraph Craft

### Heading Depth Rule
- Add a `\subsection` ONLY when the reader switches to a genuinely new formal object, construct, dataset component, result family, or validity threat (e.g., `Data Sources`, `Sample Construction`, `Parallel Trends Validation`, `Alternative Explanations`, `Fluid Benchmark`).
- Use `\subsubsection` sparingly—only for parallel outcomes or parallel algorithms referees may look up independently. Never create one-paragraph subsections or tiny headings (`Intuition`, `Discussion`, `Interesting Observation`); integrate interpretation in ordinary prose right beside the theorem or table.

### Four Kinds of Paragraph Coherence (`or-ms-writing`)
Do NOT force every paragraph into a mechanical `"Topic Sentence -> 3 Bullets -> Teaser Ending"` mold. A paragraph succeeds when it has one recoverable primary burden and satisfies all four checks:
1. **Referential Coherence**: Stable nouns, symbols, and clothed demonstratives (`"this bound"`, not naked `"this"`).
2. **Prerequisite Coherence**: Every term, actor, timing event, and benchmark appears BEFORE a later claim depends on it.
3. **Inferential Coherence**: The theorem, estimate, design feature, or decomposition visibly warrants the claim drawn from it.
4. **Scope Coherence**: Metric, population, policy class, and evidence type remain fixed unless an explicit scope transition is signaled.

Depending on local burden, **Claim-first**, **Result-first**, **Definition-first**, **Evidence-first**, and **Contrast-first** orders are all legitimate. Close a paragraph cleanly once its burden is discharged—avoid artificial forward teasers before an obvious next heading.

### Two Quick Structural Stress Tests (`conorbronsdon` + `or-ms-writing`)
1. **Paragraph-Reshuffle Immunity Test**: Try mentally swapping two body paragraphs. If nothing breaks, the section reads like an unordered list rather than a dependency chain; establish what prerequisite each earlier paragraph supplies to the next.
2. **Treadmill / Information-Density Test**: If a paragraph restates an earlier claim in fresher adjectives without adding a new assumption, warrant, magnitude, mechanism, or boundary, cut it.

---

## 4. Related Work & Citation Close-Reading Discipline

### Non-Negotiable Content-Fit Rule
**Never judge whether a citation supports a sentence from title, abstract, BibTeX metadata, citation count, or LLM memory.**
When any claim relies on a cited paper, verify five facts against the cited paper's actual full text (Introduction, Model/Design, Results/Tables, or Appendix):
1. **Object**: What decision, system, dataset, or theorem the paper actually studies.
2. **Support Type**: Formal theorem, identification design, structural counterfactual, simulation, lab/field experiment, or conceptual note.
3. **Exact Claim Used Here**: The specific theorem, parameter, or empirical finding your sentence invokes (prefer published journal version over outdated working paper numbers).
4. **Boundary**: Assumptions, policy class, sample period, or benchmark under which that result holds.
5. **Fit Role**: Background precedent, methodological tool, direct benchmark, contrast, or mechanism support.

If full text cannot be inspected, mark the citation support explicitly as **unverified** for the user rather than guessing or over-claiming.

### Common Citation Misfits to Catch
- Citing a theoretical model prediction as if it were empirical evidence, or an observational correlation as if it were causal.
- Citing a method paper (`Method X exists`) as proof that Method X outperforms in your setting.
- Clustering 6–10 citations after a generic sentence (`"A large literature studies dynamic pricing [1–8]."`). Instead, synthesize **what the stream establishes** and identify the **exact analytical or empirical dimension** on which your setting departs (timing, censoring, strategic incentives, decentralized information, or benchmark).
- **Avoid Mechanical Gap Loops**: You do NOT need to end every single literature paragraph with `"However, none of these papers consider X."` Synthesize the stream cleanly and state the collective point of departure once per conceptual group.
