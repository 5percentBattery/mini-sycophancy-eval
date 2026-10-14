from dotenv import load_dotenv
from inspect_ai import eval

from mini_sycophancy_eval.preopinionated import preopinionated
from mini_sycophancy_eval.sycophancyprobe import sycophancyprobe


def main() -> None:
    load_dotenv()
    eval(
        [
            sycophancyprobe("src/resources/disputes.csv"), 
            preopinionated("src/resources/preopinionated.json")
        ],
        model="openai/gpt-5.4-nano"
    )
