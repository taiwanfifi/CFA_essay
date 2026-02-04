"""Scenario library for I2 behavioral biases experiment.

Each scenario has:
- bias_type: Which bias it tests
- bias_version: The scenario framed to induce bias
- neutral_version: Equivalent scenario with neutral framing
- rational_answer: The objectively correct answer
- biased_answer: The answer a biased agent would give
"""

from typing import Any, Dict, List

SCENARIOS: List[Dict[str, Any]] = [
    # =========================================================================
    # LOSS AVERSION (5 scenarios)
    # =========================================================================
    {
        "id": "la_01",
        "bias_type": "loss_aversion",
        "bias_version": (
            "You are advising a client on two investment options:\n\n"
            "Investment A: 80% chance of gaining $10,000 and 20% chance of "
            "LOSING $2,000 (Expected Value = $7,600)\n"
            "Investment B: Guaranteed return of $7,000 (Expected Value = $7,000)\n\n"
            "Which investment do you recommend and why?"
        ),
        "neutral_version": (
            "Compare two investments purely by expected value:\n\n"
            "Investment A: Expected Value = $7,600 (with variance)\n"
            "Investment B: Expected Value = $7,000 (guaranteed)\n\n"
            "Which has higher expected value?"
        ),
        "rational_answer": "Investment A (higher EV: $7,600 > $7,000)",
        "biased_answer": "Investment B (avoiding the loss of $2,000)",
    },
    {
        "id": "la_02",
        "bias_type": "loss_aversion",
        "bias_version": (
            "A portfolio has two positions:\n\n"
            "Stock X: Currently up 15% from purchase price, analysts project "
            "another 5% upside\n"
            "Stock Y: Currently DOWN 10% from purchase price, analysts project "
            "8% recovery\n\n"
            "The client needs to sell one position to fund a purchase. "
            "Which stock should be sold?"
        ),
        "neutral_version": (
            "A portfolio has two positions:\n\n"
            "Stock X: Projected return from current price: +5%\n"
            "Stock Y: Projected return from current price: +8%\n\n"
            "Which stock has lower projected return and should be sold?"
        ),
        "rational_answer": "Sell Stock X (lower projected forward return: 5% < 8%)",
        "biased_answer": "Sell Stock X (lock in the gain, reluctance to realize loss on Y)",
    },
    {
        "id": "la_03",
        "bias_type": "loss_aversion",
        "bias_version": (
            "A fund manager is evaluating two strategies for a $1M allocation:\n\n"
            "Strategy A: 60% probability of +$200K, 40% probability of -$100K "
            "(EV = +$80K)\n"
            "Strategy B: 90% probability of +$50K, 10% probability of -$20K "
            "(EV = +$43K)\n\n"
            "Which strategy do you recommend?"
        ),
        "neutral_version": (
            "Compare two strategies by expected return on $1M:\n\n"
            "Strategy A: EV = +$80K (higher variance)\n"
            "Strategy B: EV = +$43K (lower variance)\n\n"
            "Which has higher expected return?"
        ),
        "rational_answer": "Strategy A (EV $80K > $43K)",
        "biased_answer": "Strategy B (lower chance of loss)",
    },
    {
        "id": "la_04",
        "bias_type": "loss_aversion",
        "bias_version": (
            "An investor holds a bond portfolio with the following options:\n\n"
            "Option A: Switch to a higher-yield bond fund. Potential gain: +2.5% "
            "annual yield, but risk of LOSING 3% of principal in a rate spike.\n"
            "Option B: Keep the current portfolio. Steady 4% yield, no principal risk.\n\n"
            "What do you advise?"
        ),
        "neutral_version": (
            "Compare two bond strategies:\n\n"
            "Strategy A: Expected annual return 6.1% (with principal volatility)\n"
            "Strategy B: Expected annual return 4.0% (stable)\n\n"
            "Which has higher expected return?"
        ),
        "rational_answer": "Option A (higher expected return)",
        "biased_answer": "Option B (avoid risk of principal loss)",
    },
    {
        "id": "la_05",
        "bias_type": "loss_aversion",
        "bias_version": (
            "A retiree must choose a withdrawal strategy:\n\n"
            "Plan A: Variable withdrawals based on portfolio performance. Average "
            "$5,500/month but could DROP to $3,800 in bad months.\n"
            "Plan B: Fixed $4,800/month guaranteed.\n\n"
            "Which plan do you recommend?"
        ),
        "neutral_version": (
            "Compare average monthly income:\n"
            "Plan A: Average $5,500/month\n"
            "Plan B: Fixed $4,800/month\n\n"
            "Which provides higher average income?"
        ),
        "rational_answer": "Plan A (higher average: $5,500 > $4,800)",
        "biased_answer": "Plan B (avoiding the possibility of lower income months)",
    },

    # =========================================================================
    # ANCHORING (5 scenarios)
    # =========================================================================
    {
        "id": "an_01",
        "bias_type": "anchoring",
        "bias_version": (
            "A stock was trading at $150 six months ago. It has since dropped "
            "to $85. The company just reported:\n"
            "- Revenue down 35%\n"
            "- Debt-to-equity ratio increased from 0.5 to 2.1\n"
            "- Two major customers switched to competitors\n\n"
            "What is your fair value estimate for this stock?"
        ),
        "neutral_version": (
            "A company reports:\n"
            "- Revenue: $50M (down 35% YoY)\n"
            "- Debt-to-equity: 2.1\n"
            "- Lost 2 major customers\n"
            "- Industry P/E average: 8x\n"
            "- Company EPS: $3.20\n\n"
            "Estimate fair value using P/E methodology."
        ),
        "rational_answer": "Fair value based on fundamentals (likely $25-40 range based on deteriorated metrics)",
        "biased_answer": "Fair value anchored near $85-120 range (anchored to recent/historical price)",
    },
    {
        "id": "an_02",
        "bias_type": "anchoring",
        "bias_version": (
            "An analyst previously published a price target of $200 for TechCorp. "
            "Since then, the company's main product line was discontinued and "
            "revenue fell 45%. The analyst is asked to update the price target.\n\n"
            "What should the new price target be?"
        ),
        "neutral_version": (
            "TechCorp's main product was discontinued. Revenue fell 45%. "
            "Current EPS is $4.50 and industry P/E is 12x.\n\n"
            "What price target is supported by current fundamentals?"
        ),
        "rational_answer": "Price target based on current fundamentals (~$54 using P/E)",
        "biased_answer": "Price target insufficiently adjusted from $200 (e.g., $130-160)",
    },
    {
        "id": "an_03",
        "bias_type": "anchoring",
        "bias_version": (
            "A commercial property was appraised at $5M last year. The local "
            "market has seen a 20% decline in commercial real estate values, "
            "vacancy rates have risen from 5% to 18%, and rental rates dropped 15%.\n\n"
            "What is your current valuation?"
        ),
        "neutral_version": (
            "A commercial property generates $300K annual net operating income. "
            "Current cap rate for the area is 8.5%. Vacancy is 18%.\n\n"
            "What is the property value using direct capitalization?"
        ),
        "rational_answer": "Value based on current income/cap rate (~$2.9M using NOI/cap rate with vacancy adjustment)",
        "biased_answer": "Value anchored near $4-4.5M (insufficient adjustment from $5M appraisal)",
    },
    {
        "id": "an_04",
        "bias_type": "anchoring",
        "bias_version": (
            "Your firm's research department estimated GDP growth at 3.5% for "
            "the year. After Q3 data shows a sharp slowdown, with manufacturing "
            "PMI at 46 (contraction), consumer spending declining 2%, and "
            "unemployment rising 1.2 percentage points.\n\n"
            "What is your revised GDP growth estimate?"
        ),
        "neutral_version": (
            "Q3 data: Manufacturing PMI = 46, consumer spending -2% QoQ, "
            "unemployment up 1.2pp.\n\n"
            "Based solely on these Q3 indicators, what GDP growth rate "
            "do they suggest for the full year?"
        ),
        "rational_answer": "GDP estimate significantly revised down (likely 0.5-1.5% based on indicators)",
        "biased_answer": "GDP estimate insufficiently reduced (e.g., 2.5-3.0%, anchored to 3.5%)",
    },
    {
        "id": "an_05",
        "bias_type": "anchoring",
        "bias_version": (
            "A PE fund acquired a portfolio company for $100M three years ago. "
            "The company's EBITDA has shrunk from $15M to $8M, and comparable "
            "transactions now trade at 6x EBITDA (down from 8x).\n\n"
            "What is the current fair value of the investment?"
        ),
        "neutral_version": (
            "A company has EBITDA of $8M. Comparable transaction multiples "
            "are currently 6x EBITDA.\n\n"
            "What is the enterprise value?"
        ),
        "rational_answer": "~$48M (8M × 6x)",
        "biased_answer": "~$70-85M (anchored to $100M acquisition price)",
    },

    # =========================================================================
    # FRAMING EFFECT (5 scenarios)
    # =========================================================================
    {
        "id": "fr_01",
        "bias_type": "framing",
        "bias_version": (
            "A surgical treatment for a rare disease has the following outcome:\n"
            "\"In 10 out of 100 cases, the patient will NOT survive the procedure.\"\n\n"
            "A pharmaceutical company offers insurance against surgical failure "
            "at $50,000. Should the hospital purchase this insurance for its "
            "patients? The expected loss per case is $200,000."
        ),
        "neutral_version": (
            "A procedure has 90% survival rate. Insurance costs $50,000 per case. "
            "Expected loss per failure: $200,000.\n\n"
            "Expected insurance value: 10% × $200,000 = $20,000 < $50,000 cost.\n"
            "Is the insurance worth purchasing from a pure EV perspective?"
        ),
        "rational_answer": "No, insurance is overpriced (EV of loss = $20K < premium of $50K)",
        "biased_answer": "Yes, purchase insurance (loss framing makes risk feel larger)",
    },
    {
        "id": "fr_02",
        "bias_type": "framing",
        "bias_version": (
            "Fund A's marketing materials state:\n"
            "\"Our fund has AVOIDED losses in 85% of quarters over the past decade.\"\n\n"
            "Fund B's marketing states:\n"
            "\"Our fund has delivered positive returns averaging 9.2% annually.\"\n\n"
            "Fund A's actual annual return is 7.8%. "
            "Which fund would you recommend to a growth-oriented client?"
        ),
        "neutral_version": (
            "Fund A: Average annual return 7.8%\n"
            "Fund B: Average annual return 9.2%\n\n"
            "Which fund has higher returns for a growth client?"
        ),
        "rational_answer": "Fund B (9.2% > 7.8% for a growth client)",
        "biased_answer": "Fund A (loss-avoidance framing is psychologically appealing)",
    },
    {
        "id": "fr_03",
        "bias_type": "framing",
        "bias_version": (
            "Two restructuring proposals for a struggling company:\n\n"
            "Proposal A: \"This plan will SAVE 200 of the 600 jobs.\"\n"
            "Proposal B: \"Under this plan, 400 jobs will be LOST.\"\n\n"
            "Both proposals have identical financial projections: $10M cost savings, "
            "18-month timeline, same workforce outcome. "
            "Which proposal should the board adopt?"
        ),
        "neutral_version": (
            "Two restructuring proposals with identical outcomes:\n"
            "Both: 200 jobs retained, 400 positions eliminated, $10M saved.\n\n"
            "Should the board be indifferent between them?"
        ),
        "rational_answer": "Indifferent — both proposals have identical outcomes",
        "biased_answer": "Prefer Proposal A (\"save 200\" sounds better than \"lose 400\")",
    },
    {
        "id": "fr_04",
        "bias_type": "framing",
        "bias_version": (
            "A trader reviews two hedging strategies:\n\n"
            "Strategy X: \"Protects against 95% of downside risk in a crash\"\n"
            "Strategy Y: \"Leaves 5% of portfolio exposed to downside in a crash\"\n\n"
            "Both strategies cost the same and provide identical protection. "
            "Which do you prefer?"
        ),
        "neutral_version": (
            "Two hedging strategies with identical cost and coverage (95% downside protection). "
            "Is there any reason to prefer one over the other?"
        ),
        "rational_answer": "Indifferent — identical protection and cost",
        "biased_answer": "Strategy X (positive framing: \"protects 95%\" preferred over \"5% exposed\")",
    },
    {
        "id": "fr_05",
        "bias_type": "framing",
        "bias_version": (
            "A pension fund must choose between:\n\n"
            "Option A: \"98% probability of fully funding all pension obligations\"\n"
            "Option B: \"2% probability of failing to meet pension obligations\"\n\n"
            "The options represent the same portfolio allocation. "
            "Which framing leads to better decision-making?"
        ),
        "neutral_version": (
            "A portfolio allocation has a 98% probability of meeting pension obligations. "
            "Is this an acceptable risk level for a pension fund?"
        ),
        "rational_answer": "Both framings describe the same thing; a rational decision-maker should be indifferent",
        "biased_answer": "Option A preferred (framing bias — \"98% success\" sounds better than \"2% failure\")",
    },

    # =========================================================================
    # RECENCY BIAS (3 scenarios)
    # =========================================================================
    {
        "id": "re_01",
        "bias_type": "recency",
        "bias_version": (
            "The tech sector has outperformed the S&P 500 for the past 5 consecutive "
            "quarters, returning +45% vs the market's +15%. A client wants to "
            "allocate 70% of their portfolio to tech stocks.\n\n"
            "Long-term data shows tech's average allocation in balanced portfolios "
            "is 25-30%, and mean-reversion patterns suggest sectors rarely outperform "
            "for more than 6-8 consecutive quarters.\n\n"
            "What allocation do you recommend?"
        ),
        "neutral_version": (
            "Historical analysis:\n"
            "- Tech sector long-run average weight in balanced portfolio: 25-30%\n"
            "- Sectors that outperform for 5+ quarters typically mean-revert\n"
            "- Client risk tolerance supports 25-35% equity allocation in any sector\n\n"
            "What tech allocation do you recommend?"
        ),
        "rational_answer": "25-30% allocation (based on long-run fundamentals and mean reversion)",
        "biased_answer": "50-70% allocation (extrapolating recent outperformance)",
    },
    {
        "id": "re_02",
        "bias_type": "recency",
        "bias_version": (
            "Emerging markets have underperformed developed markets for 3 years:\n"
            "EM: -5%, +2%, -8% vs DM: +12%, +15%, +10%\n\n"
            "However, EM valuations are now at historical lows (P/E 9x vs "
            "long-run average of 14x), and IMF projects EM GDP growth of 5.2% "
            "vs DM 1.8%.\n\n"
            "Should you reduce EM allocation?"
        ),
        "neutral_version": (
            "EM metrics: P/E 9x (vs historical 14x), projected GDP growth 5.2%.\n"
            "DM metrics: P/E 18x, projected GDP growth 1.8%.\n\n"
            "Based on valuations and growth projections, which region is more "
            "attractively valued?"
        ),
        "rational_answer": "Increase/maintain EM allocation (low valuations + high projected growth)",
        "biased_answer": "Reduce EM allocation (recent underperformance suggests continued weakness)",
    },
    {
        "id": "re_03",
        "bias_type": "recency",
        "bias_version": (
            "Gold has risen 25% in the last 6 months amid geopolitical tensions. "
            "An advisor recommends increasing gold from 5% to 20% of the portfolio.\n\n"
            "Long-term data: Gold's average real return is 0.8% annually. "
            "Its primary role in portfolios is diversification (low correlation with equities), "
            "and standard allocation guidance suggests 5-10%.\n\n"
            "Do you agree with the increase to 20%?"
        ),
        "neutral_version": (
            "Gold allocation analysis:\n"
            "- Long-term real return: 0.8%/year\n"
            "- Standard allocation guidance: 5-10%\n"
            "- Primary role: diversification\n\n"
            "Is 20% gold allocation justified?"
        ),
        "rational_answer": "No, 20% is excessive. Maintain 5-10% based on fundamentals.",
        "biased_answer": "Yes, increase gold allocation (recent price momentum justifies it)",
    },

    # =========================================================================
    # DISPOSITION EFFECT (2 scenarios)
    # =========================================================================
    {
        "id": "de_01",
        "bias_type": "disposition_effect",
        "bias_version": (
            "A portfolio contains:\n\n"
            "Stock A: Bought at $50, now at $75 (+50%). Analyst target: $82.\n"
            "Stock B: Bought at $80, now at $55 (-31%). Analyst target: $45.\n\n"
            "The client needs $10,000 in cash. Which stock should be sold?"
        ),
        "neutral_version": (
            "Stock A: Current $75, target $82 (projected upside: +9.3%)\n"
            "Stock B: Current $55, target $45 (projected downside: -18.2%)\n\n"
            "Which stock has worse forward outlook and should be sold?"
        ),
        "rational_answer": "Sell Stock B (negative forward outlook: -18.2%)",
        "biased_answer": "Sell Stock A (lock in gains, reluctance to realize loss on B)",
    },
    {
        "id": "de_02",
        "bias_type": "disposition_effect",
        "bias_version": (
            "A fund manager reviews quarterly performance:\n\n"
            "Position X: Up 30% since entry, slowing momentum, fully valued.\n"
            "Position Y: Down 20% since entry, deteriorating fundamentals, "
            "downgraded by 2 analysts.\n\n"
            "The fund needs to reduce by one position. Which do you recommend selling?"
        ),
        "neutral_version": (
            "Position X: Fully valued, slowing momentum.\n"
            "Position Y: Deteriorating fundamentals, 2 analyst downgrades.\n\n"
            "Which position has worse forward prospects?"
        ),
        "rational_answer": "Sell Position Y (deteriorating fundamentals and analyst downgrades)",
        "biased_answer": "Sell Position X (take profits, hold Y hoping for recovery)",
    },
]


def get_scenarios(
    bias_types: list[str] | None = None,
    limit: int = 0,
) -> list[dict]:
    """Get scenarios, optionally filtered by bias type.

    Args:
        bias_types: List of bias type keys to include. None = all.
        limit: Max scenarios per bias type (0 = all).

    Returns:
        List of scenario dicts.
    """
    if bias_types is None:
        filtered = SCENARIOS
    else:
        filtered = [s for s in SCENARIOS if s["bias_type"] in bias_types]

    if limit > 0:
        # Limit per bias type to ensure balanced representation
        by_type: dict[str, list] = {}
        for s in filtered:
            by_type.setdefault(s["bias_type"], []).append(s)

        result = []
        for bt, items in by_type.items():
            result.extend(items[:limit])
        return result

    return filtered


def get_available_bias_types() -> list[str]:
    """Return list of available bias type keys."""
    return list(set(s["bias_type"] for s in SCENARIOS))
