# A1+A5 Paper Status

## Paper Information
- **Title**: Beyond Multiple Choice: How Answer Options Inflate LLM Financial Reasoning Scores
- **Target Journal**: Finance Research Letters (FRL), SSCI Q1
- **Status**: DRAFT COMPLETE (smoke test data)
- **Pages**: 10 (preprint format)
- **Date**: 2026-02-06

## Key Results (n=20)

### A5 Option Bias
| Metric | Value |
|--------|-------|
| Accuracy WITH options | 75.0% |
| Accuracy WITHOUT options | 65.0% |
| Option bias | +10.0% |
| Biased questions | 5/20 (25%) |
| McNemar p-value | 0.724 |

### A1 Three-Tier Evaluation
| Level | Count | Percentage |
|-------|-------|-----------|
| Level A (Exact) | 8 | 40.0% |
| Level B (Directional) | 6 | 30.0% |
| Level C (Incorrect) | 6 | 30.0% |
| Strict accuracy | | 40.0% |
| Lenient accuracy | | 70.0% |

## Files
| File | Purpose |
|------|---------|
| `main.tex` | Complete paper (10 pages) |
| `main.pdf` | Compiled PDF |
| `theory_framework.md` | Theory & hypothesis development |
