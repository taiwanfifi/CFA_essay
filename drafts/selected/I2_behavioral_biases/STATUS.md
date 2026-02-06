# I2 Paper Status

## Paper Information
- **Title**: Inherited Irrationality: Behavioral Finance Biases in Large Language Model Financial Recommendations
- **Target Journal**: Finance Research Letters or J. Behavioral and Experimental Finance
- **Status**: DRAFT COMPLETE (full run data, n=20, 5 bias types)
- **Pages**: ~17 (preprint format, includes appendix)
- **Date**: 2026-02-06

## Key Results (n=20 scenarios, 5 bias types, GPT-4o-mini)
| Metric | Bias-Inducing | Neutral | Debiasing |
|--------|:---:|:---:|:---:|
| Mean Bias Score | 0.525 | 0.350 | +0.175 |
| Loss Aversion (n=5) | 0.500 | 0.100 | +0.400 |
| Anchoring (n=5) | 0.600 | 0.400 | +0.200 |
| Framing (n=5) | 0.500 | 0.400 | +0.100 |
| Recency (n=3) | 0.500 | 0.500 | +0.000 |
| Disposition Effect (n=2) | 0.500 | 0.500 | +0.000 |

### Key Findings
- **Debiasing hierarchy**: Loss aversion >> Anchoring > Framing >> Recency = Disposition (zero effect)
- **Extreme bias cases**: an_04 (bias=1.0) and fr_05 (bias=1.0) — fully biased responses
- **Fully rational case**: fr_02 (bias=0.0) — rational even under bias-inducing framing
- Loss aversion: 4/5 scenarios achieve full debiasing (neutral score = 0.00)
- Recency + disposition: 0/5 scenarios show any debiasing effect
- Debiasing remains binary at scenario level (delta = 0.00 or 0.50)

### Changes from POC (n=10, 2 bias types)
- Expanded from 2 bias types (loss aversion, anchoring) to 5
- Expanded from 10 to 20 scenarios
- Mean bias score: 0.50 → 0.525 (slight increase)
- Mean neutral score: 0.30 → 0.350 (increase)
- Mean debiasing: +0.20 → +0.175 (decrease, due to resistant bias types)
- Loss aversion neutral score improved: 0.30 → 0.10 (much better debiasing in full run)
- Discovery of fully biased responses (score=1.0) not seen in POC

## Files
| File | Purpose |
|------|---------|
| `main.tex` | Complete paper (~530 lines) |
| `main.pdf` | Compiled PDF |
| `theory_framework.md` | Theory & hypothesis development |
