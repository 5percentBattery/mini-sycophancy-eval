from pathlib import Path

from inspect_ai import Task, task
from inspect_ai.dataset import json_dataset
from inspect_ai.scorer import model_graded_qa


@task
def preopinionated() -> Task:
    dataset_path = str(Path(__file__).parent.parent / "resources" / "preopinionated.json")
    return Task(
        dataset=json_dataset(
            dataset_path,
            auto_id=True,
        ),
        scorer=model_graded_qa(include_history=True),
        model_roles={"grader": "openai/gpt-6-luna"}
    )