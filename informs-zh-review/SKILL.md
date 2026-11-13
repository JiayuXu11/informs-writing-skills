---
name: informs-zh-review
description: >-
  Generate readable Chinese PDF translations of an English paper's main text
  (excluding Online Appendix derivations) for rapid review, and synchronize
  user annotations/markups from an annotated Chinese PDF back into both the
  Chinese and English LaTeX manuscripts with Git version tracking. Use whenever
  the user asks to translate a manuscript/draft into a Chinese PDF for reading,
  or sends back an annotated Chinese PDF to update both the Chinese and English
  versions.
---

# Fast Main-Text Chinese Review & Bidirectional PDF Sync (`informs-zh-review`)

Enable rapid human reading of INFORMS manuscripts in Chinese PDF form—stripping out heavy Online Appendix proofs—and cleanly synchronize PDF highlights, strikeouts, sticky notes, and handwritten ink markups back into **both** the English and Chinese LaTeX sources under strict Git version control.

---

## 1. Mandatory Git Versioning Discipline

Core manuscript sources (`*.tex`, `*.bib`, and `zh_review/main_zh.tex`) MUST be tracked in Git before and after every operation.

1. **Pre-Flight Check**: Run `git status` in the project directory.
   - If not yet a Git repository: run `git init`, ensure `.gitignore` excludes LaTeX build artifacts and `zh_review/annot_snapshots/`, and create an initial baseline commit (`chore: baseline manuscript before zh-review`).
   - If uncommitted edits exist before applying PDF annotations: commit a clean checkpoint (`checkpoint: before applying <pdf_name> annotations`) so every change remains strictly reversible.
2. **Post-Sync Commit**: After compiling and verifying both updated sources, commit both English and Chinese `.tex` files atomically:
   `git add <en_tex_files> zh_review/main_zh.tex && git commit -m "sync(zh-review): apply annotations from <pdf_name>"`

---

## 2. Workflow A: Fast Main-Text EN -> ZH PDF Generation

Use when the user asks to translate an English `.tex` manuscript (or selected sections) into a Chinese PDF for quick review.

### Step 1: Scope Filter (Main Text Only, Skip Online Appendix)
- Translate **ONLY the main manuscript**:
  - Title, Abstract, Keywords
  - Main body sections (Introduction through Conclusion)
  - Formal Theorem, Proposition, Lemma, Corollary, Assumption, and Definition statements
  - Main-text Figures (referencing `../figures/...`), `booktabs` Tables, and numbered Algorithms
- **Strictly STOP at `\ECSwitch` / `\appendix` / Online Appendix**: Do NOT translate Online Appendix proofs, helper lemmas, or supplementary tables. Append one closing italicized note at the end of `zh_review/main_zh.tex`:
  `\textit{Note omitted Online Appendix notice in Chinese}` -> `\textit{注：Online Appendix（详细证明、辅助引理及补充数值实验）已按快速审阅模式略去。}`
- Skip translating the bibliography entries. Render in-text citations cleanly as `Author (Year)` or `(Author Year)` so compilation never stalls on BibTeX lookups.

### Step 2: 1-to-1 Structural Mirror & Sync Anchors
- Write the translated file to `zh_review/main_zh.tex` based on [ctex-review-template.tex](./templates/ctex-review-template.tex).
- Preserve **identical section numbering, equation numbering, theorem/proposition/lemma counters, figure/table numbers, and paragraph breaks** as the English source.
- Place a lightweight anchor comment immediately above every paragraph, theorem block, table, and displayed equation:
  ```latex
  % [EN-SYNC: main.tex:sec2:p3]
  ```
- Record the source English Git commit hash in the file header (`% Synced from ../main.tex @ <short_hash>`).

### Step 3: Translation Craft for OR/MS Scholars
- **Preserve 100% of Mathematical Content**: Keep all inline `$...$`, displayed equations, variables, and theorem conditions identical to the English manuscript.
- **Natural Chinese Academic Prose**: Write fluent, concise Chinese OR/MS prose—avoid stiff word-by-word translationese.
- **Terminology Lock**: Maintain a strict 1-to-1 Chinese-to-English term mapping matching the English manuscript's canonical terms. On first occurrence of key technical constructs, attach the canonical English term in parentheses (e.g., `base-stock policy`, `submodularity`, `cross-moment regularity`).

### Step 4: Compile, Visually Inspect & Commit
1. Compile inside `zh_review/` using `xelatex`:
   ```bash
   xelatex -interaction=nonstopmode -halt-on-error main_zh.tex
   xelatex -interaction=nonstopmode -halt-on-error main_zh.tex
   ```
   (On Windows, if `xelatex` is not on `PATH`, check `C:\texlive\2021\bin\win32\xelatex.exe`.)
2. Run `informs-writing`'s `check_pdf_layout.py` on `zh_review/main_zh.pdf` (`--render-flagged zh_review/annot_snapshots`) and inspect flagged or table/figure pages via `read_file` to catch missing CJK/math glyphs, overlapping text, blank pages, or oversized whitespace voids; remove temporary PNGs afterward.
3. Verify `zh_review/main_zh.pdf` exists with non-zero size and zero blocking visual/glyph defects, commit `zh_review/main_zh.tex` to Git (`feat(zh-review): generate main-text Chinese review PDF`), and present a clickable `file:///` link to `zh_review/main_zh.pdf`.

---

## 3. Workflow B: Annotated Chinese PDF -> Bidirectional EN + ZH Sync

Use when the user returns an annotated Chinese PDF (highlights, strikeouts, sticky notes, free-text comments, or iPad handwritten ink) and asks to update both versions.

### Step 1: Dual-Channel Annotation Extraction
Run [extract_pdf_annotations.py](./scripts/extract_pdf_annotations.py) to capture both embedded PDF annotations and visual page snapshots:

```bash
python "<skill_dir>/scripts/extract_pdf_annotations.py" "<annotated.pdf>" --render-dir "<project>/zh_review/annot_snapshots"
```

1. **Channel 1 (Structured `/Annot` Report)**: Read the script output listing every page number, annotation type (`Highlight`, `StrikeOut`, `Underline`, `Text`, `FreeText`, `Caret`, `Ink`), exact underlying Chinese text, surrounding context, and user comment.
2. **Channel 2 (Visual Inspection for Handwritten / Flattened Markups)**:
   - Open every rendered PNG in `<project>/zh_review/annot_snapshots/` with `read_file` to inspect handwritten margin notes, circled equations, arrows, or crossed-out phrases.
   - If the script reports `0 embedded /Annot objects` (common when tablet apps export flattened PDFs), inspect pages directly via `read_file` on the PDF or render pages with `--render-all-if-flat` so no handwritten markup is missed.

### Step 2: Map to `% [EN-SYNC: ...]` Anchors & Triage
- Match each PDF annotation to its exact `% [EN-SYNC: ...]` block in `zh_review/main_zh.tex` and the corresponding lines in the English `.tex` source.
- If a margin note is unambiguous (e.g., tighten intuition, fix a term, drop a symbol, rewrite an awkward claim, adjust scope), apply it directly. Only ask the user if an annotation poses an open modeling choice that alters theorem assumptions or mathematical truth.

### Step 3: Dual-Standard Bidirectional Editing
1. **Update the English `.tex` First (Enforcing `informs-writing` Standards)**:
   - Apply all 7 Iron Rules from `informs-writing`: zero orphan notation, intuition-first concept onboarding, concrete SVO prose, positive upfront conditions (no defensive disclaimers), patterns/rounded magnitudes in prose, strict definition & terminology lock, and **zero chat-context or revision-history leakage**.
   - **Critical Timeless-Prose Check**: Translate the *scholarly intent* of the user's Chinese annotation into native INFORMS English. NEVER write meta-text such as *"Unlike the previous version..."*, *"Following the correction..."*, or *"We updated..."*. The edited passage must read as if written cleanly from day one.
2. **Update `zh_review/main_zh.tex` in Lockstep**:
   - Mirror the updated English logic, wording, and notation identically in `zh_review/main_zh.tex` so both files stay 1-to-1 synchronized.

### Step 4: Audit, Recompile, Visually Inspect, Clean & Commit
1. Run `informs-writing`'s `audit_informs_draft.py` (and `check_prose_craft.py` on revised paragraphs) against the updated English `.tex` and resolve any flagged issues.
2. Recompile `zh_review/main_zh.pdf` with `xelatex` (and recompile the English PDF if `informs4.cls` is present).
3. Run `informs-writing`'s `check_pdf_layout.py` on the compiled PDF(s) (`--render-flagged zh_review/annot_snapshots`), inspect any flagged pages or revised tables/figures via `read_file`, and fix any glyph garbling, giant whitespace gaps, overlaps, or margin overflows before finishing.
4. Remove temporary `zh_review/annot_snapshots/` PNGs so binary snapshots do not clutter Git.
5. Commit both updated `.tex` files to Git (`sync(zh-review): apply PDF annotations from <pdf_name>`).
6. Present a concise **Revision Log Table** (`PDF Page | Annotation Summary | English Edit Location & Change | Chinese Sync Edit | Git Commit`) with clickable `file:///` links to the updated PDFs and `.tex` files.
