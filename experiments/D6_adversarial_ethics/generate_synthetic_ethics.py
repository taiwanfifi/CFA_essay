#!/usr/bin/env python3
"""Generate synthetic CFA ethics questions for D6 adversarial testing.

Creates novel CFA ethics MCQs covering Standards I-VII that have never appeared
in public CFA prep materials, addressing the memorization confound.

Usage:
    python -m experiments.D6_adversarial_ethics.generate_synthetic_ethics --n-per-standard 15
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from experiments.shared.config import MODEL_REGISTRY
from experiments.shared.llm_client import LLMClient

OUTPUT_DIR = Path(__file__).parent / "synthetic_questions"

# CFA Ethics Standards with descriptions for diverse question generation
CFA_STANDARDS = {
    "I_A_knowledge_of_law": {
        "name": "Standard I(A) – Knowledge of the Law",
        "description": "Members must understand and comply with all applicable laws, rules, and regulations. When conflicts exist between local law and CFA standards, follow the stricter requirement.",
        "scenarios": [
            "cross-border trading where local law conflicts with CFA Standards",
            "regulatory reporting requirements in emerging market jurisdictions",
            "whistleblower protections when discovering firm-level violations",
            "new cryptocurrency regulations conflicting with existing compliance frameworks",
            "social media policies and securities law around online stock promotion",
        ],
    },
    "I_B_independence_objectivity": {
        "name": "Standard I(B) – Independence and Objectivity",
        "description": "Members must use reasonable care to maintain independence and objectivity in professional activities. Do not offer, solicit, or accept gifts that could compromise independence.",
        "scenarios": [
            "analyst receiving corporate hospitality from a company under coverage",
            "portfolio manager pressured by investment banking division to issue favorable rating",
            "research analyst offered exclusive data access by a hedge fund client",
            "sell-side analyst spouse working at a company the analyst covers",
            "fund manager receiving luxury gifts from broker-dealer seeking order flow",
        ],
    },
    "I_C_misrepresentation": {
        "name": "Standard I(C) – Misrepresentation",
        "description": "Members must not knowingly make misrepresentations relating to investment analysis, recommendations, actions, or other professional activities.",
        "scenarios": [
            "marketing materials omitting key risk factors for a structured product",
            "backtest results presented as actual performance track record",
            "cherry-picking favorable time periods for performance reporting",
            "AI-generated research presented as human analyst work without disclosure",
            "selectively quoting economic data to support a predetermined investment thesis",
        ],
    },
    "II_A_material_nonpublic": {
        "name": "Standard II(A) – Material Nonpublic Information",
        "description": "Members who possess material nonpublic information must not act or cause others to act on it.",
        "scenarios": [
            "overhearing merger discussion in elevator at client's headquarters",
            "receiving preliminary earnings data from corporate IR before public release",
            "social media post by CEO hinting at unannounced product launch",
            "data vendor providing satellite imagery suggesting supply chain disruption",
            "consultant sharing aggregated industry data that reveals individual company trends",
        ],
    },
    "III_A_loyalty_prudence_care": {
        "name": "Standard III(A) – Loyalty, Prudence, and Care",
        "description": "Members must act for the benefit of clients and place clients' interests before their own or their employer's interests.",
        "scenarios": [
            "allocating hot IPO shares between personal account and client accounts",
            "recommending proprietary fund products over lower-cost alternatives",
            "executing block trade that benefits largest client at expense of smaller clients",
            "wealth manager steering elderly client toward products with higher commissions",
            "pension fund trustee investing in employer's stock beyond prudent levels",
        ],
    },
    "III_C_suitability": {
        "name": "Standard III(C) – Suitability",
        "description": "Members must make reasonable inquiry into clients' investment experience, risk tolerance, and financial situation before making recommendations.",
        "scenarios": [
            "recommending leveraged ETFs to conservative retirement account",
            "placing aggressive growth fund in portfolio of 85-year-old widow",
            "advising concentrated stock position without assessing client's total wealth",
            "recommending alternative investments without verifying accredited investor status",
            "using same model portfolio for clients with vastly different time horizons",
        ],
    },
    "IV_A_loyalty_to_employer": {
        "name": "Standard IV(A) – Loyalty to Employer",
        "description": "Members must act for the benefit of their employer and not cause harm to their employer.",
        "scenarios": [
            "analyst preparing to leave firm while soliciting clients for new employer",
            "portfolio manager developing proprietary trading strategy on employer's time",
            "using employer's research platform and data for personal consulting business",
            "revealing firm's proprietary risk model methodology to competitors during job interview",
            "employee retaining copies of client lists and proprietary models after resignation",
        ],
    },
    "V_A_diligence_reasonable_basis": {
        "name": "Standard V(A) – Diligence and Reasonable Basis",
        "description": "Members must exercise diligence, independence, and thoroughness in analyzing investments and making recommendations.",
        "scenarios": [
            "issuing buy recommendation based solely on management guidance without independent verification",
            "using outdated financial models without updating key assumptions",
            "relying entirely on third-party research without independent analysis",
            "recommending complex derivative strategy without understanding Greeks and tail risks",
            "making portfolio changes based on single macroeconomic indicator without broader analysis",
        ],
    },
    "VI_A_disclosure_conflicts": {
        "name": "Standard VI(A) – Disclosure of Conflicts",
        "description": "Members must make full and fair disclosure of all matters that could impair independence and objectivity.",
        "scenarios": [
            "analyst owning shares in company being recommended to clients",
            "advisory firm receiving referral fees from third-party fund managers",
            "board member providing investment advice to company where they serve as director",
            "broker-dealer earning soft dollar credits not disclosed to advisory clients",
            "analyst's compensation tied to investment banking revenue from covered companies",
        ],
    },
    "VII_A_conduct_cfa_member": {
        "name": "Standard VII(A) – Conduct as Participants in CFA Programs",
        "description": "Members must not engage in conduct that compromises the reputation or integrity of CFA Institute or the CFA designation.",
        "scenarios": [
            "CFA candidate sharing exam questions on online forum after test",
            "charterholder misrepresenting CFA designation in professional bio",
            "using CFA mark in misleading way to imply guaranteed investment returns",
            "candidate accessing unauthorized study materials derived from actual exam content",
            "charterholder failing to report colleague's violation of CFA Standards",
        ],
    },
}

GENERATION_PROMPT = """You are an expert CFA exam question writer specializing in Ethics & Standards of Professional Conduct.

Generate {n} NOVEL multiple-choice ethics questions for CFA exam preparation. Each question must:
1. Test knowledge of {standard_name}
2. Use ORIGINAL scenarios not found in standard CFA prep materials (SchweserNotes, Kaplan, AnalystPrep)
3. Have exactly 3 options (A, B, C) with ONE correct answer
4. Include realistic financial context with specific names, figures, and situations
5. Test the application of ethical principles, not just definition recall

Use these scenario contexts for inspiration (but create your own unique variations):
{scenario_hints}

IMPORTANT: Each question must be completely self-contained and test a DIFFERENT ethical nuance.

Return your response as a JSON array. Each element must have exactly these fields:
- "query": The full question text including "A: ...", "B: ...", "C: ..." options (each option on a new line)
- "answer": The correct letter ("A", "B", or "C")
- "standard": "{standard_code}"
- "explanation": A brief explanation of why the answer is correct (1-2 sentences)

Output ONLY the JSON array, no other text."""


def generate_questions_for_standard(
    client: LLMClient,
    standard_code: str,
    standard_info: dict,
    n_per_standard: int,
) -> list:
    """Generate synthetic ethics questions for one CFA Standard."""
    scenario_hints = "\n".join(f"- {s}" for s in standard_info["scenarios"])

    prompt = GENERATION_PROMPT.format(
        n=n_per_standard,
        standard_name=standard_info["name"],
        scenario_hints=scenario_hints,
        standard_code=standard_code,
    )

    messages = [
        {"role": "system", "content": "You are a CFA exam question writer. Output valid JSON only."},
        {"role": "user", "content": prompt},
    ]

    response = client.chat(messages, temperature=0.7, max_tokens=8000)
    content = response.content.strip()

    # Parse JSON from response (handle markdown code blocks)
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    content = content.strip()

    try:
        questions = json.loads(content)
    except json.JSONDecodeError:
        # Try to extract JSON array
        start = content.find("[")
        end = content.rfind("]") + 1
        if start >= 0 and end > start:
            questions = json.loads(content[start:end])
        else:
            print(f"    WARN: Failed to parse JSON for {standard_code}")
            return []

    # Validate and format
    valid_questions = []
    for q in questions:
        if not all(k in q for k in ("query", "answer", "standard")):
            continue
        if q["answer"] not in ("A", "B", "C"):
            continue
        valid_questions.append(q)

    return valid_questions


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic CFA ethics questions")
    parser.add_argument("--n-per-standard", type=int, default=15,
                        help="Questions per CFA Standard (default: 15)")
    parser.add_argument("--model", default="gpt-4o-mini",
                        help="Model for generation (default: gpt-4o-mini)")
    args = parser.parse_args()

    config = MODEL_REGISTRY[args.model]
    client = LLMClient(config)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    all_questions = []
    for code, info in CFA_STANDARDS.items():
        print(f"  Generating {args.n_per_standard} questions for {info['name']}...")
        questions = generate_questions_for_standard(
            client, code, info, args.n_per_standard
        )
        print(f"    Got {len(questions)} valid questions")
        all_questions.extend(questions)
        time.sleep(1)  # Rate limit courtesy

    # Assign unique IDs
    for i, q in enumerate(all_questions):
        q["id"] = f"synth_ethics_{i:03d}"
        q["dataset"] = "synthetic_ethics"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = OUTPUT_DIR / f"synthetic_ethics_{timestamp}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_questions, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"Generated {len(all_questions)} synthetic ethics questions")
    print(f"Saved to: {output_path}")

    # Summary by standard
    from collections import Counter
    std_counts = Counter(q.get("standard", "unknown") for q in all_questions)
    for std, count in sorted(std_counts.items()):
        print(f"  {std}: {count}")


if __name__ == "__main__":
    main()
