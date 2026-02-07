"""A1 Open-Ended Benchmark: Three-level evaluation of CFA answers.

Usage:
    python -m experiments.A1_open_ended.run_experiment --dataset easy --limit 5 --model gpt-4o-mini

    # Resume interrupted run:
    python -m experiments.A1_open_ended.run_experiment --resume experiments/A1_open_ended/results/run_XXXXXXXX_XXXXXX
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from experiments.shared.config import MODEL_REGISTRY
from experiments.shared.data_loader import load_dataset
from experiments.shared.llm_client import LLMClient

from .config import OPEN_ENDED_SYSTEM
from .transform import strip_choices_and_instruction, generate_gold_answer
from .evaluator import evaluate_response
from .error_attribution import attribute_error

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


def run(args):
    """Main experiment runner."""
    if args.model not in MODEL_REGISTRY:
        print(f"Unknown model: {args.model}. Available: {list(MODEL_REGISTRY.keys())}")
        sys.exit(1)

    config = MODEL_REGISTRY[args.model]
    client = LLMClient(config)
    judge_client = LLMClient(MODEL_REGISTRY["gpt-4o-mini"])

    questions = load_dataset(args.dataset, args.limit)

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
        print(f"A1 Open-Ended Benchmark (RESUMING)")
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

    print(f"A1 Open-Ended Benchmark")
    print(f"  Model: {args.model}")
    print(f"  Dataset: {args.dataset} ({len(questions)} questions)")
    print(f"  Judge: gpt-4o-mini")
    print(f"  Output: {output_dir}")
    print()

    level_counts = {"exact": 0, "directional": 0, "incorrect": 0}
    # Count levels from resumed results
    for r in results:
        level_counts[r["level"]] = level_counts.get(r["level"], 0) + 1

    for i, q in enumerate(questions):
        if q["id"] in done_ids:
            continue

        print(f"  [{i+1}/{len(questions)}] {q['id']}...", end=" ", flush=True)

        # Step 1: Generate gold answer for this question
        gold = generate_gold_answer(q, judge_client)

        # Step 2: Strip choices and get model's open-ended response
        open_text = strip_choices_and_instruction(q["query"])
        messages = [
            {"role": "system", "content": OPEN_ENDED_SYSTEM},
            {"role": "user", "content": open_text},
        ]
        response = client.chat(messages, temperature=0.0, max_tokens=2000)

        # Step 3: Three-level evaluation
        evaluation = evaluate_response(
            question_text=open_text,
            student_response=response.content,
            gold_answer=gold,
            judge_client=judge_client,
        )

        level = evaluation["level"]
        level_counts[level] = level_counts.get(level, 0) + 1

        # Step 4: Error attribution for Level C
        error_attr = None
        if level == "incorrect":
            error_attr = attribute_error(
                question_text=open_text,
                student_response=response.content,
                gold_answer=gold.get("answer_text", q["answer"]),
                client=judge_client,
            )

        result = {
            "question_id": q["id"],
            "correct_answer_letter": q["answer"],
            "gold_answer": {
                "numerical": gold.get("numerical_answer"),
                "text": gold.get("answer_text", ""),
                "concept": gold.get("concept", ""),
            },
            "model_response": response.content[:500],
            "level": level,
            "evaluation": {
                "reasoning": evaluation["reasoning"],
                "auto_graded": evaluation["auto_graded"],
                "student_value": evaluation.get("student_value"),
                "gold_value": evaluation.get("gold_value"),
            },
            "error_attribution": error_attr,
            "tokens": response.prompt_tokens + response.completion_tokens,
        }
        results.append(result)
        _append_checkpoint(checkpoint_path, result)

        level_label = {"exact": "A", "directional": "B", "incorrect": "C"}[level]
        print(f"Level {level_label}")

    # Summary
    n = len(results)
    summary = {
        "n_questions": n,
        "level_distribution": {
            "exact": level_counts.get("exact", 0),
            "directional": level_counts.get("directional", 0),
            "incorrect": level_counts.get("incorrect", 0),
        },
        "level_rates": {
            "exact": round(level_counts.get("exact", 0) / n, 4) if n else 0,
            "directional": round(level_counts.get("directional", 0) / n, 4) if n else 0,
            "incorrect": round(level_counts.get("incorrect", 0) / n, 4) if n else 0,
        },
        "strict_accuracy": round(level_counts.get("exact", 0) / n, 4) if n else 0,
        "lenient_accuracy": round(
            (level_counts.get("exact", 0) + level_counts.get("directional", 0)) / n, 4
        ) if n else 0,
    }

    # Error attribution summary
    error_cats = {}
    for r in results:
        if r.get("error_attribution"):
            cat = r["error_attribution"]["error_category"]
            error_cats[cat] = error_cats.get(cat, 0) + 1
    summary["error_categories"] = error_cats

    # Save final results
    output = {
        "metadata": {
            "experiment": "A1_open_ended",
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
    print(f"  Level A (Exact):       {level_counts.get('exact', 0)}/{n} "
          f"({summary['level_rates']['exact']:.1%})")
    print(f"  Level B (Directional): {level_counts.get('directional', 0)}/{n} "
          f"({summary['level_rates']['directional']:.1%})")
    print(f"  Level C (Incorrect):   {level_counts.get('incorrect', 0)}/{n} "
          f"({summary['level_rates']['incorrect']:.1%})")
    print(f"  Strict accuracy (A only): {summary['strict_accuracy']:.1%}")
    print(f"  Lenient accuracy (A+B):   {summary['lenient_accuracy']:.1%}")
    if error_cats:
        print(f"\n  Error categories:")
        for cat, count in sorted(error_cats.items(), key=lambda x: x[1], reverse=True):
            print(f"    {cat}: {count}")
    print(f"  Results saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="A1: Open-Ended CFA Benchmark")
    parser.add_argument("--dataset", default="easy", choices=["easy", "challenge", "both"])
    parser.add_argument("--limit", type=int, default=0, help="Max questions (0=all)")
    parser.add_argument("--model", default="gpt-4o-mini", help="Model to test")
    parser.add_argument("--resume", type=str, default=None,
                        help="Path to previous run directory to resume from")
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
