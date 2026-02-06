# D1+D4 Paper Status

## Paper Information
- **Title**: When AI Is Confidently Wrong: Calibration and Risk Analysis of Large Language Models in Financial Decision-Making
- **Target Journal**: Finance Research Letters (FRL), SSCI Q1
- **Status**: DRAFT COMPLETE
- **Pages**: 14 (preprint format)
- **Date**: 2026-02-06

## Completion Checklist

### Data & Experiments
- [x] D1 calibration data: 257 observations (90 questions × 3 model-method configs)
- [x] D4 overconfident error analysis: 77/257 = 30.0% OC error rate
- [x] Topic classification: 10 CFA topics identified via keyword matching
- [x] Statistical hypothesis tests: All 4 hypotheses significant

### Figures (6 total, 3 in paper)
- [x] Fig 1: Reliability diagrams (3-panel) — IN PAPER
- [x] Fig 2: ECE comparison bar chart — supplementary
- [x] Fig 3: Coverage-accuracy tradeoff — IN PAPER
- [x] Fig 4: Overconfidence gap visualization — IN PAPER
- [x] Fig 5: Topic-level analysis (3-panel) — supplementary
- [x] Fig 6: Confidence distribution by correctness — supplementary

### Tables (7 total)
- [x] Table 1: Dataset summary
- [x] Table 2: Calibration metrics by model/method
- [x] Table 3: Overconfident error analysis
- [x] Table 4: Topic-level calibration
- [x] Table 5: Hypothesis test results
- [x] Table 6: Regulatory framework mapping
- [x] Table 7: Tiered calibration standards (inline)

### Paper Sections
- [x] Abstract (with all key numbers)
- [x] Introduction (4 contributions)
- [x] Related Work (3 subsections)
- [x] Methodology (4 subsections: confidence methods, ECE, OC errors, CaR)
- [x] Data and Experimental Design
- [x] Results (6 subsections with all data)
- [x] Discussion (Economic Significance, CFA Ethics, Regulatory, Limitations)
- [x] Conclusion
- [x] References (11 citations)
- [x] Data Availability statement

### LaTeX
- [x] Compiles without errors
- [x] All figures embedded
- [x] All cross-references resolved
- [x] No undefined citations

## Key Results Summary

| Metric | Value | Significance |
|--------|-------|-------------|
| Overconfidence gap | +22–32% | t=9.70, p<0.0001 |
| OC error rate | 30.0% | z=3.99, p<0.0001 |
| OC among errors | 66.4% | z=3.53, p=0.0002 |
| Topic variation | χ²=12.37 | p=0.030 |
| Best ECE | qwen3:32b = 0.247 | |
| Worst ECE | gpt-4o-mini verb. = 0.315 | |
| CaR(5%) | Undefined for all models | |

## Files

| File | Purpose |
|------|---------|
| `main.tex` | Complete paper (14 pages) |
| `main.pdf` | Compiled PDF |
| `theory_framework.md` | Theory & hypothesis development |
| `run_analysis.py` | Experiment analysis script |
| `analysis_results.json` | Raw analysis output |
| `figures/*.pdf` | Publication-quality figures |
| `tables/*.tex` | LaTeX table source |

## Next Steps for Submission
1. Get advisor feedback
2. Prepare cover letter
3. Submit to FRL via Elsevier Editorial Manager
