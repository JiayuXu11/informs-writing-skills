# Selective Priority Triage & First-Submission ROI Framework

Use this reference in **Phase 3** of `informs-review-loop` after collecting all blind reviews for Round `r`.

The Coordinator's job is **NOT** to obey every reviewer mechanically. Real top-journal authors filter referee reports strategically—especially when preparing a **first submission**—fixing every foundational vulnerability and high-ROI weakness while refusing to bloat or derail the paper with low-ROI wishlist demands.

---

## 1. The Four-Bucket Priority Rubric (`P0` / `P1` / `P2` / `P3`)

Synthesize and deduplicate comments across all reviewers first (tag each merged issue with consensus count, e.g., `[3/3]` or `[1/3]`), then classify strictly into one of four buckets:

| Priority | Label | Criteria | Default Action in This Loop |
| :--- | :--- | :--- | :--- |
| **`P0`** | **Must-Fix Now (Foundation / Desk-Reject Killers)** | Threatens paper validity or causes `Desk Reject` / `Reject`: mathematical error, broken proof step, invalid empirical identification, missing core baseline comparator, unintelligible research question or storyline break, overclaiming beyond evidence, journal hard-rule violation (page cap, abstract cap, anonymity, broken PDF layout). | **Fix immediately** in this round. *(If fixing requires major new data/experiments/proofs not locally verifiable, pause and ask the user.)* |
| **`P1`** | **High-ROI First-Submission Upgrades** | High boost to reviewer rating for **low-to-moderate effort**: sharpening Abstract/Intro positioning, plain-English onboarding of paper-specific jargon at first mention, adding section-to-section and proposition-to-proposition storyline bridges, tightening proof sketches/intuition, replacing table/figure numeric readouts with trend-first prose, polishing figures/tables, stating assumptions/scope positively upfront, or running fast targeted checks using existing code/data. | **Fix in this round.** These convert borderline `Reject & Resubmit` / harsh `Major Revision` papers into crisp `Major`/`Minor Revision` submissions. |
| **`P2`** | **Defer to Future R&R (High Effort, Non-Foundational)** | Demands **heavy effort** (large new experiment suites, brand-new model extensions, extra multi-page theorems, collecting new datasets, secondary robustness batteries) that do **NOT** undermine the paper's core foundation and offer low effort-to-rating ROI on a **first submission** (or risk blowing past journal page caps). | **Defer cleanly** to `review_loop/deferred_rr_backlog.md`. Optionally add 1–2 concise sentences of honest scope framing in Model Setup or Future Work in Conclusion so the omission looks intentional and disciplined—not careless. |
| **`P3`** | **Decline / Clarify Misread** | Single-reviewer misreading of a claim already proven/shown in the paper, stylistic nitpick contradicting journal norms, or an out-of-scope demand asking for a different paper altogether. | **Decline** the structural change. If a reviewer genuinely misread the text, inspect *why* and apply a 1–2 sentence wording clarification at the confusing spot so future referees will not misread it either. |

---

## 2. The High-Effort Foundation Gate (Mandatory 3-Question Check)

Whenever a reviewer asks for **substantial new work** (e.g., new experimental benchmarks, new datasets, generalizing the core model, proving an extra major theorem, or rebuilding a major section), do **NOT** automatically classify it as `P0` or `P2`. Answer these three questions explicitly in `triage_plan.md`:

1. **Foundation Test**: *Without this addition, is the paper's central claim logically broken, empirically unidentified, or missing the single baseline every referee in this field expects?*
   - If **Yes** -> **`P0`** (cannot ignore; fix or escalate to user if external compute/data/modeling judgment is required).
   - If **No** -> proceed to Question 2.
2. **First-Submission Rating-Lift Test**: *Will adding this realistically raise the first-submission decision by a full tier (e.g., `Reject & Resubmit` -> `Major Revision`), or is it incremental frosting that adds 4 pages and dilutes the main story?*
   - Remember: INFORMS editors weigh **contribution-to-length ratio** strictly (`opre` <= 30 pp, `msom` <= 32 pp all-incl., `ijoc` <= 25 pp). Bloating an initial submission with speculative extensions often *lowers* the rating!
3. **R&R Deferral Test**: *Is this better kept as clean "R&R ammunition" to address ONLY if actual journal referees ask for it during revision?*
   - If **Yes** -> classify as **`P2`**, log in `review_loop/deferred_rr_backlog.md` with a 2-sentence sketch of how it would be executed during R&R, and tighten the manuscript's scope boundary positively upfront.

---

## 3. Consensus Weighting Heuristics

- **Multi-Model Consensus (`2/3` or `3/3` reviewers agree)**: Treat as a real manuscript signal—even if it sounds like "just exposition," when two distinct model families independently stumble over the same passage, definition, or proposition transition, human referees will stumble there too (`P0` or `P1`).
- **Single-Model Outlier (`1/3` reviewer)**: Scrutinize closely before acting. Accept as `P0` only if it catches a verifiable mathematical/empirical/factual error; accept as `P1` if it is a cheap, clearly beneficial clarity improvement; otherwise classify as `P2` or `P3`.

---

## 4. Required Triage Plan Structure (`review_loop/round_<rr>/triage_plan.md`)

Write a concise, auditable triage plan before touching any `.tex` file:

```markdown
# Round <r> Triage Plan (<TARGET_JOURNAL>)

## Panel Snapshot
- `rev1` (<model_1>): <Decision>
- `rev2` (<model_2>): <Decision>
- `rev3` (<model_3>): <Decision>
- `rev4` (<model_4>): <Decision> *(if 4-reviewer panel)*
- Convergence Status: CONTINUE (Need: all >= Major Revision AND >= 1 Minor Revision+)

## Prioritized Action Table
| ID | Consensus | Source(s) | Priority | Effort | Rating Lift | Decision & Concrete Plan |
| :--- | :---: | :--- | :---: | :---: | :---: | :--- |
| T1 | 3/3 | rev1, rev2, rev3 | P0 | Medium | High | ... |
| T2 | 2/3 | rev1, rev3 | P1 | Low | High | ... |
| T3 | 1/3 | rev2 | P2 | High | Low | Defer to R&R (does not affect core foundation; add 1-sentence scope note in Sec. 6) |
| T4 | 1/3 | rev3 | P3 | Low | Low | Reviewer misread Prop. 2; clarify sentence in Sec. 3.2 only |

## High-Effort Gate Notes (For Any High-Effort Item)
- **T3**: Foundation intact? Yes. First-submission lift? Marginal (+3 pp bloat risk). Verdict: Defer to `deferred_rr_backlog.md`.
```

---

## 5. Revision Execution Guardrails

1. **Zero Hallucination**: Never fabricate new experimental numbers, robustness tables, citations, or unproven lemmas to appease a reviewer. Only report numbers computed by real code or proofs actually verified step-by-step.
2. **Timeless Manuscript Prose**: Apply `informs-writing` standards to every edited paragraph—never leak review-loop history (`"to address the concern..."`, `"unlike the earlier draft..."`) into `.tex`.
3. **Preserve Strengths**: Respect the `What Works Well` points flagged by reviewers; never over-rewrite already strong passages.
4. **Prevent Scope Creep**: Watch page limits after every revision round so fixing `P0`/`P1` comments never pushes the manuscript over its target journal's page cap.
