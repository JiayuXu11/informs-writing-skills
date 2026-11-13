# Visual Design Aesthetics & Compiled-PDF Layout QA

A manuscript's visual polish shapes referee first impressions as strongly as its prose. Never evaluate layout, tables, or figures from `.tex` source alone: always compile the PDF, run [check_pdf_layout.py](../scripts/check_pdf_layout.py), and visually inspect rendered pages.

---

## 1. Publication-Grade Table Aesthetics

INFORMS tables must look crisp, uncrowded, and scannable at reading magnification:

1. **Flush Edges & Rule Hierarchy**:
   - Strip extraneous outer padding with `@{}l ... r@{}` in column specifications so `\toprule`, `\midrule`, and `\bottomrule` align flush with left and right column edges.
   - Use thin trimmed group rules `\cmidrule(lr){2-4}` under spanning headers (`\multicolumn{3}{c}{...}`), never full-width secondary lines or vertical `|` bars.
2. **Vertical Breathing Room**:
   - Set `\renewcommand{\arraystretch}{1.12}` (inside the `table` environment so prose line spacing is untouched) and insert `\addlinespace[4pt]` between logical panels or model blocks.
3. **Decimal Alignment & Uniform Precision**:
   - Align numerical columns with `siunitx` (`S[table-format=2.2]`) or fixed-decimal formatting; center `Yes`/`No` indicator rows and place standard errors cleanly in parentheses beneath estimates.
   - Match decimal places within each metric across all rows and columns.
4. **Anti-Cramming Rule (Avoid `\resizebox` Distortion)**:
   - Do **not** wrap wide tables in `\resizebox{\textwidth}{!}{...}` unless strictly unavoidable; blind scaling shrinks body fonts below `7 pt`, washes out `booktabs` rule weights, and looks amateurish.
   - Fix wide tables structurally instead: shorten column labels by moving units/subheaders to a second header row, tune `\setlength{\tabcolsep}{4.5pt}`, step font down at most once to `\small` or `\footnotesize`, pivot tall-and-narrow, use `sidewaystable`, or defer exhaustive grids to `Online Appendix EC.x`.
5. **Notes & Caption Discipline**:
   - Put scope, sample count $N$, cluster level, and significance stars inside `threeparttable`'s `tablenotes` (`\footnotesize`), keeping captions crisp (`<= 12` words). Notice `informs4.cls` uses custom caption formatting—avoid loading `\usepackage{caption}` unless verified error-free on your `informs4.cls` version.

### Canonical `booktabs` + `threeparttable` Template

```latex
\begin{table}[tbp]
\centering
\renewcommand{\arraystretch}{1.12}
\setlength{\tabcolsep}{5pt}
\begin{threeparttable}
\caption{Main Benchmark Comparison Across Demand Regimes}
\label{tab:main_comparison}
\begin{tabular}{@{}lcccc@{}}
\toprule
& \multicolumn{2}{c}{Low Volatility} & \multicolumn{2}{c}{High Volatility} \\
\cmidrule(lr){2-3} \cmidrule(lr){4-5}
Policy & Cost & Gap (\%) & Cost & Gap (\%) \\
\midrule
Myopic FIFO        & 14.82 & 6.41 & 19.35 & 9.12 \\
Fixed Threshold    & 14.11 & 1.31 & 18.04 & 1.73 \\
Adaptive Index     & 13.93 & 0.00 & 17.73 & 0.00 \\
\addlinespace[4pt]
Instance Count     & \multicolumn{2}{c}{120} & \multicolumn{2}{c}{120} \\
\bottomrule
\end{tabular}
\begin{tablenotes}
\footnotesize
\item \textit{Notes.} Gaps are relative to the hindsight DP lower bound; all runs use common random numbers.
\end{tablenotes}
\end{threeparttable}
\end{table}
```

---

## 2. Publication-Grade Figures & Visualizations

1. **Vector First**:
   - Export line charts, event-study plots, equilibrium diagrams, and policy thresholds as **vector PDF** (matplotlib `savefig(..., bbox_inches="tight")`, R `ggsave`, Stata `graph export fig.pdf, replace`) or native `TikZ`/`PGFPlots`.
   - Use PNG only for dense spatial maps or high-count heatmaps (`>= 300 DPI`).
2. **Target-Width Canvas Sizing**:
   - Create plots near final column width—e.g., `figsize=(6.0, 3.6)` inches for a full-width figure or `(3.1, 2.7)` per panel for 2-up subfigures—so axis tick labels and annotations render at **8–10 pt** on paper without squinting.
3. **Typography Matching**:
   - Match LaTeX serif/math typography (`Computer Modern`, `Latin Modern`, or `Times`; in matplotlib set `"font.family": "serif"` and `"mathtext.fontset": "cm"`). Never leave oversized 16 pt sans-serif defaults next to 10 pt Times prose.
4. **Colorblind-Safe + Grayscale-Redundant Palettes**:
   - Use restrained, high-contrast academic palettes (e.g., Deep Navy `#1B365D`, Teal `#008080`, Vermilion `#D55E00`, Slate `#64748B`)—never neon RGB primaries (`#FF0000`, `#00FF00`) or rainbow colormaps.
   - Always pair color with **distinct line styles** (`solid`, `dashed`, `dashdot`, `dotted`) and sparse markers so printed grayscale copies remain 100% distinguishable.
5. **Minimal Ink & Direct Callouts**:
   - Remove top and right axis spines, drop dark heavy gridlines (keep subtle `#E2E8F0` horizontal guides only if reading values matters), use light semi-transparent confidence bands (`alpha=0.15`), and label curves/thresholds ($\tau^*$) directly on the plot instead of floating boxed legends.

---

## 3. Mandatory Compiled-PDF Visual Inspection Loop

Text-clean `.tex` files can still compile into broken PDFs. Whenever a TeX engine (`pdflatex`, `xelatex`, or `latexmk`) and `informs4.cls` (or `ctexart` for `zh_review`) are available:

1. **Full Multi-Pass Compile**: Run LaTeX -> BibTeX (if `.bib` used) -> LaTeX x2 so cross-references, page numbers, and `EC.` labels resolve completely.
2. **Automated PDF Layout & Glyph Audit**:
   ```bash
   python "<skill_dir>/scripts/check_pdf_layout.py" path/to/main.pdf --render-flagged /tmp/pdf_qa
   ```
   This inspects text extraction, bounding-box overlaps, pixel-row blank bands / underfilled pages, margin protrusions, and the companion `.log` (`Missing character`, `Overfull \hbox`, `Underfull \vbox`).
3. **Human-Like Visual Page Inspection (`read_file`)**:
   - Open every rendered PNG flagged by `check_pdf_layout.py`—plus key visual pages (title/abstract, main results table page, figure pages, and the `\ECSwitch` transition)—using `read_file` to verify alignment, spacing balance, label legibility, and overall aesthetic harmony.
4. **Remediate & Re-Verify**: Fix any defect in `.tex` (or regenerate undersized figures), recompile, and re-run `check_pdf_layout.py` until exit code `0` with clean visuals.

---

## 4. Compiled-PDF Defect Triage & LaTeX Remediation

| Visual / PDF Symptom | Root Cause in LaTeX / Assets | Concrete Remediation |
| :--- | :--- | :--- |
| **Garbled characters, replacement tofu (`U+FFFD`), `¡`/`¿`, or missing math/CJK glyphs** | Pasted Unicode (`−`, `“`, `”`, `α`, non-breaking space) under `pdflatex`; missing `fontenc`; missing CJK glyph under `xelatex` fontset | Add `\usepackage[T1]{fontenc}`; replace raw Unicode minus `−` with ASCII `-` in math and smart quotes with `` `` '' ``; inspect `.log` `Missing character:` lines; switch CJK fontset only in `zh_review` if needed |
| **`??`, `[?]`, or broken EC pointers** | Incomplete single-pass compile or mistyped `\label`/`\ref` key | Run full `pdflatex -> bibtex -> pdflatex -> pdflatex`; verify matching `\label{...}` spelling |
| **Large mid-page or bottom-of-page blank whitespace gaps** | Restrictive `[h]`/`[H]` float specifiers forcing huge tables/figures onto next page; tall unbreakable `align` blocks; `Underfull \vbox` vertical glue stretching | Switch floats to `[tbp]` or `[htbp]`; add `\allowdisplaybreaks[1]` in preamble; split giant multi-panel figures or widen `\textfloatsep` carefully; add `\raggedbottom` if block glue stretches excessively |
| **Blank interior pages** | Explicit `\clearpage`/`\cleardoublepage` stacked with oversized float queues or `openright` | Replace unnecessary `\clearpage` calls inside main body; avoid `[p]`-only float traps |
| **Overlapping lines or colliding table columns** | Negative `\vspace{-...}` hacks, overlapping `TikZ` coordinates, or manual column widths (`p{1cm}`) overflowing adjacent cells | Delete negative `\vspace{-...}`; add `\raggedright` or wider `p{...}` / `tabularx` `X` columns; re-export figures with `bbox_inches="tight"` |
| **Text or equations protruding into margins (`Overfull \hbox`)** | Long inline math without breakpoints, missing `microtype`, unbreakable URLs/code, or wide tables | Add `\usepackage{microtype}`; break long display math across `multline*` or `aligned`; use `\url{...}`; trim `\tabcolsep` or split headers |
