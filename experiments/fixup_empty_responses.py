#!/usr/bin/env python3
"""Fix-up script: re-run questions that got empty responses due to
max_completion_tokens being too low for GPT-5-mini reasoning models.

Reads a checkpoint.jsonl, identifies empty-response entries, re-runs them
with the fixed llm_client (higher token budget), and writes a merged checkpoint.

Usage:
    # Fix A1 empty responses
    python -m experiments.fixup_empty_responses \
        --experiment A1 \
        --checkpoint experiments/A1_open_ended/results/run_XXXXXXXX/checkpoint.jsonl

    # Fix E1 empty responses
    python -m experiments.fixup_empty_responses \
        --experiment E1 \
        --checkpoint experiments/E1_error_analysis/results/checkpoint_gpt-5-mini_XXXXXXXX.jsonl

    # Dry run (just count empty responses)
    python -m experiments.fixup_empty_responses \
        --experiment A1 \
        --checkpoint experiments/A1_open_ended/results/run_XXXXXXXX/checkpoint.jsonl \
        --dry-run
"""

import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from experiments.shared.config import MODEL_REGISTRY
from experiments.shared.llm_client import LLMClient


def find_empty_responses(checkpoint_path: Path, experiment: str) -> list:
    """Identify entries with empty model responses."""
    empty_ids = []
    with open(checkpoint_path, "r") as f:
        for line in f:
            r = json.loads(line.strip())
            if experiment == "A1":
                if len(r.get("model_response", "")) == 0:
                    empty_ids.append(r["question_id"])
            elif experiment == "A5":
                if r.get("answer_with") is None:
                    empty_ids.append(r["question_id"])
            elif experiment == "I1":
                if r["original"].get("answer") is None:
                    empty_ids.append(r["question_id"])
            elif experiment == "I3":
                if r.get("clean_answer") is None:
                    empty_ids.append(r["question_id"])
            elif experiment == "E1":
                if r.get("model_response_length", 0) < 10:
                    empty_ids.append(r["question_id"])
    return empty_ids


def fixup_a1(checkpoint_path: Path, empty_ids: set, model: str):
    """Re-run A1 questions with empty responses."""
    from experiments.shared.data_loader import load_dataset
    from experiments.A1_open_ended.config import OPEN_ENDED_SYSTEM
    from experiments.A1_open_ended.transform import strip_choices_and_instruction, generate_gold_answer
    from experiments.A1_open_ended.evaluator import evaluate_response
    from experiments.A1_open_ended.error_attribution import attribute_error

    client = LLMClient(MODEL_REGISTRY[model])
    judge_client = LLMClient(MODEL_REGISTRY["gpt-4o-mini"])
    questions = load_dataset("easy", 0)
    q_lookup = {q["id"]: q for q in questions}

    # Read existing checkpoint
    existing = []
    with open(checkpoint_path, "r") as f:
        for line in f:
            existing.append(json.loads(line.strip()))

    fixed_count = 0
    for i, entry in enumerate(existing):
        qid = entry["question_id"]
        if qid not in empty_ids:
            continue

        q = q_lookup.get(qid)
        if not q:
            continue

        print(f"  Fixing [{fixed_count+1}/{len(empty_ids)}] {qid}...", end=" ", flush=True)

        gold = generate_gold_answer(q, judge_client)
        open_text = strip_choices_and_instruction(q["query"])
        messages = [
            {"role": "system", "content": OPEN_ENDED_SYSTEM},
            {"role": "user", "content": open_text},
        ]
        response = client.chat(messages, temperature=0.0, max_tokens=2000)

        if len(response.content.strip()) == 0:
            print(f"STILL EMPTY (tokens={response.prompt_tokens+response.completion_tokens})")
            continue

        evaluation = evaluate_response(
            question_text=open_text,
            student_response=response.content,
            gold_answer=gold,
            judge_client=judge_client,
        )
        level = evaluation["level"]

        error_attr = None
        if level == "incorrect":
            error_attr = attribute_error(
                question_text=open_text,
                student_response=response.content,
                gold_answer=gold.get("answer_text", q["answer"]),
                client=judge_client,
            )

        existing[i] = {
            "question_id": qid,
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
        fixed_count += 1
        level_label = {"exact": "A", "directional": "B", "incorrect": "C"}[level]
        print(f"Level {level_label} (fixed!)")

    # Write merged checkpoint
    merged_path = checkpoint_path.parent / "checkpoint_fixed.jsonl"
    with open(merged_path, "w") as f:
        for entry in existing:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"\n  Fixed {fixed_count}/{len(empty_ids)} entries")
    print(f"  Merged checkpoint: {merged_path}")
    return merged_path, existing


def main():
    parser = argparse.ArgumentParser(description="Fix empty GPT-5-mini responses")
    parser.add_argument("--experiment", required=True, choices=["A1", "A5", "I1", "I3", "E1"])
    parser.add_argument("--checkpoint", required=True, help="Path to checkpoint.jsonl")
    parser.add_argument("--model", default="gpt-5-mini")
    parser.add_argument("--dry-run", action="store_true", help="Just count empty responses")
    args = parser.parse_args()

    cp = Path(args.checkpoint)
    if not cp.is_absolute():
        cp = Path(__file__).resolve().parent.parent / args.checkpoint

    empty_ids = find_empty_responses(cp, args.experiment)
    print(f"Found {len(empty_ids)} empty responses in {cp.name}")

    if args.dry_run:
        for qid in empty_ids[:20]:
            print(f"  {qid}")
        if len(empty_ids) > 20:
            print(f"  ... and {len(empty_ids)-20} more")
        return

    if not empty_ids:
        print("No empty responses to fix!")
        return

    if args.experiment == "A1":
        fixup_a1(cp, set(empty_ids), args.model)
    else:
        print(f"Fixup for {args.experiment} not yet implemented (low empty rate, likely not needed)")


if __name__ == "__main__":
    main()
