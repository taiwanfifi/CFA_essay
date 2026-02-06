# I1+I3 Paper Status

## Paper Information
- **Title**: Stress Testing Financial LLMs: Counterfactual Perturbation and Noise Sensitivity Analysis on CFA Examinations
- **Target Journal**: Finance Research Letters (FRL), SSCI Q1
- **Status**: DRAFT COMPLETE (n=100 results integrated)
- **Pages**: 13 (preprint format)
- **Date**: 2026-02-06

## Key Results (N=100)

### I1 Counterfactual Perturbation
| Metric | Value |
|--------|-------|
| Original accuracy | 86.0% |
| Level 1 (numerical) accuracy | 62.5% (n_valid=64) |
| Level 2 (conditional) accuracy | 72.9% (n_valid=85) |
| Memorization gap (L1) | +23.5% |
| Memorization gap (L2) | +13.1% |
| Robust accuracy | 58.0% |
| Memorization suspect | 28.0% |

### I3 Noise Sensitivity
| Noise Type | Accuracy | NSI | Flipped |
|------------|----------|-----|---------|
| Clean | 86.0% | --- | --- |
| N1 (irrelevant data) | 82.0% | 0.046 | 7/100 |
| N2 (misleading) | 85.0% | 0.012 | 5/100 |
| N3 (format noise) | 85.0% | 0.012 | 3/100 |
| N4 (contradictory) | 87.0% | -0.012 | 3/100 |

## Key Findings (updated from n=100)
- Memorization gap remains significant (23.5% at L1), confirming pattern-matching reliance
- Noise sensitivity is much lower than smoke test suggested (max NSI=0.046 vs 0.222)
- Primary vulnerability is memorization, not noise susceptibility
- Robust accuracy (58.0%) still substantially below standard (86.0%)
- Level 1 perturbation validity rate (64%) lower than Level 2 (85%)

## Files
| File | Purpose |
|------|---------|
| `main.tex` | Complete paper (13 pages) |
| `main.pdf` | Compiled PDF |
| `theory_framework.md` | Theory & hypothesis development |
| `submission/cover_letter.tex` | Cover letter for FRL |

## Next Steps
1. ~~Wait for n=100 experiment results~~ DONE
2. ~~Update paper with large-scale data~~ DONE
3. Add figures (degradation curve, NSI radar chart)
4. Get advisor feedback
5. Cross-model validation (test additional models)
