#!/usr/bin/env python3
"""
E1 Golden Context Injection Experiment.

Tests whether injecting correct CFA concept hints into the prompt
can recover errors made by the model in open-ended answering.

This distinguishes:
  - Knowledge Gap errors (fixed by context → RAG is effective)
  - Reasoning Gap errors (still wrong despite context → needs fine-tuning)

Usage:
    python -m experiments.E1_error_analysis.golden_context \
        --a1-results experiments/A1_open_ended/results/run_20260206_173445/results.json \
        --model gpt-4o-mini --limit 50

    # Full run (all 557 errors)
    python -m experiments.E1_error_analysis.golden_context \
        --a1-results experiments/A1_open_ended/results/run_20260206_173445/results.json \
        --model gpt-4o-mini
"""

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from experiments.shared.config import MODEL_REGISTRY
from experiments.shared.data_loader import load_cfa_easy
from experiments.shared.llm_client import LLMClient

RESULTS_DIR = Path(__file__).parent / "results"


def _load_checkpoint(checkpoint_path: Path) -> list:
    """Load completed results from a JSONL checkpoint file."""
    results = []
    if checkpoint_path.exists():
        with open(checkpoint_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    results.append(json.loads(line))
    return results


def _append_checkpoint(checkpoint_path: Path, result: dict):
    """Append a single result to the JSONL checkpoint file."""
    with open(checkpoint_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(result, ensure_ascii=False) + "\n")

# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

BASELINE_SYSTEM = (
    "You are a CFA exam expert. Solve the following problem step by step. "
    "Show all calculations, state all assumptions, and give your final "
    "answer clearly. Do NOT refer to multiple-choice options."
)

GOLDEN_CONTEXT_SYSTEM = (
    "You are a CFA exam expert. You are given a hint about the key concept "
    "being tested. Use this hint to guide your reasoning. Solve the problem "
    "step by step, show all calculations, and give your final answer clearly. "
    "Do NOT refer to multiple-choice options."
)

GOLDEN_CONTEXT_USER = """Hint: This question tests the concept of "{concept}".

Question:
{question}"""

JUDGE_SYSTEM = """You are a CFA exam grading assistant. Compare the student's response to the gold standard answer.

Evaluate the student's answer:
- "exact": Student's final answer matches the gold answer (within 2% tolerance for numerical, or semantically equivalent for text)
- "directional": Student's approach/reasoning is correct but the final answer differs (wrong assumptions, incomplete, etc.)
- "incorrect": Student's answer is fundamentally wrong

Respond in JSON:
{"level": "exact" or "directional" or "incorrect", "reasoning": "brief explanation"}"""

JUDGE_USER = """Gold standard answer: {gold_text}
Gold concept: {gold_concept}
Gold numerical value: {gold_numerical}

Student's response:
{student_response}

Grade this response."""


# ---------------------------------------------------------------------------
# Core Functions
# ---------------------------------------------------------------------------

def strip_choices_and_instruction(query: str) -> str:
    """Remove MCQ choices and instruction prefix from a CFA query."""
    text = query
    prefix_pattern = (
        r"Read the questions and answers carefully, and choose the one "
        r"you think is appropriate among the three options A, B and C\.\s*"
    )
    text = re.sub(prefix_pattern, "", text, flags=re.IGNORECASE)
    text = re.sub(r",?\s*CHOICES\s*:.*$", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"\s*Answer\s*:\s*$", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^Q\s*:\s*", "", text.strip())
    return text.strip()


def judge_response(
    judge_client: LLMClient,
    student_response: str,
    gold_answer: dict,
) -> dict:
    """Grade a student response against gold answer."""
    gold_text = gold_answer.get("text", "")
    gold_concept = gold_answer.get("concept", "")
    gold_numerical = gold_answer.get("numerical", "N/A")

    messages = [
        {"role": "system", "content": JUDGE_SYSTEM},
        {"role": "user", "content": JUDGE_USER.format(
            gold_text=gold_text,
            gold_concept=gold_concept,
            gold_numerical=gold_numerical,
            student_response=student_response[:3000],
        )},
    ]

    response = judge_client.chat(messages, temperature=0.0, max_tokens=200)
    try:
        json_match = re.search(r'\{[^}]+\}', response.content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except json.JSONDecodeError:
        pass
    return {"level": "incorrect", "reasoning": "Judge parse error"}


def run(args):
    """Main experiment runner."""
    # Load A1 results
    a1_path = Path(args.a1_results)
    if not a1_path.exists():
        a1_path = PROJECT_ROOT / args.a1_results
    if not a1_path.exists():
        print(f"ERROR: A1 results not found: {args.a1_results}")
        sys.exit(1)

    with open(a1_path, "r", encoding="utf-8") as f:
        a1_data = json.load(f)

    # Filter to incorrect (Level C) results only
    errors = [r for r in a1_data["results"] if r["level"] == "incorrect"]
    print(f"E1 Golden Context Injection Experiment")
    print(f"  Model: {args.model}")
    print(f"  A1 source: {a1_path.name}")
    print(f"  Total A1 errors (Level C): {len(errors)}")

    if args.limit > 0:
        errors = errors[:args.limit]
        print(f"  Limit applied: {args.limit}")

    # Load CFA Easy dataset for original questions
    questions = load_cfa_easy()
    q_lookup = {q["id"]: q for q in questions}
    print(f"  CFA Easy questions loaded: {len(questions)}")

    # Initialize clients
    if args.model not in MODEL_REGISTRY:
        print(f"Unknown model: {args.model}. Available: {list(MODEL_REGISTRY.keys())}")
        sys.exit(1)

    client = LLMClient(MODEL_REGISTRY[args.model])
    judge_client = LLMClient(MODEL_REGISTRY["gpt-4o-mini"])

    print(f"  Judge: gpt-4o-mini")

    # Handle resume via checkpoint
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    checkpoint_name = f"checkpoint_{args.model}_{ts}.jsonl"
    if args.resume:
        resume_path = Path(args.resume)
        if not resume_path.is_absolute():
            resume_path = PROJECT_ROOT / args.resume
        checkpoint_path = resume_path
        existing = _load_checkpoint(checkpoint_path)
        done_ids = {r["question_id"] for r in existing}
        results = existing
        print(f"  RESUMING from: {checkpoint_path}")
        print(f"  Already completed: {len(done_ids)}/{len(errors)}")
    else:
        RESULTS_DIR.mkdir(exist_ok=True, parents=True)
        checkpoint_path = RESULTS_DIR / checkpoint_name
        done_ids = set()
        results = []

    print()

    recovery_count = sum(1 for r in results if r.get("recovery") == "full")
    partial_count = sum(1 for r in results if r.get("recovery") == "partial")
    still_wrong_count = sum(1 for r in results if r.get("recovery") == "none")

    for i, err in enumerate(errors):
        qid = err["question_id"]

        if qid in done_ids:
            continue

        q = q_lookup.get(qid)
        if not q:
            print(f"  [{i+1}/{len(errors)}] {qid}... SKIP (question not found)")
            continue

        gold_answer = err["gold_answer"]
        concept = gold_answer.get("concept", "")
        error_category = (err.get("error_attribution") or {}).get("error_category", "unknown")

        # Strip choices from original question
        question_text = strip_choices_and_instruction(q["query"])

        # Ask with golden context injection
        messages = [
            {"role": "system", "content": GOLDEN_CONTEXT_SYSTEM},
            {"role": "user", "content": GOLDEN_CONTEXT_USER.format(
                concept=concept,
                question=question_text,
            )},
        ]
        response = client.chat(messages, temperature=0.0, max_tokens=2000)

        # Judge the response
        evaluation = judge_response(judge_client, response.content, gold_answer)
        new_level = evaluation.get("level", "incorrect")

        # Classify recovery
        if new_level == "exact":
            recovery = "full"
            recovery_count += 1
            symbol = "R"
        elif new_level == "directional":
            recovery = "partial"
            partial_count += 1
            symbol = "P"
        else:
            recovery = "none"
            still_wrong_count += 1
            symbol = "X"

        print(f"  [{i+1}/{len(errors)}] {qid} ({error_category[:15]})... {symbol} ({new_level})")

        result_entry = {
            "question_id": qid,
            "original_error_category": error_category,
            "concept_hint": concept,
            "original_level": "incorrect",
            "new_level": new_level,
            "recovery": recovery,
            "judge_reasoning": evaluation.get("reasoning", ""),
            "model_response_length": len(response.content),
            "tokens": response.prompt_tokens + response.completion_tokens,
        }
        results.append(result_entry)
        _append_checkpoint(checkpoint_path, result_entry)

    # Summary
    total = len(results)
    print()
    print("=" * 60)
    print("GOLDEN CONTEXT INJECTION RESULTS")
    print("=" * 60)
    print(f"  Total errors tested:     {total}")
    print(f"  Full recovery (→exact):  {recovery_count} ({recovery_count/total*100:.1f}%)" if total else "")
    print(f"  Partial (→directional):  {partial_count} ({partial_count/total*100:.1f}%)" if total else "")
    print(f"  Still wrong:             {still_wrong_count} ({still_wrong_count/total*100:.1f}%)" if total else "")
    print(f"  Recovery rate:           {(recovery_count + partial_count)/total*100:.1f}%" if total else "")

    # Breakdown by error category
    print(f"\n--- Recovery by Error Category ---")
    cat_stats = {}
    for r in results:
        cat = r["original_error_category"]
        if cat not in cat_stats:
            cat_stats[cat] = {"total": 0, "recovered": 0, "partial": 0}
        cat_stats[cat]["total"] += 1
        if r["recovery"] == "full":
            cat_stats[cat]["recovered"] += 1
        elif r["recovery"] == "partial":
            cat_stats[cat]["partial"] += 1

    for cat, stats in sorted(cat_stats.items(), key=lambda x: -x[1]["total"]):
        t = stats["total"]
        rec = stats["recovered"]
        par = stats["partial"]
        rate = (rec + par) / t * 100 if t > 0 else 0
        print(f"  {cat:<25} {t:>4} errors | {rec:>3} full + {par:>3} partial = {rate:.1f}% recovery")

    # Save final results
    RESULTS_DIR.mkdir(exist_ok=True, parents=True)
    final_ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = RESULTS_DIR / f"golden_context_{args.model}_{final_ts}.json"

    output = {
        "metadata": {
            "experiment": "E1_golden_context_injection",
            "model": args.model,
            "a1_source": str(a1_path),
            "n_errors_tested": total,
            "timestamp": ts,
        },
        "summary": {
            "total": total,
            "full_recovery": recovery_count,
            "partial_recovery": partial_count,
            "still_wrong": still_wrong_count,
            "recovery_rate": round((recovery_count + partial_count) / total * 100, 1) if total else 0,
            "full_recovery_rate": round(recovery_count / total * 100, 1) if total else 0,
            "by_error_category": cat_stats,
        },
        "results": results,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\n  Results saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="E1 Golden Context Injection")
    parser.add_argument("--a1-results", type=str, required=True,
                        help="Path to A1 open-ended results JSON")
    parser.add_argument("--model", type=str, default="gpt-4o-mini",
                        help="Model to test")
    parser.add_argument("--limit", type=int, default=0,
                        help="Max errors to test (0 = all)")
    parser.add_argument("--resume", type=str, default=None,
                        help="Path to checkpoint JSONL file to resume from")
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
