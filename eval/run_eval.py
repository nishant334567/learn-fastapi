import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.job_graph import job_app

DATASET_PATH = Path(__file__).parent / "dataset.json"
cases = json.loads(DATASET_PATH.read_text())


def check(result, expected):
    drafted = result["cover_letter"] is not None
    if drafted != expected["should_draft"]:
        return False

    score = result["score"]
    if "score_min" in expected and score < expected["score_min"]:
        return False
    if "score_max" in expected and score > expected["score_max"]:
        return False

    return True


async def run_eval():
    passed = 0
    failed = 0
    for case in cases:
        result = await job_app.ainvoke(
            {
                "jd": case["jd"],
                "resume": case["resume"],
                "jd_skills": [],
                "resume_skills": [],
                "score": 0,
                "cover_letter": None,
                "reason": "",
            }
        )

        ok = check(result, case["expected"])
        if ok:
            passed += 1
            print("PASSED", case["id"], "Score:", result["score"])
        else:
            failed += 1
            print("FAILED", case["id"], "Score:", result["score"])

    print(f"Routing accuracy: {passed}/{passed + failed}")


if __name__ == "__main__":
    asyncio.run(run_eval())
