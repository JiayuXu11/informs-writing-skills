---
name: informs-review-loop
description: >-
  Run an iterative multi-model blind peer-review and selective revision loop to
  raise an academic manuscript's first-submission rating (calibrated for INFORMS
  flagship journals OR, MS, M&SOM, IJOC, and adaptable to other journals). Spawns
  clean-context reviewer agents across distinct LLM families (e.g., Gemini,
  Claude, GPT) who inspect ONLY the compiled PDF with zero chat or revision
  history, triages their feedback by Impact vs. Effort (P0/P1/P2/P3) for an
  initial submission, applies high-ROI revisions while deferring non-foundational
  heavy work to future R&R, recompiles, and loops until EVERY reviewer gives at
  least Major Revision AND at least one reviewer gives Minor Revision (or higher).
---

# Multi-Model Blind Peer-Review & Rating-Improvement Loop (`informs-review-loop`)

Iteratively elevate a first-submission manuscript PDF through independent, clean-context multi-model peer review, disciplined Priority/ROI triage, and targeted manuscript revisions until the entire panel converges.

---

## Stopping Criterion & Loop Bounds

- **Target Convergence Condition (STOP & DELIVER)**:
  1. **Every** reviewer in the active panel assigns **`Major Revision` or higher** (zero `Desk Reject`, zero `Reject`, zero `Reject & Resubmit`), **AND**
  2. **At least one** reviewer assigns **`Minor Revision` or higher** (`Minor Revision` or `Accept`).
- **Safety Guardrails (Prevent Infinite Loops)**:
  - Default ceiling: **`max_rounds = 4`** (override if the user specifies a custom limit or runs under `/goal`).
  - **Plateau Exit**: If two consecutive rounds produce no rating improvement and every remaining blocker is a high-effort `P2` item (e.g., major new experiments or brand-new theorems requiring user decision), stop the loop cleanly and present the `P2` decision menu to the user.

---

## Core Non-Negotiable Invariants

1. **Strict Clean-Context Blind PDF-Only Review**:
   - Every reviewer agent starts with a **fresh conversation** (`swarm` without `fork`, or fresh `invoke_subagent`) and has **zero access** to prior chat turns, author intentions, `.tex` draft comments, Git history, or earlier review rounds.
   - Reviewers inspect **ONLY the compiled PDF** (via `read_file`) and write their structured review to their own isolated file (`review_loop/round_<NN>/<reviewer_id>.md`). On any shared swarm board, reviewers post ONLY a one-line completion signal (`DONE: <path>`) so **no reviewer ever reads another reviewer's verdict or earlier-round reviews**.
2. **True Cross-Model Diversity & Panel Size (No Artificial Topic Silos)**:
   - Call `swarm(action="models", all=true)` before Round 1 to discover currently available models across distinct model families and tiers (e.g., **Claude Opus**, **Claude Sonnet**, **Gemini Neon**, **GPT**).
   - **Panel quantity and model diversity are the priority**: spawn **3–4+ independent reviewers** across distinct models (never assign narrow topic silos like "only check math" or "only check writing"—every reviewer acts simply as an anonymous **Reviewer** evaluating the entire paper holistically, just like real peer review).
   - Never hardcode stale model IDs. If `swarm` is unavailable or only one model family is enabled, fall back cleanly to parallel `invoke_subagent` calls (and report the actual panel models to the user).
3. **Selective First-Submission Triage (No Blind Compliance)**:
   - The Coordinator never executes every reviewer comment blindly. Synthesize, deduplicate, and classify every comment into **`P0` / `P1` / `P2` / `P3`** using [triage-and-roi-framework.md](./references/triage-and-roi-framework.md), explicitly weighing **rating lift**, **foundation risk**, and **revision effort** for a **first submission**.
4. **Zero Fabrication & Zero Revision-History Leakage**:
   - Never invent numerical results, empirical findings, citations, or fake proofs to satisfy a reviewer. If a genuine `P0` flaw requires new simulations, data runs, or derivations that cannot be verified locally, run actual verification code/proofs or escalate clearly to the user.
   - All edits to `.tex` files must follow **`informs-writing`** standards (timeless reader-facing prose with zero meta-commentary such as *"In response to Reviewer 2..."* or *"Unlike the previous draft..."*). Keep all review logs strictly inside `review_loop/` (never inside manuscript `.tex`).
5. **Git Checkpoint Every Round**:
   - Ensure the manuscript workspace is Git-initialized before Round 1 (`checkpoint: pre-review-loop baseline`), add `review_loop/` to `.gitignore` (or keep it cleanly separated from manuscript commits), and commit each round's manuscript edits atomically (`revise(review-loop-r<N>): ...`).

---

## End-to-End Loop Procedure

### Phase 0: Pre-Flight Setup & Baseline PDF
1. Confirm **target journal** (`opre`, `mnsc`, `msom`, `ijoc`, or another named journal), **manuscript `.tex` root**, **compiled PDF path**, and **panel size** (default: **3–4 independent reviewers** maximizing distinct model families/tiers).
2. Verify the workspace Git status and create a clean baseline checkpoint if uncommitted changes exist.
3. Compile the baseline PDF if missing or stale (and copy/snapshot it to `review_loop/round_01/submission_r01.pdf` so reviewers inspect a frozen, self-contained PDF artifact with no source-tree hints).
4. Call `swarm(action="models", all=true)` and select as many distinct high-capability model families/tiers as fit the panel size (e.g., Claude Opus, Gemini Neon, GPT, Claude Sonnet).

### Phase 1: Parallel Clean-Context Blind Review (Round `r`)
1. Load [reviewer-personas-and-prompts.md](./references/reviewer-personas-and-prompts.md).
2. Do **NOT** partition reviewers into specialized sub-scopes or topic silos. Every agent is simply an independent anonymous **Reviewer** (`rev1`, `rev2`, `rev3`, `rev4`, ...) for `<TARGET_JOURNAL>` evaluating the **entire manuscript holistically**—letting natural model diversity surface blind spots and reveal genuine multi-reviewer consensus.
3. Spawn **all Round-`r` reviewers simultaneously in parallel** via `swarm(action="add", name="r<r>-rev<k>", model="<model_id>", workspace="inherit", brief=...)` (no `fork`!).
   - Each brief provides **ONLY**: (a) target journal & strict calibration rubric, (b) the instruction to review the full manuscript holistically as an anonymous Reviewer, (c) the frozen PDF path `review_loop/round_<rr>/submission_r<rr>.pdf`, and (d) the private output path `review_loop/round_<rr>/rev<k>_<model_slug>.md` with the required YAML decision header.
   - Each brief **explicitly forbids** reading `.tex` files, Git logs, `review_loop/` sibling files, or other swarm board messages, and instructs the worker to post ONLY `DONE: <output_path>` on the board after saving its review.
4. Wait for all Round-`r` reviewers to finish, then immediately **`swarm(action="kill", ...)`** all Round-`r` reviewer workers so Round `r+1` always starts from brand-new zero-memory workers.

### Phase 2: Automated Verdict Check & Stopping Gate
Run the round evaluator script from the skill root:

```bash
python "<skill_dir>/scripts/evaluate_review_round.py" "<project>/review_loop" --round <r>
```

- **Exit code `0` (`CONVERGED`)**: Every reviewer rated `>= Major Revision` AND at least one rated `>= Minor Revision`. Update `review_loop/scoreboard.md`, write the final summary report (including the `P2` Deferred-to-R&R Backlog for future journal rounds), and **STOP**.
- **Exit code `10` (`CONTINUE`)**: Convergence not yet reached. Proceed to Phase 3 (unless `r >= max_rounds` or a plateau is detected, in which case stop and present the remaining `P2` decisions to the user).
- **Exit code `2` (`INVALID`)**: A reviewer omitted or malformed its YAML decision header; inspect the file and re-run only that reviewer cleanly.

### Phase 3: Coordinator Synthesis & Selective Priority Triage (`P0 / P1 / P2 / P3`)
Read all Round-`r` review files and write `review_loop/round_<rr>/triage_plan.md` following [triage-and-roi-framework.md](./references/triage-and-roi-framework.md):

1. **Deduplicate & Cross-Reference**: Merge overlapping criticisms across reviewers (noting consensus weight, e.g., `[3/3 reviewers]` vs `[1/3 reviewer]`).
2. **Classify into Four Priority Buckets**:
   - **`P0` (Must-Fix Now)**: Foundation threats, fatal math/identification errors, missing core benchmark, severe positioning/storyline breaks, journal hard-rule violations, or layout defects that cause `Desk Reject` / `Reject`.
   - **`P1` (High-ROI First-Submission Polish)**: High rating impact for low-to-moderate effort (sharper Abstract/Intro, plain-English jargon onboarding, section/proposition transitions, tighter intuition/proof sketches, cleaner trend-first numerical prose, table/figure polish, clearer scope/assumptions, quick verification checks on existing code/data).
   - **`P2` (Defer to Future R&R — High Effort, Non-Foundational)**: Heavy new experiment suites, extra model extensions, or additional theorems that do **not** shake the paper's core foundation and have poor effort-to-rating ROI for an initial submission. Record in `review_loop/deferred_rr_backlog.md` (optionally add 1–2 sentences of honest upfront scope or Future Work).
   - **`P3` (Decline / Clarify Misread)**: Out-of-scope wishes, reviewer quirks contradicting journal norms, or misreadings (fix only the ambiguous sentence that triggered the misread—do not rebuild the model).
3. **High-Effort Foundation Gate**: Before committing to any high-effort revision (major new experiments, new theorems/extensions, or structural redesign), explicitly verify: *(i)* does omitting it shake the paper's core foundation, *(ii)* does it meaningfully lift the first-submission decision, and *(iii)* can it wait for R&R? If major new experiments or modeling changes are genuinely `P0` and require author approval or external compute/data, **pause and ask the user** before proceeding.

### Phase 4: Execute `P0 + P1` Revisions, Quality-Gate & Recompile
1. Apply approved **`P0`** and **`P1`** edits cleanly to the manuscript `.tex` (and code/figures if applicable), strictly following **`informs-writing`** conventions (all 7 Iron Rules, journal page/abstract caps, minimal explanatory parentheticals, trend-first numerical prose, storyline bridges, front-to-back readability).
2. Run `informs-writing`'s automated quality gates on the revised `.tex`:
   ```bash
   python "<informs_writing_dir>/scripts/audit_informs_draft.py" "<main.tex>" --journal <journal>
   python "<informs_writing_dir>/scripts/audit_manuscript_contract.py" "<main.tex>" --journal <journal>
   ```
3. Recompile the full PDF (multi-pass LaTeX + BibTeX) and run visual layout QA:
   ```bash
   python "<informs_writing_dir>/scripts/check_pdf_layout.py" "<main.pdf>" --render-flagged "<project>/review_loop/round_<rr>/pdf_qa"
   ```
   Inspect any flagged PNGs via `read_file` and fix layout/glyph/void defects before sending the PDF to the next review panel.
4. Commit the updated manuscript cleanly to Git (`revise(review-loop-r<r>): address P0/P1 blind review findings`), copy the fresh PDF to `review_loop/round_<r+1>/submission_r<r+1>.pdf`, and loop back to **Phase 1** for Round `r + 1`.

---

## Final Handoff Report (Upon Convergence or Stop)

Deliver a concise final report with clickable `file:///` links containing:
1. **Rating Trajectory Scoreboard** (`Round | Reviewer / Model | Decision | Key Bottlenecks Resolved`) from `review_loop/scoreboard.md`.
2. **Summary of Applied `P0` & `P1` Upgrades** (with Git commit hashes).
3. **`P2` Deferred-to-R&R Backlog** (`review_loop/deferred_rr_backlog.md`) so the author keeps a ready-made roadmap if real referees request those extensions during revision.
4. **Declined / Clarified `P3` Items** with brief rationale.
