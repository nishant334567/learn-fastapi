from fastapi import APIRouter
from pydantic import BaseModel

from core.job_graph import job_app

router = APIRouter(prefix="/agent", tags=["agent"])


class ApplyInput(BaseModel):
    jd: str
    resume: str


@router.post("/apply")
async def apply(data: ApplyInput):
    return await job_app.ainvoke(
        {
            "jd": data.jd,
            "resume": data.resume,
            "jd_skills": [],
            "resume_skills": [],
            "score": 0,
            "cover_letter": None,
            "reason": "",
        }
    )
