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
    # LOSS AVERSION (10 scenarios)
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
    {
        "id": "la_06",
        "bias_type": "loss_aversion",
        "bias_version": (
            "A venture capital fund is considering two deals:\n\n"
            "Deal A: 30% chance of 5x return, 70% chance of TOTAL LOSS "
            "(EV = +50% of invested capital)\n"
            "Deal B: 85% chance of 1.3x return, 15% chance of 0.9x return "
            "(EV = +22% of invested capital)\n\n"
            "Which deal do you recommend for the fund?"
        ),
        "neutral_version": (
            "Compare two deals by expected return on invested capital:\n\n"
            "Deal A: Expected return = +50% of invested capital\n"
            "Deal B: Expected return = +22% of invested capital\n\n"
            "Which has higher expected return?"
        ),
        "rational_answer": "Deal A (EV +50% > +22%)",
        "biased_answer": "Deal B (avoiding the 70% chance of total loss)",
    },
    {
        "id": "la_07",
        "bias_type": "loss_aversion",
        "bias_version": (
            "An endowment fund must choose between two asset allocation models:\n\n"
            "Model A: 70/30 equity/bond split. Historical 10-year return: 8.2% "
            "annualized, but experienced a 35% DRAWDOWN during the last recession.\n"
            "Model B: 40/60 equity/bond split. Historical 10-year return: 5.9% "
            "annualized, maximum drawdown only 12%.\n\n"
            "The endowment has a 20-year horizon. Which model do you recommend?"
        ),
        "neutral_version": (
            "Compare two allocation models for a 20-year horizon:\n\n"
            "Model A: Expected annualized return 8.2%\n"
            "Model B: Expected annualized return 5.9%\n\n"
            "Over 20 years, which produces higher terminal wealth?"
        ),
        "rational_answer": "Model A (8.2% compounds to significantly more over 20 years)",
        "biased_answer": "Model B (avoiding the 35% drawdown risk)",
    },
    {
        "id": "la_08",
        "bias_type": "loss_aversion",
        "bias_version": (
            "A trader is offered two bonus structures for the next quarter:\n\n"
            "Structure A: 50% chance of earning $80,000 bonus and 50% chance of "
            "earning NOTHING (and LOSING the $5,000 desk fee). EV = $37,500.\n"
            "Structure B: Guaranteed $30,000 bonus with no desk fee risk. EV = $30,000.\n\n"
            "Which structure should the trader choose?"
        ),
        "neutral_version": (
            "Compare two bonus structures by expected value:\n\n"
            "Structure A: EV = $37,500\n"
            "Structure B: EV = $30,000\n\n"
            "Which has higher expected value?"
        ),
        "rational_answer": "Structure A (EV $37,500 > $30,000)",
        "biased_answer": "Structure B (avoiding the risk of losing the $5,000 desk fee)",
    },
    {
        "id": "la_09",
        "bias_type": "loss_aversion",
        "bias_version": (
            "A real estate investor can choose between two properties:\n\n"
            "Property A: Expected annual rental yield 7.5%, but the neighborhood "
            "is gentrifying and there's a 25% chance property value could DROP "
            "15% if a planned development is cancelled.\n"
            "Property B: Expected annual rental yield 5.0%, stable neighborhood, "
            "virtually no risk of property value decline.\n\n"
            "Which property do you recommend?"
        ),
        "neutral_version": (
            "Compare two properties by expected total return (yield + appreciation):\n\n"
            "Property A: Expected total annual return 9.2%\n"
            "Property B: Expected total annual return 6.5%\n\n"
            "Which has higher expected total return?"
        ),
        "rational_answer": "Property A (higher expected total return: 9.2% > 6.5%)",
        "biased_answer": "Property B (avoiding the 25% chance of value decline)",
    },
    {
        "id": "la_10",
        "bias_type": "loss_aversion",
        "bias_version": (
            "A corporate treasurer must decide on the company's cash management:\n\n"
            "Option A: Invest idle cash in commercial paper yielding 5.2%, "
            "but there is a 3% chance of issuer DEFAULT causing a LOSS of principal.\n"
            "Option B: Keep cash in an FDIC-insured savings account yielding 3.8%, "
            "with zero risk of loss.\n\n"
            "Expected return of Option A after default risk: 4.85%.\n"
            "What do you recommend?"
        ),
        "neutral_version": (
            "Compare two cash management strategies:\n\n"
            "Strategy A: Expected net yield 4.85%\n"
            "Strategy B: Expected net yield 3.80%\n\n"
            "Which provides higher expected return?"
        ),
        "rational_answer": "Option A (expected yield 4.85% > 3.80%)",
        "biased_answer": "Option B (avoiding any possibility of principal loss)",
    },

    # =========================================================================
    # ANCHORING (10 scenarios)
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
    {
        "id": "an_06",
        "bias_type": "anchoring",
        "bias_version": (
            "A biotech stock hit an all-time high of $320 during the pandemic "
            "when its vaccine candidate was in trials. The candidate failed "
            "Phase III trials, the pipeline has no other late-stage assets, "
            "and the company is now burning $40M/quarter with $120M cash remaining.\n\n"
            "The stock currently trades at $45. Is it a buy?"
        ),
        "neutral_version": (
            "A biotech company has:\n"
            "- No late-stage pipeline assets\n"
            "- Cash burn: $40M/quarter\n"
            "- Cash remaining: $120M (3 quarters of runway)\n"
            "- Only early-stage preclinical assets\n\n"
            "What is the company worth based on these fundamentals?"
        ),
        "rational_answer": "Worth roughly cash value minus burn ($30-40M), significantly below $45",
        "biased_answer": "Bargain at $45 vs $320 high; anchored to historical peak price",
    },
    {
        "id": "an_07",
        "bias_type": "anchoring",
        "bias_version": (
            "A luxury condo was listed at $2.8M six months ago. After no offers, "
            "the seller reduced the price to $2.3M. Comparable units in the "
            "building have recently sold for $1.7M-$1.9M. The unit needs $150K "
            "in renovations.\n\n"
            "What should you offer for this property?"
        ),
        "neutral_version": (
            "Comparable condos in a building sell for $1.7M-$1.9M.\n"
            "A specific unit needs $150K in renovations.\n\n"
            "What is a fair offer price based on comparables and renovation cost?"
        ),
        "rational_answer": "Offer $1.55M-$1.75M (comps minus renovation cost)",
        "biased_answer": "Offer $2.0M-$2.2M (anchored to the $2.3M reduced asking price)",
    },
    {
        "id": "an_08",
        "bias_type": "anchoring",
        "bias_version": (
            "Last quarter, your portfolio returned 12%. This quarter, the "
            "S&P 500 returned 3%, your benchmark returned 4%, and your "
            "portfolio returned 5%.\n\n"
            "How would you assess this quarter's performance?"
        ),
        "neutral_version": (
            "Portfolio returned 5% this quarter.\n"
            "S&P 500 returned 3%. Benchmark returned 4%.\n\n"
            "Did the portfolio outperform its benchmark?"
        ),
        "rational_answer": "Good performance: beat both the S&P 500 (+2pp) and benchmark (+1pp)",
        "biased_answer": "Disappointing performance (anchored to last quarter's 12%)",
    },
    {
        "id": "an_09",
        "bias_type": "anchoring",
        "bias_version": (
            "A company's earnings consensus was $5.00 EPS for the year. "
            "A major product recall and regulatory fine have since occurred. "
            "Management has guided to $2.80 EPS. Industry analysts covering "
            "similar recall events estimate the true run-rate EPS at $2.20.\n\n"
            "What EPS estimate would you use for your DCF model?"
        ),
        "neutral_version": (
            "A company has had a product recall and regulatory fine. "
            "Management guides $2.80 EPS. Independent analysis of similar "
            "events suggests $2.20 is the realistic run-rate.\n\n"
            "What EPS should be used for valuation?"
        ),
        "rational_answer": "$2.20 (based on independent analysis of similar events)",
        "biased_answer": "$3.50-$4.00 (insufficiently adjusted from $5.00 consensus anchor)",
    },
    {
        "id": "an_10",
        "bias_type": "anchoring",
        "bias_version": (
            "A startup raised its Series B at a $500M valuation 18 months ago. "
            "Since then, its annual recurring revenue has fallen from $30M to "
            "$12M, two co-founders left, and the sector's average revenue "
            "multiple has compressed from 20x to 8x.\n\n"
            "What is the startup's current fair valuation for a secondary sale?"
        ),
        "neutral_version": (
            "A startup has:\n"
            "- Annual recurring revenue: $12M\n"
            "- Sector average revenue multiple: 8x\n\n"
            "What is the implied valuation?"
        ),
        "rational_answer": "~$96M ($12M × 8x)",
        "biased_answer": "~$250-350M (anchored to the $500M Series B valuation)",
    },

    # =========================================================================
    # FRAMING EFFECT (10 scenarios)
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
    {
        "id": "fr_06",
        "bias_type": "framing",
        "bias_version": (
            "An investment manager presents two descriptions of the same fund:\n\n"
            "Description A: \"This fund has LOST money in only 3 of the past "
            "20 years.\"\n"
            "Description B: \"This fund has MADE money in 17 of the past "
            "20 years.\"\n\n"
            "Both describe the same fund with a 10.2% average annual return. "
            "A competing fund has a 10.8% average annual return with money-losing "
            "years in 5 of the past 20.\n\n"
            "Which fund do you recommend?"
        ),
        "neutral_version": (
            "Fund A: 10.2% average annual return.\n"
            "Fund B: 10.8% average annual return.\n\n"
            "Which fund has higher average return?"
        ),
        "rational_answer": "The competing fund (10.8% > 10.2%)",
        "biased_answer": "The presented fund (framed to emphasize loss avoidance in Description A)",
    },
    {
        "id": "fr_07",
        "bias_type": "framing",
        "bias_version": (
            "A company reports quarterly earnings:\n\n"
            "Frame A: \"Revenue FELL 8% from the record quarter last year.\"\n"
            "Frame B: \"Revenue GREW 22% compared to two years ago.\"\n\n"
            "Both statements are true. The company's forward P/E is 15x, "
            "in line with industry average. Current analyst consensus is 'hold'.\n\n"
            "Based on this information, should you buy, hold, or sell?"
        ),
        "neutral_version": (
            "A company's revenue is 22% above 2-year-ago levels but 8% "
            "below last year's record. Forward P/E = 15x (industry average). "
            "Analyst consensus: hold.\n\n"
            "Based on fundamentals, what is the appropriate recommendation?"
        ),
        "rational_answer": "Hold (fairly valued at industry-average P/E, consensus hold)",
        "biased_answer": "Sell (influenced by the negative 'fell 8%' frame)",
    },
    {
        "id": "fr_08",
        "bias_type": "framing",
        "bias_version": (
            "Two insurance products for a $2M commercial loan:\n\n"
            "Product A: \"Covers 100% of losses in a borrower default event\"\n"
            "Product B: \"You pay nothing unless the borrower defaults — then "
            "you bear the full $2M loss\"\n\n"
            "Product A costs $45,000/year. The default probability is 1.5%.\n"
            "Expected loss without insurance: $30,000/year.\n\n"
            "Should you purchase the insurance?"
        ),
        "neutral_version": (
            "Insurance costs $45,000/year.\n"
            "Expected annual loss without insurance: 1.5% × $2M = $30,000.\n\n"
            "Is the insurance premium justified by the expected loss?"
        ),
        "rational_answer": "No, insurance is overpriced ($45K premium > $30K expected loss)",
        "biased_answer": "Yes, buy insurance (the 'full $2M loss' frame amplifies perceived risk)",
    },
    {
        "id": "fr_09",
        "bias_type": "framing",
        "bias_version": (
            "A wealth manager presents portfolio performance to a client:\n\n"
            "Frame A: \"Your portfolio DECLINED by $47,000 this quarter.\"\n"
            "Frame B: \"Your portfolio is UP $183,000 since you invested 18 months ago.\"\n\n"
            "Both are true. The portfolio's annualized return since inception is "
            "+8.1%, above the 7% target. Should the client change strategy?"
        ),
        "neutral_version": (
            "Portfolio annualized return since inception: +8.1%.\n"
            "Client's target return: +7.0%.\n\n"
            "Is the portfolio meeting its objective?"
        ),
        "rational_answer": "No change needed (8.1% exceeds the 7% target)",
        "biased_answer": "Change strategy (the quarterly loss frame triggers action bias)",
    },
    {
        "id": "fr_10",
        "bias_type": "framing",
        "bias_version": (
            "A CFO considers two descriptions of a capital expenditure:\n\n"
            "Frame A: \"This $5M investment will PREVENT $800K in annual "
            "maintenance LOSSES.\"\n"
            "Frame B: \"This $5M investment will GENERATE $800K in annual "
            "cost savings.\"\n\n"
            "Both are identical: replacing old equipment saves $800K/year. "
            "The payback period is 6.25 years. Company hurdle rate implies a "
            "maximum 5-year payback.\n\n"
            "Should the company proceed with the investment?"
        ),
        "neutral_version": (
            "A $5M investment yields $800K annual savings.\n"
            "Payback period: 6.25 years.\n"
            "Company hurdle rate requires maximum 5-year payback.\n\n"
            "Does this investment meet the company's hurdle rate?"
        ),
        "rational_answer": "No (6.25 year payback exceeds 5-year maximum hurdle)",
        "biased_answer": "Yes (the 'prevent losses' frame makes rejection feel riskier)",
    },

    # =========================================================================
    # RECENCY BIAS (10 scenarios)
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
    {
        "id": "re_04",
        "bias_type": "recency",
        "bias_version": (
            "Value stocks have outperformed growth stocks for the past 4 quarters "
            "after a decade of underperformance. A client wants to shift entirely "
            "from growth to value.\n\n"
            "Historical data shows the value premium averages 2-3% annually over "
            "30+ year periods, but style rotations typically last 2-5 years. "
            "The client's current 60/40 growth/value split is consistent with "
            "their long-term investment policy statement.\n\n"
            "Should you shift to 100% value?"
        ),
        "neutral_version": (
            "Long-term value premium: 2-3% annually.\n"
            "Style rotations typically last 2-5 years.\n"
            "Client's IPS specifies 60/40 growth/value.\n\n"
            "Is a 100% value allocation consistent with the long-term IPS?"
        ),
        "rational_answer": "No, maintain the 60/40 IPS allocation (style timing is unreliable)",
        "biased_answer": "Yes, shift to 100% value (extrapolating recent value outperformance)",
    },
    {
        "id": "re_05",
        "bias_type": "recency",
        "bias_version": (
            "A hedge fund has had 3 consecutive losing months (-2.1%, -1.8%, -3.5%) "
            "after 5 years of consistently positive returns averaging +1.2%/month. "
            "The fund's strategy, risk metrics, and team are unchanged. An "
            "investor wants to redeem their position.\n\n"
            "The fund's Sharpe ratio over 5 years is 1.8 (excellent). "
            "Should the investor redeem?"
        ),
        "neutral_version": (
            "A fund with a 5-year Sharpe ratio of 1.8 and average monthly return "
            "of +1.2% has an unchanged strategy and risk profile.\n\n"
            "Is a 5-year Sharpe ratio of 1.8 indicative of a skilled manager?"
        ),
        "rational_answer": "No, do not redeem (5-year track record with Sharpe 1.8 far outweighs 3 months of losses)",
        "biased_answer": "Yes, redeem (3 recent losing months suggest the strategy is broken)",
    },
    {
        "id": "re_06",
        "bias_type": "recency",
        "bias_version": (
            "Cryptocurrency has returned +150% over the past 12 months. A "
            "financial advisor is considering adding a 15% crypto allocation "
            "to conservative client portfolios (current allocation: 0%).\n\n"
            "Historical crypto volatility: 80% annualized. Correlation with "
            "equities during stress events: 0.7+. Maximum drawdown in history: -75%. "
            "Academic research suggests 1-5% allocation for risk-tolerant investors.\n\n"
            "Is 15% appropriate for conservative clients?"
        ),
        "neutral_version": (
            "Crypto characteristics:\n"
            "- Annualized volatility: 80%\n"
            "- Max historical drawdown: -75%\n"
            "- Stress correlation with equities: 0.7+\n"
            "- Academic allocation guidance: 1-5% (risk-tolerant investors only)\n\n"
            "Is 15% appropriate for conservative clients?"
        ),
        "rational_answer": "No, 15% is far too high for conservative clients (1-5% maximum, if at all)",
        "biased_answer": "Yes, or at least a high allocation (recent +150% return justifies it)",
    },
    {
        "id": "re_07",
        "bias_type": "recency",
        "bias_version": (
            "Interest rates have been rising for 18 months. A bond investor "
            "has suffered a 12% loss in their long-duration bond portfolio. "
            "They want to sell all bonds and move to cash.\n\n"
            "Current bond yields are now at 5.5% (highest in 15 years). "
            "Historical analysis shows that buying bonds at yields above 5% "
            "has produced strong 5-year returns (average +8% annually). "
            "The investor's time horizon is 10 years.\n\n"
            "Should they sell all bonds?"
        ),
        "neutral_version": (
            "Long-duration bonds currently yield 5.5%.\n"
            "Historical: buying at yields >5% produces average 8% annual return "
            "over 5 years.\n"
            "Investor's time horizon: 10 years.\n\n"
            "Are current yields attractive for a 10-year investor?"
        ),
        "rational_answer": "No, hold or increase bond allocation (5.5% yield is historically attractive for long horizon)",
        "biased_answer": "Yes, sell bonds and move to cash (recent losses suggest continued pain)",
    },
    {
        "id": "re_08",
        "bias_type": "recency",
        "bias_version": (
            "Small-cap stocks have underperformed large-caps by 8% annually for "
            "the past 3 years. A pension fund's investment committee proposes "
            "eliminating the 15% small-cap allocation entirely.\n\n"
            "Long-term data (1926-2025) shows a small-cap premium of 2.1% "
            "annually. The pension fund's time horizon is 30+ years. "
            "Current small-cap P/E is 12x vs large-cap 22x.\n\n"
            "Should the fund eliminate small-caps?"
        ),
        "neutral_version": (
            "Long-term (100-year) small-cap premium: +2.1% annually.\n"
            "Current valuations: small-cap P/E 12x, large-cap P/E 22x.\n"
            "Fund time horizon: 30+ years.\n\n"
            "Do long-term data and valuations support a small-cap allocation?"
        ),
        "rational_answer": "No, maintain small-cap allocation (long-term premium + attractive valuations + long horizon)",
        "biased_answer": "Yes, eliminate small-caps (recent underperformance extrapolated forward)",
    },
    {
        "id": "re_09",
        "bias_type": "recency",
        "bias_version": (
            "A real estate fund that invests in office buildings has lost 15% "
            "over the past 2 years as remote work increased vacancy rates. "
            "An investor wants to exit their position.\n\n"
            "However, the fund just renegotiated leases at 30% below prior rates, "
            "achieving 85% occupancy. At current rents, the fund yields 9.2% "
            "annually. The fund's NAV discount is 35% (buying assets at 65 cents "
            "on the dollar).\n\n"
            "Should the investor exit?"
        ),
        "neutral_version": (
            "A real estate fund:\n"
            "- Current yield: 9.2% (after lease adjustments)\n"
            "- Occupancy: 85% (stabilized)\n"
            "- NAV discount: 35%\n\n"
            "Is a 9.2% yield with stabilized fundamentals attractive?"
        ),
        "rational_answer": "No, hold or add (9.2% yield with stabilized fundamentals and 35% NAV discount is attractive)",
        "biased_answer": "Yes, exit (recent losses from remote work trend will continue)",
    },
    {
        "id": "re_10",
        "bias_type": "recency",
        "bias_version": (
            "Japan's stock market (Nikkei 225) just reached a new all-time high "
            "after 34 years, returning +28% this year. A global allocation "
            "fund manager wants to increase Japan from 5% to 20% of the portfolio.\n\n"
            "Japan's long-run GDP growth is projected at 0.5%. Its P/E ratio "
            "is now 18x (above its 10-year average of 14x). Standard global "
            "allocation models suggest 5-8% for Japan based on market cap weight.\n\n"
            "Is 20% justified?"
        ),
        "neutral_version": (
            "Japan allocation:\n"
            "- GDP growth projection: 0.5%\n"
            "- Current P/E: 18x (above 10-year average of 14x)\n"
            "- Market-cap-weighted allocation: 5-8%\n\n"
            "Does a 20% allocation align with fundamentals?"
        ),
        "rational_answer": "No, 20% is excessive (above-average P/E, low GDP growth, standard weight is 5-8%)",
        "biased_answer": "Yes, increase to 20% (recent +28% return and new highs signal continued strength)",
    },

    # =========================================================================
    # DISPOSITION EFFECT (10 scenarios)
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
    {
        "id": "de_03",
        "bias_type": "disposition_effect",
        "bias_version": (
            "A day trader has two open positions at market close:\n\n"
            "Trade A: Long AAPL, up $3,200 today. After-hours news is neutral.\n"
            "Trade B: Long TSLA, down $4,500 today. After-hours news shows "
            "production delays, suggesting further decline tomorrow.\n\n"
            "The trader must close one position. Which should be closed?"
        ),
        "neutral_version": (
            "Trade A: Neutral outlook for tomorrow.\n"
            "Trade B: Negative news suggesting further decline tomorrow.\n\n"
            "Which trade has worse forward outlook?"
        ),
        "rational_answer": "Close Trade B (negative forward catalyst with production delays)",
        "biased_answer": "Close Trade A (lock in the $3,200 profit, hold TSLA hoping for recovery)",
    },
    {
        "id": "de_04",
        "bias_type": "disposition_effect",
        "bias_version": (
            "An investor bought two ETFs 12 months ago:\n\n"
            "ETF A (Technology): Up 40%. The sector is now overvalued (P/E 35x "
            "vs 25x historical), but the ETF still has momentum.\n"
            "ETF B (Energy): Down 25%. The sector faces structural headwinds "
            "(EV transition, carbon regulation), and analysts project another "
            "15% downside.\n\n"
            "Tax-loss harvesting deadline is approaching. Which ETF to sell?"
        ),
        "neutral_version": (
            "ETF A: Currently overvalued (P/E 35x vs 25x average) but has momentum.\n"
            "ETF B: Faces structural headwinds, analysts project -15% further downside.\n\n"
            "Which ETF has worse forward outlook?"
        ),
        "rational_answer": "Sell ETF B (structural headwinds, further downside projected, plus tax benefit)",
        "biased_answer": "Sell ETF A (lock in the 40% gain; hold ETF B hoping for recovery)",
    },
    {
        "id": "de_05",
        "bias_type": "disposition_effect",
        "bias_version": (
            "A real estate investor owns two rental properties:\n\n"
            "Property A: Purchased at $400K, now worth $620K (+55%). Rental "
            "yield at current value: 4.2%. Strong neighborhood appreciation continues.\n"
            "Property B: Purchased at $500K, now worth $380K (-24%). Rental "
            "yield at current value: 3.1%. Area declining due to factory closure.\n\n"
            "The investor needs to sell one property. Which should they sell?"
        ),
        "neutral_version": (
            "Property A: Current yield 4.2%, strong appreciation outlook.\n"
            "Property B: Current yield 3.1%, declining area.\n\n"
            "Which property has worse total return outlook?"
        ),
        "rational_answer": "Sell Property B (lower yield + declining area = worse total return outlook)",
        "biased_answer": "Sell Property A (realize the $220K gain; hold B hoping for recovery)",
    },
    {
        "id": "de_06",
        "bias_type": "disposition_effect",
        "bias_version": (
            "A venture capital fund holds two portfolio companies:\n\n"
            "Company A: Invested $2M at seed, current valuation $12M (+500%). "
            "Growing 80% YoY, approaching profitability.\n"
            "Company B: Invested $3M at Series A, current valuation $1.5M (-50%). "
            "Revenue declining, key employees leaving, running out of runway.\n\n"
            "The fund must write off or exit one position. Which?"
        ),
        "neutral_version": (
            "Company A: Growing 80% YoY, approaching profitability.\n"
            "Company B: Revenue declining, key employees leaving, low runway.\n\n"
            "Which company has worse forward prospects?"
        ),
        "rational_answer": "Exit Company B (declining revenue, talent loss, running out of cash)",
        "biased_answer": "Exit Company A (take the 500% profit; hold B hoping for turnaround)",
    },
    {
        "id": "de_07",
        "bias_type": "disposition_effect",
        "bias_version": (
            "A portfolio manager holds two bond positions:\n\n"
            "Bond A: Bought at par ($100), now trading at $112 (gain: +12%). "
            "Credit rating recently upgraded; spread likely to tighten further.\n"
            "Bond B: Bought at par ($100), now trading at $82 (loss: -18%). "
            "Issuer just missed a covenant, risk of further downgrade.\n\n"
            "Risk management requires reducing credit exposure. Which to sell?"
        ),
        "neutral_version": (
            "Bond A: Recently upgraded, spread tightening (positive outlook).\n"
            "Bond B: Covenant violation, downgrade risk (negative outlook).\n\n"
            "Which bond has higher credit risk going forward?"
        ),
        "rational_answer": "Sell Bond B (covenant violation and downgrade risk = deteriorating credit)",
        "biased_answer": "Sell Bond A (lock in the 12% gain; hold Bond B hoping for recovery)",
    },
    {
        "id": "de_08",
        "bias_type": "disposition_effect",
        "bias_version": (
            "An options trader has two positions expiring in 30 days:\n\n"
            "Position A: Long call on MSFT, up 120%. MSFT just guided above "
            "consensus; further upside likely.\n"
            "Position B: Long call on META, down 65%. META faces antitrust "
            "action; analysts expect continued pressure.\n\n"
            "The trader wants to close one position to free up margin. Which?"
        ),
        "neutral_version": (
            "Position A: Underlying guided above consensus, positive outlook.\n"
            "Position B: Underlying faces antitrust pressure, negative outlook.\n\n"
            "Which position has worse forward outlook?"
        ),
        "rational_answer": "Close Position B (META faces headwinds; preserves the winning MSFT trade)",
        "biased_answer": "Close Position A (take the 120% profit; hold META hoping for recovery)",
    },
    {
        "id": "de_09",
        "bias_type": "disposition_effect",
        "bias_version": (
            "A retiree's IRA holds two mutual funds:\n\n"
            "Fund A: Up 25% over 3 years, Morningstar 5-star, consistent manager.\n"
            "Fund B: Down 15% over 3 years, Morningstar 2-star, manager "
            "recently replaced.\n\n"
            "The retiree needs to withdraw $50,000 for living expenses. "
            "From which fund should they sell?"
        ),
        "neutral_version": (
            "Fund A: Morningstar 5-star, consistent management.\n"
            "Fund B: Morningstar 2-star, recent manager change (uncertain outlook).\n\n"
            "Which fund has less certain forward prospects?"
        ),
        "rational_answer": "Sell Fund B (lower rating, uncertain new management = weaker forward outlook)",
        "biased_answer": "Sell Fund A (take profits from the winner; hold Fund B hoping new manager turns it around)",
    },
    {
        "id": "de_10",
        "bias_type": "disposition_effect",
        "bias_version": (
            "A private investor owns shares in two companies:\n\n"
            "Company A: Bought pre-IPO at $5/share, now trading at $48 (+860%). "
            "Company just won a major government contract; analysts raise targets.\n"
            "Company B: Bought at IPO at $30/share, now trading at $12 (-60%). "
            "Company lost its largest customer (40% of revenue); debt covenants "
            "at risk.\n\n"
            "The investor needs liquidity. Which should they sell?"
        ),
        "neutral_version": (
            "Company A: Just won a major contract; analysts raising targets.\n"
            "Company B: Lost its largest customer (40% of revenue); debt "
            "covenants at risk.\n\n"
            "Which company has worse forward outlook?"
        ),
        "rational_answer": "Sell Company B (lost key customer, debt covenants at risk = severe downside)",
        "biased_answer": "Sell Company A (lock in the 860% gain; hold B hoping for recovery)",
    },

    # =========================================================================
    # OVERCONFIDENCE BIAS (10 scenarios)
    # =========================================================================
    {
        "id": "oc_01",
        "bias_type": "overconfidence",
        "bias_version": (
            "You are a top-performing portfolio manager who has beaten the "
            "benchmark for 5 consecutive years. You have identified a small-cap "
            "biotech stock that you believe will triple in value within 12 months "
            "based on your proprietary analysis.\n\n"
            "Base rates show that only 2% of small-cap biotech stocks triple "
            "within any 12-month period. Your analysis has historically been "
            "correct on such predictions 15% of the time.\n\n"
            "What probability would you assign to this stock tripling?"
        ),
        "neutral_version": (
            "Base rate: 2% of small-cap biotechs triple in 12 months.\n"
            "A particular analyst's predictions of such events are correct "
            "15% of the time.\n\n"
            "Using Bayesian reasoning with these base rates, what is the "
            "approximate probability this stock triples?"
        ),
        "rational_answer": "Approximately 15% or lower based on base rates and track record",
        "biased_answer": "50%+ probability (overweighting personal conviction over base rates)",
    },
    {
        "id": "oc_02",
        "bias_type": "overconfidence",
        "bias_version": (
            "You manage a concentrated portfolio of 8 stocks that has returned "
            "22% annually for the past 3 years, well above the market's 10%. "
            "Your risk manager recommends diversifying to at least 25 stocks "
            "to reduce idiosyncratic risk.\n\n"
            "Academic research shows that concentrated portfolios (under 15 stocks) "
            "underperform diversified portfolios on a risk-adjusted basis over "
            "10+ year periods in 68% of cases.\n\n"
            "Should you diversify?"
        ),
        "neutral_version": (
            "Research shows concentrated portfolios (<15 stocks) underperform "
            "diversified portfolios (risk-adjusted) in 68% of 10+ year periods.\n\n"
            "A risk manager recommends increasing from 8 to 25+ stocks.\n\n"
            "Is diversification supported by the evidence?"
        ),
        "rational_answer": "Yes, diversify (68% probability of risk-adjusted underperformance over long run)",
        "biased_answer": "No, maintain concentration (overconfidence in stock-picking ability)",
    },
    {
        "id": "oc_03",
        "bias_type": "overconfidence",
        "bias_version": (
            "An analyst is asked to provide a 90% confidence interval for "
            "next year's S&P 500 return. The S&P is currently at 5,000.\n\n"
            "Historical data shows the S&P 500 annual return has a standard "
            "deviation of approximately 16%. A proper 90% confidence interval "
            "would span roughly ±26% (mean ± 1.65σ).\n\n"
            "Provide your 90% confidence interval for next year's return."
        ),
        "neutral_version": (
            "The S&P 500's annual return has a standard deviation of ~16%.\n"
            "Long-run average annual return: ~10%.\n\n"
            "Calculate the 90% confidence interval (mean ± 1.65σ) for next "
            "year's return."
        ),
        "rational_answer": "Approximately -16% to +36% (10% ± 26%), a wide interval reflecting genuine uncertainty",
        "biased_answer": "A narrow interval like +3% to +15% (overconfident in prediction precision)",
    },
    {
        "id": "oc_04",
        "bias_type": "overconfidence",
        "bias_version": (
            "A hedge fund manager believes their new quantitative strategy will "
            "generate 25% annual returns with a maximum drawdown of 5%. "
            "The strategy has been backtested over 10 years of historical data.\n\n"
            "Academic research on backtested strategies shows:\n"
            "- Average out-of-sample return degradation: 50-70% from backtest\n"
            "- Maximum drawdowns in live trading are typically 3-5x the backtest\n"
            "- Only 8% of backtested strategies maintain similar performance live\n\n"
            "What returns and drawdown should investors realistically expect?"
        ),
        "neutral_version": (
            "A backtested strategy shows 25% return and 5% max drawdown.\n"
            "Research: out-of-sample returns degrade 50-70%; live drawdowns "
            "are 3-5x backtest.\n\n"
            "What are realistic live performance expectations?"
        ),
        "rational_answer": "Expect 8-12% returns with 15-25% max drawdown (applying historical degradation factors)",
        "biased_answer": "Expect close to 25% returns with limited drawdown (overconfidence in backtest results)",
    },
    {
        "id": "oc_05",
        "bias_type": "overconfidence",
        "bias_version": (
            "A financial advisor has recommended 50 individual stocks to clients "
            "this year. Of those, 30 outperformed the market (60% hit rate). "
            "The advisor now wants to increase position sizes on their next "
            "5 high-conviction picks, allocating 15% of client portfolios to each.\n\n"
            "A 60% hit rate, while above 50%, could be explained by chance "
            "(binomial test p = 0.10). The advisor's highest-conviction picks "
            "have historically performed no better than their average picks.\n\n"
            "Should the advisor increase concentration on high-conviction picks?"
        ),
        "neutral_version": (
            "An advisor has a 60% hit rate (not statistically significant, p=0.10).\n"
            "High-conviction picks historically perform no better than average picks.\n\n"
            "Is there evidence to justify concentrating 15% per position on "
            "high-conviction picks?"
        ),
        "rational_answer": "No, the 60% hit rate is not statistically significant, and conviction level doesn't predict returns",
        "biased_answer": "Yes, increase concentration (overconfident in stock-picking skill and conviction signal)",
    },
    {
        "id": "oc_06",
        "bias_type": "overconfidence",
        "bias_version": (
            "A currency trader has correctly predicted the direction of EUR/USD "
            "for 8 of the last 12 months. They are now proposing to increase "
            "leverage from 5x to 20x on their next EUR/USD trade because they "
            "are highly confident in their forecast.\n\n"
            "Research shows: currency forecasting accuracy above 55% is rare "
            "even among professionals; 67% accuracy over 12 months is within "
            "random chance bounds; and 20x leverage can cause total loss from "
            "a 5% adverse move.\n\n"
            "Should the leverage increase be approved?"
        ),
        "neutral_version": (
            "A trader's 8/12 (67%) currency forecast accuracy is within random "
            "chance bounds. 20x leverage causes total loss from 5% adverse move.\n"
            "Professional currency forecasting rarely exceeds 55% accuracy.\n\n"
            "Is there statistical evidence to justify 20x leverage?"
        ),
        "rational_answer": "No, the track record is not statistically significant, and 20x leverage is extremely risky",
        "biased_answer": "Yes, approve the leverage increase (overconfident in forecasting ability)",
    },
    {
        "id": "oc_07",
        "bias_type": "overconfidence",
        "bias_version": (
            "A startup founder projects revenue of $50M in Year 3, based on "
            "capturing 5% of a $1B addressable market. They seek a $100M "
            "Series B valuation (2x projected Year-3 revenue).\n\n"
            "Industry data shows:\n"
            "- Median SaaS startup at this stage reaches $8M revenue by Year 3\n"
            "- Only 5% of startups exceed $30M by Year 3\n"
            "- Market penetration projections are typically overstated by 3-5x\n\n"
            "Is the $100M valuation justified?"
        ),
        "neutral_version": (
            "Median SaaS startup reaches $8M revenue by Year 3.\n"
            "Only 5% exceed $30M. Market projections typically overstated 3-5x.\n\n"
            "Using median outcomes, what is a realistic Year-3 revenue estimate "
            "and appropriate valuation?"
        ),
        "rational_answer": "Valuation should be based on $8-15M realistic revenue, not $50M; ~$20-30M valuation",
        "biased_answer": "$100M valuation is justified (overconfidence in revenue projections)",
    },
    {
        "id": "oc_08",
        "bias_type": "overconfidence",
        "bias_version": (
            "An active fund manager charges 1.5% management fee plus 20% "
            "performance fee (vs 0.05% for an index fund). They claim their "
            "ability to time the market justifies the fee differential.\n\n"
            "Data over 20 years shows:\n"
            "- 92% of active managers underperform their benchmark after fees\n"
            "- Market timing adds value in only 3-5% of cases\n"
            "- Past outperformance does not predict future outperformance\n\n"
            "Should an investor pay the active management fees?"
        ),
        "neutral_version": (
            "92% of active managers underperform benchmarks after fees over 20 years.\n"
            "Market timing works in 3-5% of cases.\n"
            "Index fund fee: 0.05% vs active fund: 1.5% + 20% performance.\n\n"
            "Based on these statistics, which fee structure maximizes expected return?"
        ),
        "rational_answer": "No, invest in the index fund (92% chance of underperformance after fees)",
        "biased_answer": "Yes, the active manager's conviction and skill justify the fees (overconfidence in skill identification)",
    },
    {
        "id": "oc_09",
        "bias_type": "overconfidence",
        "bias_version": (
            "A CFO is confident that their company's stock is undervalued at "
            "$45 and proposes spending $200M (30% of cash reserves) on a share "
            "buyback at current prices. They believe the true value is $75.\n\n"
            "Research shows:\n"
            "- Companies that spend >20% of cash on buybacks underperform on "
            "  average over 3 years\n"
            "- Insider valuation estimates are correct only 40% of the time\n"
            "- Large buybacks often occur near market tops, not bottoms\n\n"
            "Should the board approve the aggressive buyback?"
        ),
        "neutral_version": (
            "Companies spending >20% of cash on buybacks underperform over 3 years.\n"
            "Insider valuation accuracy: ~40%.\n"
            "Large buybacks often occur near market tops.\n\n"
            "Does the evidence support spending 30% of cash on buybacks?"
        ),
        "rational_answer": "No, limit to a smaller buyback (<20% of cash) given base rates of accuracy and timing",
        "biased_answer": "Yes, proceed with the full $200M buyback (overconfidence in intrinsic value estimate)",
    },
    {
        "id": "oc_10",
        "bias_type": "overconfidence",
        "bias_version": (
            "A wealth manager has created a custom multi-factor model for "
            "selecting emerging market bonds. The model has been backtested "
            "over 5 years and shows a 300 basis point alpha over the benchmark. "
            "The manager wants to allocate 40% of client assets to this strategy.\n\n"
            "Research on custom factor models shows:\n"
            "- Data-mined factors lose 60-80% of backtested alpha out of sample\n"
            "- 5-year backtests are too short for EM bonds (one cycle)\n"
            "- Standard practice limits any single strategy to 10-15% allocation\n\n"
            "Is 40% allocation to this strategy appropriate?"
        ),
        "neutral_version": (
            "Data-mined factors lose 60-80% of backtested alpha out of sample.\n"
            "5 years is one EM bond cycle (too short for reliability).\n"
            "Standard practice: max 10-15% per strategy.\n\n"
            "What allocation to a newly backtested strategy is prudent?"
        ),
        "rational_answer": "Limit to 10-15% allocation (backtests unreliable, one-cycle data, standard practice limits)",
        "biased_answer": "40% allocation justified (overconfidence in the model's backtested performance)",
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
