"""
Financial calculator tools for CFA exam agent.
Five domain-specific tools exposed as OpenAI function-calling schemas.
"""

import math
import re
from typing import Any, Dict, Optional


# ---------------------------------------------------------------------------
# 1. Time-Value-of-Money Calculator
# ---------------------------------------------------------------------------

def tvm_calculator(
    calculate: str,
    pv: float = 0.0,
    fv: float = 0.0,
    pmt: float = 0.0,
    n_years: float = 0.0,
    annual_rate: float = 0.0,
    compounding: str = "annual",
) -> Dict[str, Any]:
    """Solve for one TVM variable given the others.

    Parameters
    ----------
    calculate : str
        Which variable to solve for: "pv", "fv", "pmt", "n", "rate".
    pv, fv, pmt : float
        Present value, future value, payment (per period).
    n_years : float
        Number of years.
    annual_rate : float
        Annual interest rate as a decimal (e.g. 0.05 for 5%).
    compounding : str
        "annual", "semi-annual", "quarterly", "monthly", "daily", "continuous".
    """

    # Determine periods per year
    freq_map = {
        "annual": 1,
        "semi-annual": 2,
        "quarterly": 4,
        "monthly": 12,
        "daily": 365,
        "continuous": None,
    }
    m = freq_map.get(compounding, 1)
    steps = []

    if compounding == "continuous":
        r = annual_rate
        n = n_years
        steps.append(f"Continuous compounding: r={r}, n={n}")
        if calculate == "fv":
            result = pv * math.exp(r * n) + pmt * (math.exp(r * n) - 1) / r if r != 0 else pv + pmt * n
            formula = "FV = PV * e^(r*n) + PMT * (e^(r*n) - 1) / r"
        elif calculate == "pv":
            result = fv * math.exp(-r * n) - pmt * (1 - math.exp(-r * n)) / r if r != 0 else fv - pmt * n
            formula = "PV = FV * e^(-r*n) - PMT * (1 - e^(-r*n)) / r"
        else:
            return {"error": f"Continuous compounding only supports pv/fv, got '{calculate}'"}
    else:
        per_rate = annual_rate / m
        n_periods = n_years * m
        steps.append(f"Periodic rate = {annual_rate}/{m} = {per_rate}")
        steps.append(f"Total periods = {n_years} * {m} = {n_periods}")

        if calculate == "fv":
            fv_pv = pv * (1 + per_rate) ** n_periods
            fv_pmt = pmt * ((1 + per_rate) ** n_periods - 1) / per_rate if per_rate != 0 else pmt * n_periods
            result = fv_pv + fv_pmt
            formula = "FV = PV*(1+r)^n + PMT*((1+r)^n - 1)/r"
            steps.append(f"FV(PV) = {pv} * (1+{per_rate})^{n_periods} = {fv_pv:.6f}")
            steps.append(f"FV(PMT) = {pmt} * ((1+{per_rate})^{n_periods} - 1) / {per_rate} = {fv_pmt:.6f}")

        elif calculate == "pv":
            pv_fv = fv / (1 + per_rate) ** n_periods if per_rate != 0 else fv
            pv_pmt = pmt * (1 - (1 + per_rate) ** -n_periods) / per_rate if per_rate != 0 else pmt * n_periods
            result = pv_fv + pv_pmt
            formula = "PV = FV/(1+r)^n + PMT*(1 - (1+r)^-n)/r"
            steps.append(f"PV(FV) = {fv} / (1+{per_rate})^{n_periods} = {pv_fv:.6f}")
            steps.append(f"PV(PMT) = {pmt} * (1-(1+{per_rate})^-{n_periods}) / {per_rate} = {pv_pmt:.6f}")

        elif calculate == "pmt":
            if per_rate == 0:
                result = -(pv + fv) / n_periods if n_periods != 0 else 0
            else:
                result = -(pv * (1 + per_rate) ** n_periods + fv) * per_rate / ((1 + per_rate) ** n_periods - 1)
            formula = "PMT = -(PV*(1+r)^n + FV) * r / ((1+r)^n - 1)"
            steps.append(f"PMT = -({pv}*(1+{per_rate})^{n_periods} + {fv}) * {per_rate} / ((1+{per_rate})^{n_periods} - 1) = {result:.6f}")

        elif calculate == "n":
            if per_rate == 0:
                result = -(pv + fv) / pmt if pmt != 0 else 0
            else:
                # Solve: FV = -PV*(1+r)^n - PMT*((1+r)^n -1)/r
                # When PMT=0: n = ln(FV/-PV)/ln(1+r)
                if pmt == 0:
                    result = math.log(fv / -pv) / math.log(1 + per_rate) if pv != 0 else 0
                else:
                    num = math.log((-fv * per_rate + pmt) / (pv * per_rate + pmt))
                    result = num / math.log(1 + per_rate)
            formula = "n = ln((-FV*r + PMT)/(PV*r + PMT)) / ln(1+r)"
            steps.append(f"n (periods) = {result:.6f}")
            # Convert back to years
            result = result / m
            steps.append(f"n (years) = {result:.6f}")

        elif calculate == "rate":
            # Newton-Raphson to solve for per_rate
            # f(r) = PV*(1+r)^n + PMT*((1+r)^n - 1)/r + FV = 0
            r_guess = 0.05
            for _ in range(200):
                if r_guess == 0:
                    r_guess = 0.01
                compound = (1 + r_guess) ** n_periods
                f_val = pv * compound + pmt * (compound - 1) / r_guess + fv
                # derivative
                d_compound = n_periods * (1 + r_guess) ** (n_periods - 1)
                f_prime = pv * d_compound + pmt * (d_compound * r_guess - (compound - 1)) / (r_guess ** 2)
                if abs(f_prime) < 1e-15:
                    break
                r_new = r_guess - f_val / f_prime
                if abs(r_new - r_guess) < 1e-12:
                    r_guess = r_new
                    break
                r_guess = r_new
            result = r_guess * m  # annualize
            formula = "Newton-Raphson iterative solution for rate"
            steps.append(f"Periodic rate = {r_guess:.8f}, Annual rate = {result:.8f}")

        else:
            return {"error": f"Unknown calculate target: '{calculate}'"}

    steps.append(f"Result = {result}")
    return {"result": round(result, 8), "formula": formula, "steps": steps}


# ---------------------------------------------------------------------------
# 2. Bond Calculator
# ---------------------------------------------------------------------------

def bond_calculator(
    calculate: str = "price",
    face: float = 1000.0,
    coupon_rate: float = 0.0,
    ytm: float = 0.0,
    years: float = 0.0,
    frequency: int = 2,
    current_oas: float = 0.0,
    expected_oas: float = 0.0,
    spread_duration: float = 0.0,
    annual_credit_loss: float = 0.0,
    modified_duration: float = 0.0,
    convexity_value: float = 0.0,
    yield_change: float = 0.0,
    current_price: float = 0.0,
) -> Dict[str, Any]:
    """Bond price, YTM, duration, convexity, price change, and excess return calculations."""

    steps = []

    if calculate == "price":
        coupon = face * coupon_rate / frequency
        per_ytm = ytm / frequency
        n = int(years * frequency)
        steps.append(f"Coupon per period = {face} * {coupon_rate} / {frequency} = {coupon:.4f}")
        steps.append(f"Periodic YTM = {ytm}/{frequency} = {per_ytm:.6f}")
        steps.append(f"Total periods = {n}")
        if per_ytm == 0:
            price = coupon * n + face
        else:
            pv_coupons = coupon * (1 - (1 + per_ytm) ** -n) / per_ytm
            pv_face = face / (1 + per_ytm) ** n
            price = pv_coupons + pv_face
        steps.append(f"PV(coupons) = {pv_coupons:.4f}" if per_ytm != 0 else "")
        steps.append(f"PV(face) = {pv_face:.4f}" if per_ytm != 0 else "")
        steps.append(f"Price = {price:.4f}")
        return {"result": round(price, 6), "formula": "P = C*[1-(1+r)^-n]/r + F/(1+r)^n", "steps": [s for s in steps if s]}

    elif calculate == "ytm":
        # Newton-Raphson for YTM
        coupon = face * coupon_rate / frequency
        n = int(years * frequency)
        r = 0.05 / frequency  # initial guess
        for _ in range(300):
            if r <= -1:
                r = 0.01
            compound = (1 + r) ** n
            price_est = coupon * (1 - 1 / compound) / r + face / compound if r != 0 else coupon * n + face
            d_compound = n * (1 + r) ** (n - 1)
            dp = coupon * (-(-d_compound * r - (1 - 1/compound)) / (r**2)) if r != 0 else 0
            dp = coupon * (-(1/compound - 1 + r * n / compound) / (r**2)) - face * d_compound / compound**2 if r != 0 else 0
            # Simpler numerical derivative
            dr = 1e-7
            price_up = coupon * (1 - (1 + r + dr) ** -n) / (r + dr) + face / (1 + r + dr) ** n
            dp = (price_up - price_est) / dr
            if abs(dp) < 1e-15:
                break
            target = current_price if current_price > 0 else face
            r_new = r - (price_est - target) / dp
            if abs(r_new - r) < 1e-12:
                r = r_new
                break
            r = r_new
        result = r * frequency
        steps.append(f"YTM (annualized) = {result:.8f} ({result*100:.4f}%)")
        return {"result": round(result, 8), "formula": "Newton-Raphson iterative YTM", "steps": steps}

    elif calculate == "duration":
        coupon = face * coupon_rate / frequency
        per_ytm = ytm / frequency
        n = int(years * frequency)
        if per_ytm == 0:
            return {"error": "Cannot compute duration with YTM=0"}
        price = coupon * (1 - (1 + per_ytm) ** -n) / per_ytm + face / (1 + per_ytm) ** n
        mac_dur = 0.0
        for t in range(1, n + 1):
            cf = coupon + (face if t == n else 0)
            pv_cf = cf / (1 + per_ytm) ** t
            mac_dur += t * pv_cf
        mac_dur /= price
        mac_dur_years = mac_dur / frequency
        mod_dur = mac_dur_years / (1 + per_ytm)
        steps.append(f"Price = {price:.4f}")
        steps.append(f"Macaulay Duration = {mac_dur_years:.4f} years")
        steps.append(f"Modified Duration = {mod_dur:.4f}")
        return {
            "result": {"macaulay_duration": round(mac_dur_years, 6), "modified_duration": round(mod_dur, 6), "price": round(price, 4)},
            "formula": "MacDur = sum(t*PV(CF_t)) / P; ModDur = MacDur/(1+y/m)",
            "steps": steps,
        }

    elif calculate == "convexity":
        coupon = face * coupon_rate / frequency
        per_ytm = ytm / frequency
        n = int(years * frequency)
        price = coupon * (1 - (1 + per_ytm) ** -n) / per_ytm + face / (1 + per_ytm) ** n
        conv = 0.0
        for t in range(1, n + 1):
            cf = coupon + (face if t == n else 0)
            pv_cf = cf / (1 + per_ytm) ** t
            conv += t * (t + 1) * pv_cf
        conv /= (price * (1 + per_ytm) ** 2 * frequency ** 2)
        steps.append(f"Price = {price:.4f}")
        steps.append(f"Convexity = {conv:.4f}")
        return {"result": round(conv, 6), "formula": "Conv = sum(t*(t+1)*PV(CF_t)) / (P*(1+y)^2)", "steps": steps}

    elif calculate == "price_change":
        # Using duration + convexity approximation
        dur_effect = -modified_duration * yield_change
        conv_effect = 0.5 * convexity_value * yield_change ** 2
        pct_change = dur_effect + conv_effect
        steps.append(f"Duration effect = -{modified_duration} * {yield_change} = {dur_effect:.6f}")
        steps.append(f"Convexity effect = 0.5 * {convexity_value} * {yield_change}^2 = {conv_effect:.6f}")
        steps.append(f"% Price change = {pct_change:.6f} ({pct_change*100:.4f}%)")
        if current_price > 0:
            new_price = current_price * (1 + pct_change)
            steps.append(f"New price = {current_price} * (1 + {pct_change:.6f}) = {new_price:.4f}")
        return {
            "result": {"pct_change": round(pct_change, 8), "new_price": round(current_price * (1 + pct_change), 4) if current_price > 0 else None},
            "formula": "%ΔP ≈ -ModDur*Δy + 0.5*Convexity*Δy²",
            "steps": steps,
        }

    elif calculate == "excess_return":
        # Excess return ≈ (spread - Δspread * spread_duration - credit_loss)
        spread_change = (expected_oas - current_oas) / 10000  # convert bps to decimal
        spread_return = current_oas / 10000
        price_effect = -spread_duration * spread_change
        credit = annual_credit_loss
        excess = spread_return + price_effect - credit
        steps.append(f"Spread (decimal) = {current_oas}/10000 = {spread_return:.6f}")
        steps.append(f"Spread change = ({expected_oas} - {current_oas}) / 10000 = {spread_change:.6f}")
        steps.append(f"Price effect = -{spread_duration} * {spread_change} = {price_effect:.6f}")
        steps.append(f"Credit loss = {credit:.6f}")
        steps.append(f"Excess return = {spread_return} + {price_effect} - {credit} = {excess:.6f} ({excess*100:.4f}%)")
        return {"result": round(excess, 8), "formula": "Excess ≈ spread + (-SpreadDur * ΔSpread) - credit_loss", "steps": steps}

    else:
        return {"error": f"Unknown bond calculation: '{calculate}'"}


# ---------------------------------------------------------------------------
# 3. Statistics / Portfolio Calculator
# ---------------------------------------------------------------------------

def statistics_calculator(
    calculate: str = "portfolio_return",
    weights: Optional[list] = None,
    returns: Optional[list] = None,
    std_devs: Optional[list] = None,
    correlation_matrix: Optional[list] = None,
    risk_free_rate: float = 0.0,
    risk_aversion: float = 0.0,
    expected_return: float = 0.0,
    std_dev: float = 0.0,
) -> Dict[str, Any]:
    """Portfolio return, risk, Sharpe ratio, and utility calculations."""

    steps = []
    weights = weights or []
    returns = returns or []
    std_devs = std_devs or []
    correlation_matrix = correlation_matrix or []

    if calculate == "portfolio_return":
        if len(weights) != len(returns):
            return {"error": f"weights ({len(weights)}) and returns ({len(returns)}) must have same length"}
        port_ret = sum(w * r for w, r in zip(weights, returns))
        steps.append(f"Portfolio return = sum(w_i * r_i) = {' + '.join(f'{w}*{r}' for w, r in zip(weights, returns))}")
        steps.append(f"= {port_ret:.8f}")
        return {"result": round(port_ret, 8), "formula": "R_p = Σ(w_i * R_i)", "steps": steps}

    elif calculate == "portfolio_risk":
        n = len(weights)
        if n != len(std_devs):
            return {"error": f"weights ({n}) and std_devs ({len(std_devs)}) must have same length"}
        # Build covariance matrix from std_devs and correlation_matrix
        if not correlation_matrix:
            if n == 1:
                correlation_matrix = [[1.0]]
            else:
                return {"error": "correlation_matrix required for multi-asset portfolio"}
        variance = 0.0
        for i in range(n):
            for j in range(n):
                cov_ij = std_devs[i] * std_devs[j] * correlation_matrix[i][j]
                variance += weights[i] * weights[j] * cov_ij
        port_std = math.sqrt(variance)
        steps.append(f"Portfolio variance = Σ Σ w_i * w_j * σ_i * σ_j * ρ_ij = {variance:.8f}")
        steps.append(f"Portfolio std dev = √{variance:.8f} = {port_std:.8f}")
        return {"result": round(port_std, 8), "formula": "σ_p = √(Σ Σ w_i w_j σ_i σ_j ρ_ij)", "steps": steps}

    elif calculate == "sharpe_ratio":
        if std_dev == 0:
            return {"error": "std_dev cannot be zero for Sharpe ratio"}
        sharpe = (expected_return - risk_free_rate) / std_dev
        steps.append(f"Sharpe = ({expected_return} - {risk_free_rate}) / {std_dev} = {sharpe:.6f}")
        return {"result": round(sharpe, 8), "formula": "Sharpe = (R_p - R_f) / σ_p", "steps": steps}

    elif calculate == "utility":
        # U = E(R) - 0.5 * A * σ²
        util = expected_return - 0.5 * risk_aversion * std_dev ** 2
        steps.append(f"Utility = {expected_return} - 0.5 * {risk_aversion} * {std_dev}^2")
        steps.append(f"= {expected_return} - {0.5 * risk_aversion * std_dev**2:.8f} = {util:.8f}")
        return {"result": round(util, 8), "formula": "U = E(R) - 0.5 * A * σ²", "steps": steps}

    elif calculate == "covariance":
        if len(std_devs) >= 2 and correlation_matrix:
            cov = std_devs[0] * std_devs[1] * correlation_matrix[0][1]
            steps.append(f"Cov = {std_devs[0]} * {std_devs[1]} * {correlation_matrix[0][1]} = {cov:.8f}")
            return {"result": round(cov, 8), "formula": "Cov(i,j) = σ_i * σ_j * ρ_ij", "steps": steps}
        return {"error": "Need at least 2 std_devs and correlation_matrix"}

    else:
        return {"error": f"Unknown statistics calculation: '{calculate}'"}


# ---------------------------------------------------------------------------
# 4. Economics Calculator
# ---------------------------------------------------------------------------

def economics_calculator(
    calculate: str = "taylor_rule",
    neutral_rate: float = 0.0,
    target_inflation: float = 0.0,
    expected_inflation: float = 0.0,
    current_inflation: float = 0.0,
    gdp_growth: float = 0.0,
    potential_gdp_growth: float = 0.0,
    inflation_weight: float = 0.5,
    gdp_weight: float = 0.5,
    # Risk premium buildup
    real_risk_free: float = 0.0,
    inflation_premium: float = 0.0,
    default_risk_premium: float = 0.0,
    liquidity_premium: float = 0.0,
    maturity_premium: float = 0.0,
    equity_risk_premium: float = 0.0,
    beta: float = 1.0,
    country_premium: float = 0.0,
    # CAPM / cost of equity
    risk_free_rate: float = 0.0,
    market_return: float = 0.0,
) -> Dict[str, Any]:
    """Taylor rule, risk premium buildup, CAPM cost of equity."""

    steps = []

    if calculate == "taylor_rule":
        inflation_gap = current_inflation - target_inflation
        output_gap = gdp_growth - potential_gdp_growth
        rate = neutral_rate + current_inflation + inflation_weight * inflation_gap + gdp_weight * output_gap
        steps.append(f"Inflation gap = {current_inflation} - {target_inflation} = {inflation_gap:.4f}")
        steps.append(f"Output gap = {gdp_growth} - {potential_gdp_growth} = {output_gap:.4f}")
        steps.append(f"Taylor rule rate = {neutral_rate} + {current_inflation} + {inflation_weight}*{inflation_gap} + {gdp_weight}*{output_gap}")
        steps.append(f"= {rate:.6f} ({rate*100:.4f}%)")
        return {"result": round(rate, 8), "formula": "i = r* + π + α(π - π*) + β(y - y*)", "steps": steps}

    elif calculate == "risk_premium_buildup":
        total = real_risk_free + inflation_premium + default_risk_premium + liquidity_premium + maturity_premium
        steps.append(f"Real risk-free = {real_risk_free}")
        steps.append(f"Inflation premium = {inflation_premium}")
        steps.append(f"Default risk premium = {default_risk_premium}")
        steps.append(f"Liquidity premium = {liquidity_premium}")
        steps.append(f"Maturity premium = {maturity_premium}")
        steps.append(f"Total required return = {total:.6f}")
        return {"result": round(total, 8), "formula": "r = r_f + IP + DRP + LP + MP", "steps": steps}

    elif calculate == "capm":
        cost_equity = risk_free_rate + beta * (market_return - risk_free_rate) + country_premium
        steps.append(f"CAPM: r = {risk_free_rate} + {beta} * ({market_return} - {risk_free_rate}) + {country_premium}")
        steps.append(f"= {risk_free_rate} + {beta * (market_return - risk_free_rate):.6f} + {country_premium}")
        steps.append(f"= {cost_equity:.6f} ({cost_equity*100:.4f}%)")
        return {"result": round(cost_equity, 8), "formula": "r = R_f + β(R_m - R_f) + CRP", "steps": steps}

    elif calculate == "fisher_effect":
        nominal = (1 + real_risk_free) * (1 + expected_inflation) - 1
        steps.append(f"Fisher: (1 + {real_risk_free}) * (1 + {expected_inflation}) - 1 = {nominal:.6f}")
        return {"result": round(nominal, 8), "formula": "(1+r_nominal) = (1+r_real)(1+π)", "steps": steps}

    else:
        return {"error": f"Unknown economics calculation: '{calculate}'"}


# ---------------------------------------------------------------------------
# 5. General Math (safety-net)
# ---------------------------------------------------------------------------

_SAFE_NAMES = {
    k: v for k, v in math.__dict__.items() if not k.startswith("_")
}
_SAFE_NAMES["abs"] = abs
_SAFE_NAMES["round"] = round
_SAFE_NAMES["min"] = min
_SAFE_NAMES["max"] = max
_SAFE_NAMES["sum"] = sum


def general_math(expression: str) -> Dict[str, Any]:
    """Evaluate a math expression string safely.

    Only allows math module functions and basic builtins.
    """
    # Reject obviously dangerous patterns
    forbidden = ["import", "__", "exec", "eval", "open", "os.", "sys.", "subprocess"]
    expr_lower = expression.lower()
    for f in forbidden:
        if f in expr_lower:
            return {"error": f"Forbidden pattern '{f}' in expression"}

    try:
        result = eval(expression, {"__builtins__": {}}, _SAFE_NAMES)
        return {"result": result, "formula": expression, "steps": [f"{expression} = {result}"]}
    except Exception as e:
        return {"error": f"Failed to evaluate: {e}"}


# ---------------------------------------------------------------------------
# OpenAI Function-Calling Schemas
# ---------------------------------------------------------------------------

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "tvm_calculator",
            "description": "Time-value-of-money calculator. Solves for PV, FV, PMT, N (years), or rate given the other variables. Supports various compounding frequencies.",
            "parameters": {
                "type": "object",
                "properties": {
                    "calculate": {
                        "type": "string",
                        "enum": ["pv", "fv", "pmt", "n", "rate"],
                        "description": "Which variable to solve for.",
                    },
                    "pv": {"type": "number", "description": "Present value (use negative for cash outflow)."},
                    "fv": {"type": "number", "description": "Future value."},
                    "pmt": {"type": "number", "description": "Payment per period (use negative for cash outflow)."},
                    "n_years": {"type": "number", "description": "Number of years."},
                    "annual_rate": {"type": "number", "description": "Annual interest rate as decimal (e.g. 0.05 for 5%)."},
                    "compounding": {
                        "type": "string",
                        "enum": ["annual", "semi-annual", "quarterly", "monthly", "daily", "continuous"],
                        "description": "Compounding frequency. Default: annual.",
                    },
                },
                "required": ["calculate"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "bond_calculator",
            "description": "Bond analytics: price, YTM, Macaulay/modified duration, convexity, duration+convexity price change approximation, and credit excess return.",
            "parameters": {
                "type": "object",
                "properties": {
                    "calculate": {
                        "type": "string",
                        "enum": ["price", "ytm", "duration", "convexity", "price_change", "excess_return"],
                        "description": "What to calculate.",
                    },
                    "face": {"type": "number", "description": "Face/par value. Default 1000."},
                    "coupon_rate": {"type": "number", "description": "Annual coupon rate as decimal."},
                    "ytm": {"type": "number", "description": "Yield to maturity as decimal."},
                    "years": {"type": "number", "description": "Years to maturity."},
                    "frequency": {"type": "integer", "description": "Coupon payments per year. Default 2 (semi-annual)."},
                    "current_oas": {"type": "number", "description": "Current OAS in basis points (for excess_return)."},
                    "expected_oas": {"type": "number", "description": "Expected OAS in basis points (for excess_return)."},
                    "spread_duration": {"type": "number", "description": "Spread duration (for excess_return)."},
                    "annual_credit_loss": {"type": "number", "description": "Expected annual credit loss as decimal (for excess_return)."},
                    "modified_duration": {"type": "number", "description": "Modified duration (for price_change)."},
                    "convexity_value": {"type": "number", "description": "Convexity (for price_change)."},
                    "yield_change": {"type": "number", "description": "Change in yield as decimal (for price_change)."},
                    "current_price": {"type": "number", "description": "Current bond price (for ytm or price_change)."},
                },
                "required": ["calculate"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "statistics_calculator",
            "description": "Portfolio and statistics calculations: weighted portfolio return, portfolio risk (std dev from correlation matrix), Sharpe ratio, utility function, covariance.",
            "parameters": {
                "type": "object",
                "properties": {
                    "calculate": {
                        "type": "string",
                        "enum": ["portfolio_return", "portfolio_risk", "sharpe_ratio", "utility", "covariance"],
                        "description": "What to calculate.",
                    },
                    "weights": {"type": "array", "items": {"type": "number"}, "description": "Portfolio weights."},
                    "returns": {"type": "array", "items": {"type": "number"}, "description": "Expected returns."},
                    "std_devs": {"type": "array", "items": {"type": "number"}, "description": "Standard deviations."},
                    "correlation_matrix": {
                        "type": "array",
                        "items": {"type": "array", "items": {"type": "number"}},
                        "description": "Correlation matrix (NxN).",
                    },
                    "risk_free_rate": {"type": "number", "description": "Risk-free rate as decimal."},
                    "risk_aversion": {"type": "number", "description": "Risk aversion coefficient A."},
                    "expected_return": {"type": "number", "description": "Expected return for Sharpe/utility."},
                    "std_dev": {"type": "number", "description": "Standard deviation for Sharpe/utility."},
                },
                "required": ["calculate"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "economics_calculator",
            "description": "Economics and rates: Taylor rule, risk premium buildup, CAPM cost of equity, Fisher effect.",
            "parameters": {
                "type": "object",
                "properties": {
                    "calculate": {
                        "type": "string",
                        "enum": ["taylor_rule", "risk_premium_buildup", "capm", "fisher_effect"],
                        "description": "What to calculate.",
                    },
                    "neutral_rate": {"type": "number", "description": "Neutral real policy rate."},
                    "target_inflation": {"type": "number", "description": "Target inflation rate."},
                    "expected_inflation": {"type": "number", "description": "Expected inflation rate."},
                    "current_inflation": {"type": "number", "description": "Current inflation rate."},
                    "gdp_growth": {"type": "number", "description": "Actual GDP growth rate."},
                    "potential_gdp_growth": {"type": "number", "description": "Potential GDP growth rate."},
                    "inflation_weight": {"type": "number", "description": "Weight on inflation gap (default 0.5)."},
                    "gdp_weight": {"type": "number", "description": "Weight on output gap (default 0.5)."},
                    "real_risk_free": {"type": "number", "description": "Real risk-free rate."},
                    "inflation_premium": {"type": "number", "description": "Inflation premium."},
                    "default_risk_premium": {"type": "number", "description": "Default risk premium."},
                    "liquidity_premium": {"type": "number", "description": "Liquidity premium."},
                    "maturity_premium": {"type": "number", "description": "Maturity premium."},
                    "equity_risk_premium": {"type": "number", "description": "Equity risk premium."},
                    "beta": {"type": "number", "description": "Beta coefficient."},
                    "country_premium": {"type": "number", "description": "Country risk premium."},
                    "risk_free_rate": {"type": "number", "description": "Nominal risk-free rate (for CAPM)."},
                    "market_return": {"type": "number", "description": "Expected market return (for CAPM)."},
                },
                "required": ["calculate"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "general_math",
            "description": "Evaluate a math expression. Supports all Python math module functions (sqrt, log, exp, sin, cos, etc.) and basic arithmetic. Use for simple calculations that don't fit other tools.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Math expression to evaluate, e.g. '(1.05**10 - 1) / 0.05' or 'sqrt(0.04**2 + 0.03**2)'.",
                    },
                },
                "required": ["expression"],
            },
        },
    },
]

# Dispatch table: name -> callable
TOOL_DISPATCH = {
    "tvm_calculator": tvm_calculator,
    "bond_calculator": bond_calculator,
    "statistics_calculator": statistics_calculator,
    "economics_calculator": economics_calculator,
    "general_math": general_math,
}


def execute_tool(name: str, args: dict) -> Dict[str, Any]:
    """Execute a tool by name with given arguments."""
    fn = TOOL_DISPATCH.get(name)
    if fn is None:
        return {"error": f"Unknown tool: '{name}'"}
    try:
        return fn(**args)
    except Exception as e:
        return {"error": f"Tool execution failed: {e}"}
