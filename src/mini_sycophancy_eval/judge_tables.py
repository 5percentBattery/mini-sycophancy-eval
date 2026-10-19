"""
Summarize rejection_flips eval logs: one table per judge, one row per model under test.

Expects a directory laid out as <logs>/<judge>/<model>/*.eval, with one log per task.
A "flag" is a sample the judge graded "I" (the assistant flipped its answer).
"""

import argparse
import math
from collections import defaultdict
from pathlib import Path

from inspect_ai.log import read_eval_log

SCORER = "model_graded_qa"
FLAG = "I"


def sample_flag_rates(log_dir: Path) -> tuple[int, int, list[float]]:
    """Return (flags, total, per-question flag rates) pooled over every log in log_dir."""
    flags = total = 0
    per_question: dict[tuple[str, object], list[int]] = defaultdict(list)
    for path in sorted(log_dir.glob("*.eval")):
        log = read_eval_log(str(path))
        if log.status != "success":
            raise ValueError(f"{path} has status {log.status!r}")
        for sample in log.samples or []:
            flagged = int(sample.scores[SCORER].value == FLAG)
            flags += flagged
            total += 1
            per_question[(log.eval.task, sample.id)].append(flagged)
    rates = [sum(v) / len(v) for v in per_question.values()]
    return flags, total, rates


def stderr(rates: list[float]) -> float:
    """Standard error of the mean over questions, averaging epochs first (as inspect does)."""
    n = len(rates)
    if n < 2:
        return 0.0
    mean = sum(rates) / n
    variance = sum((r - mean) ** 2 for r in rates) / (n - 1)
    return math.sqrt(variance / n)


def judge_table(judge_dir: Path) -> str:
    rows = ["| model | #flags | %flags | stderr |", "|---|---|---|---|"]
    for model_dir in sorted(p for p in judge_dir.iterdir() if p.is_dir()):
        flags, total, rates = sample_flag_rates(model_dir)
        rows.append(
            f"| {model_dir.name} | {flags}/{total} | {100 * flags / total:.1f}% "
            f"| {100 * stderr(rates):.1f}% |"
        )
    return "\n".join(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("logs", type=Path, nargs="?", default=Path("v0.2 logs"))
    args = parser.parse_args()
    for judge_dir in sorted(p for p in args.logs.iterdir() if p.is_dir()):
        print(f"### {judge_dir.name}\n")
        print(judge_table(judge_dir))
        print()


if __name__ == "__main__":
    main()
