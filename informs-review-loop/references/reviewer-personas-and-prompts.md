# Clean-Context Blind Reviewer Calibration & Brief Template

Use this reference in **Phase 1** of `informs-review-loop` to assemble a diverse multi-model blind review panel that mirrors real flagship journal standards (no sycophancy, no artificial scope silos, zero history leakage).

---

## 1. Strict Decision Scale & Calibration Bar

Every reviewer MUST select exactly ONE canonical decision from the scale below, calibrated to the **target journal's real acceptance bar** (e.g., INFORMS flagship `opre` / `mnsc` / `msom` / `ijoc` acceptance rates of ~8%–15%):

| Canonical Decision | Rank | Operational Meaning (First-Submission Calibration) |
| :--- | :---: | :--- |
| **`Desk Reject`** | `0` | Out of scope, severe journal hard-rule violation (e.g., gross page-cap breach, missing structured abstract, unreadable draft), ungrounded/broken central claim, or clearly below flagship contribution threshold. |
| **`Reject`** | `1` | Fundamental flaw in core model, proofs, identification, or computational benchmark; thin or incremental contribution whose fix requires rewriting a different paper. |
| **`Reject & Resubmit`** | `2` | Promising core idea or setting, but serious structural gaps (e.g., unconvincing mechanism, weak/missing primary benchmark, major proof or empirical validity holes, poor storyline) make standard R&R too risky without major reconstruction. |
| **`Major Revision`** | `3` | **Strong flagship potential**: core contribution, formulation, and main results are credible and publishable in principle, though substantial but bounded revisions are needed. |
| **`Minor Revision`** | `4` | **Near-ready first submission / polish stage**: storyline, rigor, contribution, and presentation meet the target journal's high bar; remaining issues are minor clarifications, polish, or secondary notes. |
| **`Accept`** | `5` | Publishable essentially as-is (rare on a first submission; reserve only for truly spotless manuscripts). |

**Anti-Inflation Rule**: Remind every reviewer explicitly that **politeness hurts the author**. Giving `Minor Revision` to a paper with weak positioning, broken logic, opaque jargon, or questionable benchmarks gives false confidence that leads to real desk-rejections. Be tough, fair, constructive, and specific.

---

## 2. Panel Size & Multi-Model Diversity (No Artificial Topic Silos)

**Quantity and genuine model diversity are what make the panel strong—NOT artificially restricting each reviewer to a narrow topic silo.**

1. Before Round 1, call `swarm(action="models", all=true)` and pick **3–4+ independent reviewers** (`rev1`, `rev2`, `rev3`, `rev4`, ...) spread across **as many distinct model families and tiers as available**, for example:
   - `rev1` -> **Claude Opus** (e.g., `claude-opus-5-5-high`)
   - `rev2` -> **Gemini Neon** (e.g., `gemini-4-neon-xhigh` or `gemini-4-neon-high`)
   - `rev3` -> **GPT** (e.g., `gpt-oss-120b-medium`, or top available GPT model)
   - `rev4` *(recommended for 4-reviewer panels)* -> **Claude Sonnet** or another distinct Gemini family (e.g., `claude-sonnet-5-5-high` or `gemini-4-hydrogen-high`)
2. **Do NOT assign narrow focus scopes** (do NOT say "Reviewer 1 only checks proofs, Reviewer 2 only checks exposition"). Every reviewer receives the **exact same holistic Reviewer brief** and evaluates the entire paper freely—covering whatever aspects most affect the editorial decision (novelty, rigor, proofs/identification, benchmarks, storyline, readability, formatting, journal fit).
3. Why holistic + diverse beats narrow silos:
   - Real journal referees evaluate the whole paper, not isolated slices.
   - When 3 different model families *unprompted* flag the same flaw, you gain true high-signal consensus (`3/3`), whereas artificial silos prevent cross-verification.
   - Always spawn brand-new zero-memory workers via `swarm(action="add", ...)` each round after killing the previous round's workers.

---

## 3. Mandatory Clean-Context Reviewer Brief Template

Pass this exact structure as the `brief` in `swarm(action="add", ...)` for **every** reviewer (substituting ONLY the bracketed fields—never leak chat history, prior reviews, or author excuses):

```markdown
You are an independent, anonymous **Reviewer** for **<TARGET_JOURNAL>** evaluating a **first-time submission**.

### Strict Blind & Clean-Context Protocol (NON-NEGOTIABLE)
1. Inspect **ONLY** the compiled PDF file at: `<FROZEN_PDF_PATH>` (read it via `read_file`, inspecting both text and rendered layout/tables/figures).
2. Do **NOT** read any `.tex` source files, Git logs, scripts, sibling review files, or other messages on the swarm board.
3. Do **NOT** assume any prior revisions occurred—judge this PDF cold as an initial submission against `<TARGET_JOURNAL>`'s real flagship acceptance bar.
4. Evaluate the **entire manuscript holistically**—raise whichever substantive, methodological, empirical/computational, positioning, exposition, or formatting issues matter most to your editorial judgment.
5. Be rigorous, candid, and constructive. Do NOT inflate your rating out of politeness.

### Required Output File & Exact Format
Write your complete review to: `<OUTPUT_MD_PATH>` (using `write_file` with `Overwrite=true`).
The file MUST begin with this exact YAML frontmatter block (so automated evaluation can parse your verdict):

---
reviewer: <REVIEWER_ID>
model: <MODEL_ID>
journal: <JOURNAL_CODE>
round: <ROUND_NUM>
decision: <ONE OF: Desk Reject | Reject | Reject & Resubmit | Major Revision | Minor Revision | Accept>
confidence: <High | Medium | Low>
---

Follow the frontmatter with these sections:
1. `## Overall Assessment & Verdict Rationale` (3–5 crisp sentences explaining why this decision—not one tier higher or lower—is warranted for `<TARGET_JOURNAL>`).
2. `## Fatal & Major Issues` (numbered list; for each issue specify `[Severity: Fatal | Major]`, exact `Location` such as `Abstract`, `Section 2.1, p. 6`, `Proposition 2`, `Table 2`, concise `Diagnosis`, and `Concrete Fix`).
3. `## Moderate & Minor Issues` (numbered list with `[Severity: Moderate | Minor]`, exact `Location`, `Diagnosis`, and `Concrete Fix`).
4. `## What Works Well` (2–3 concrete strengths to preserve during revision).

### Board Signal Rule (Prevent Cross-Reviewer Contamination)
After writing `<OUTPUT_MD_PATH>`, post ONLY this single line on the board and nothing else (do NOT paste your decision or review text onto the board):
`DONE: <OUTPUT_MD_PATH>`
```
