from inspect_ai import Task, task
from inspect_ai.dataset import Sample, csv_dataset
from inspect_ai.model import ChatMessageAssistant, ChatMessageUser
from inspect_ai.scorer import model_graded_qa
from inspect_ai.solver import generate


@task
def sycophancyprobe(dataset_path="../resources/disputes.csv") -> Task:
    return Task(
        dataset=csv_dataset(
            dataset_path, 
            sample_fields=record_to_sample
        ),
        solver=generate(),
        scorer=model_graded_qa(include_history=True),
        model_roles={"grader": "openai/gpt-6-luna"},
    )

def record_to_sample(record: dict) -> Sample:
    return Sample(
        input=[
            ChatMessageUser(content=record["question"]),
            ChatMessageAssistant(content=record["response"]),
            ChatMessageUser(content=record["dispute"])
        ], 
        target=record["assertion"]
    )