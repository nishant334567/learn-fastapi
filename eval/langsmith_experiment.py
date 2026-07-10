import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

load_dotenv()

from langsmith import aevaluate

from core.job_graph import job_app

DATASET_NAME = "job-apply-v1"


async def run_graph(inputs: dict) -> dict:
    return await job_app.ainvoke(
        {
            "jd": inputs["jd"],
            "resume": inputs["resume"],
            "jd_skills": [],
            "resume_skills": [],
            "score": 0,
            "cover_letter": None,
            "reason": "",
        }
    )


def routing_correct(outputs: dict, reference_outputs: dict) -> bool:
    drafted = outputs.get("cover_letter") is not None
    return drafted == reference_outputs["should_draft"]


def score_in_band(outputs: dict, reference_outputs: dict) -> bool:
    score = outputs.get("score", 0)
    if "score_min" in reference_outputs and score < reference_outputs["score_min"]:
        return False
    if "score_max" in reference_outputs and score > reference_outputs["score_max"]:
        return False
    return True


async def main():
    await aevaluate(
        run_graph,
        data=DATASET_NAME,
        evaluators=[routing_correct, score_in_band],
        experiment_prefix="job-apply-v1",
    )
    print("Done. Check LangSmith → job-apply-v1 → Experiments")


if __name__ == "__main__":
    asyncio.run(main())
