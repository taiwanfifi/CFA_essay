"""A5 Option Bias: Compare model performance with and without MCQ options.

Usage:
    python -m experiments.A5_option_bias.run_experiment --dataset easy --limit 5 --model gpt-4o-mini

    # Resume interrupted run:
    python -m experiments.A5_option_bias.run_experiment --resume experiments/A5_option_bias/results/run_XXXXXXXX_XXXXXX
"""

import argparse
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from experiments.shared.config import MODEL_REGISTRY
from experiments.shared.data_loader import load_cfa_easy_with_choices, load_cfa_challenge
from experiments.shared.llm_client import LLMClient
from experiments.shared.prompts import extract_answer, extract_numerical_answer

from .config import MCQ_SYSTEM, OPEN_ENDED_SYSTEM, JUDGE_SYSTEM, JUDGE_USER_TEMPLATE
from .transform import strip_choices, get_gold_answer_text

logger = logging.getLogger(__name__)

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


def evaluate_with_options(client: LLMClient, question: dict) -> dict:
    """Run the question in standard MCQ format."""
    messages = [
        {"role": "system", "content": MCQ_SYSTEM},
        {"role": "user", "content": question["query"]},
    ]
    response = client.chat(messages, temperature=0.0, max_tokens=2000)
    answer = extract_answer(response.content)
    correct = answer == question["answer"] if answer else False

    return {
        "answer": answer,
        "correct": correct,
        "response": response.content,
        "tokens": response.prompt_tokens + response.completion_tokens,
    }


def evaluate_without_options(
    client: LLMClient,
    question: dict,
    judge_client: LLMClient,
) -> dict:
    """Run the question in open-ended format (no choices)."""
    open_text = strip_choices(question["query"])

    messages = [
        {"role": "system", "content": OPEN_ENDED_SYSTEM},
        {"role": "user", "content": open_text},
    ]
    response = client.chat(messages, temperature=0.0, max_tokens=2000)

    # Try numerical matching first
    predicted_num = extract_numerical_answer(response.content)
    gold_text = get_gold_answer_text(question)
    gold_num = extract_numerical_answer(gold_text)

    if predicted_num is not None and gold_num is not None and gold_num != 0:
        # Numerical tolerance match (±2%)
        correct = abs(predicted_num - gold_num) / abs(gold_num) <= 0.02
        judge_verdict = "NUMERICAL_MATCH" if correct else "NUMERICAL_MISMATCH"
        judge_reasoning = (
            f"predicted={predicted_num}, gold={gold_num}, "
            f"diff={abs(predicted_num - gold_num) / abs(gold_num):.4f}"
        )
    else:
        # Fall back to LLM-as-judge
        judge_messages = [
            {"role": "system", "content": JUDGE_SYSTEM},
            {"role": "user", "content": JUDGE_USER_TEMPLATE.format(
                question=open_text,
                gold_answer=gold_text,
                student_answer=response.content,
            )},
        ]
        judge_response = judge_client.chat(judge_messages, temperature=0.0, max_tokens=300)

        try:
            judge_result = json.loads(judge_response.content)
            correct = judge_result.get("correct", False)
            judge_reasoning = judge_result.get("reasoning", "")
        except json.JSONDecodeError:
            correct = "correct" in judge_response.content.lower() and \
                      "incorrect" not in judge_response.content.lower()
            judge_reasoning = judge_response.content

        judge_verdict = "CORRECT" if correct else "INCORRECT"

    return {
        "answer_text": response.content[:500],
        "correct": correct,
        "judge_verdict": judge_verdict,
        "judge_reasoning": judge_reasoning,
        "tokens": response.prompt_tokens + response.completion_tokens,
    }


def run(args):
    """Main experiment runner."""
    # Load model
    if args.model not in MODEL_REGISTRY:
        print(f"Unknown model: {args.model}. Available: {list(MODEL_REGISTRY.keys())}")
        sys.exit(1)

    config = MODEL_REGISTRY[args.model]
    client = LLMClient(config)
    judge_client = LLMClient(MODEL_REGISTRY["gpt-4o-mini"])

    # Load dataset
    if args.dataset == "easy":
        questions = load_cfa_easy_with_choices(args.limit)
    elif args.dataset == "challenge":
        questions = load_cfa_challenge(args.limit)
    else:
        print(f"Dataset must be 'easy' or 'challenge', got: {args.dataset}")
        sys.exit(1)

    # Handle resume
    if args.resume:
        resume_dir = Path(args.resume)
        if not resume_dir.is_absolute():
            resume_dir = Path(__file__).resolve().parent.parent.parent / args.resume
        output_dir = resume_dir
        checkpoint_path = output_dir / "checkpoint.jsonl"
        existing = _load_checkpoint(checkpoint_path)
        done_ids = {r["question_id"] for r in existing}
        results = existing
        print(f"A5 Option Bias Experiment (RESUMING)")
        print(f"  Resumed from: {output_dir}")
        print(f"  Already completed: {len(done_ids)}/{len(questions)}")
    else:
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = RESULTS_DIR / f"run_{timestamp}"
        output_dir.mkdir()
        checkpoint_path = output_dir / "checkpoint.jsonl"
        done_ids = set()
        results = []

    print(f"A5 Option Bias Experiment")
    print(f"  Model: {args.model}")
    print(f"  Dataset: {args.dataset} ({len(questions)} questions)")
    print(f"  Judge: gpt-4o-mini")
    print(f"  Output: {output_dir}")
    print()

    for i, q in enumerate(questions):
        if q["id"] in done_ids:
            continue

        print(f"  [{i+1}/{len(questions)}] {q['id']}...", end=" ", flush=True)

        # Format A: with options
        with_opts = evaluate_with_options(client, q)

        # Format B: without options
        without_opts = evaluate_without_options(client, q, judge_client)

        option_biased = with_opts["correct"] and not without_opts["correct"]

        result = {
            "question_id": q["id"],
            "correct_answer": q["answer"],
            "correct_with_options": with_opts["correct"],
            "answer_with": with_opts["answer"],
            "correct_without_options": without_opts["correct"],
            "answer_without": without_opts["answer_text"][:200],
            "judge_verdict": without_opts["judge_verdict"],
            "option_biased": option_biased,
            "total_tokens": with_opts["tokens"] + without_opts["tokens"],
        }
        results.append(result)
        _append_checkpoint(checkpoint_path, result)

        status = "BIAS" if option_biased else ("OK" if with_opts["correct"] else "MISS")
        print(f"with={with_opts['answer']}({'✓' if with_opts['correct'] else '✗'}) "
              f"without={'✓' if without_opts['correct'] else '✗'} [{status}]")

    # Compute summary
    n = len(results)
    acc_with = sum(1 for r in results if r["correct_with_options"]) / n if n else 0
    acc_without = sum(1 for r in results if r["correct_without_options"]) / n if n else 0
    n_biased = sum(1 for r in results if r["option_biased"])
    total_tokens = sum(r["total_tokens"] for r in results)

    summary = {
        "accuracy_with_options": round(acc_with, 4),
        "accuracy_without_options": round(acc_without, 4),
        "option_bias": round(acc_with - acc_without, 4),
        "n_biased_questions": n_biased,
        "bias_rate": round(n_biased / n, 4) if n else 0,
        "total_tokens": total_tokens,
        "estimated_cost_usd": round(client.cost(total_tokens // 2, total_tokens // 2), 4),
    }

    # McNemar's test
    from experiments.shared.evaluation import mcnemar_test
    paired = [
        {"condition_a": r["correct_with_options"], "condition_b": r["correct_without_options"]}
        for r in results
    ]
    mcnemar = mcnemar_test(paired)
    summary["mcnemar_test"] = mcnemar

    # Save final results
    output = {
        "metadata": {
            "experiment": "A5_option_bias",
            "model": args.model,
            "dataset": args.dataset,
            "n_questions": n,
            "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
        },
        "summary": summary,
        "results": results,
    }

    output_path = output_dir / "results.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"  Accuracy WITH options:    {acc_with:.1%}")
    print(f"  Accuracy WITHOUT options: {acc_without:.1%}")
    print(f"  Option bias:              {acc_with - acc_without:+.1%}")
    print(f"  Biased questions:         {n_biased}/{n}")
    print(f"  McNemar p-value:          {mcnemar['p_value']:.4f}")
    print(f"  Results saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="A5: Option Bias Experiment")
    parser.add_argument("--dataset", default="easy", choices=["easy", "challenge"])
    parser.add_argument("--limit", type=int, default=0, help="Max questions (0=all)")
    parser.add_argument("--model", default="gpt-4o-mini", help="Model to test")
    parser.add_argument("--resume", type=str, default=None,
                        help="Path to previous run directory to resume from")
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
