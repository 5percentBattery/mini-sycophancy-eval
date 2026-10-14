from dotenv import load_dotenv
from inspect_ai import eval

from mini_sycophancy_eval.sycophancyprobe import sycophancyprobe


def main() -> None:
    load_dotenv()
    eval(sycophancyprobe("src/mini_sycophancy_eval/disputes.csv"), model="openai/gpt-5.4-mini")
