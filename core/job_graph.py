from typing import TypedDict

from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langgraph.graph import END, StateGraph

llm = ChatOllama(model="gemma4", temperature=0.2)


class JobState(TypedDict):
    jd: str
    resume: str
    jd_skills: list[str]
    resume_skills: list[str]
    score: int
    cover_letter: str | None
    reason: str


async def parse_jd_node(state: JobState):
    prompt = ChatPromptTemplate.from_template(
        "Extract required technical skills from the job description. "
        "Return ONLY a JSON array of strings. No explanation.\n\n"
        "Job Description: {jd_text}"
    )
    chain = prompt | llm | JsonOutputParser()
    skills = await chain.ainvoke({"jd_text": state["jd"]})
    return {"jd_skills": skills}


async def parse_resume_node(state: JobState):
    prompt = ChatPromptTemplate.from_template(
        "Extract technical skills from this resume. "
        "Return ONLY a JSON array of strings. No explanation.\n\n"
        "Resume: {resume_text}"
    )
    chain = prompt | llm | JsonOutputParser()
    skills = await chain.ainvoke({"resume_text": state["resume"]})
    return {"resume_skills": skills}


async def score_fit_node(state: JobState):
    prompt = ChatPromptTemplate.from_template(
        "Score the fit between the job description skills and the resume skills. "
        "Return ONLY a number between 0 and 100. No explanation.\n\n"
        "Job Description Skills: {jd_skills}\n"
        "Resume Skills: {resume_skills}"
    )
    chain = prompt | llm | StrOutputParser()
    result = await chain.ainvoke(
        {"jd_skills": state["jd_skills"], "resume_skills": state["resume_skills"]}
    )
    return {"score": int(result.strip())}


async def draft_cover_node(state: JobState):
    prompt = ChatPromptTemplate.from_template(
        "Draft a cover letter for the job description and resume. "
        "Return the cover letter text only. No explanation.\n\n"
        "Job Description: {jd_text}\n"
        "Resume: {resume_text}"
    )
    chain = prompt | llm | StrOutputParser()
    cover_letter = await chain.ainvoke(
        {"jd_text": state["jd"], "resume_text": state["resume"]}
    )
    return {"cover_letter": cover_letter, "reason": "Cover letter drafted successfully"}


def reject_node(state: JobState):
    return {
        "cover_letter": None,
        "reason": f"Score is too low: {state['score']}",
    }


def route_by_score(state: JobState):
    return "reject" if state["score"] < 50 else "draft_cover"


job_graph = StateGraph(JobState)
job_graph.add_node("parse_jd", parse_jd_node)
job_graph.add_node("parse_resume", parse_resume_node)
job_graph.add_node("score_fit", score_fit_node)
job_graph.add_node("draft_cover", draft_cover_node)
job_graph.add_node("reject", reject_node)

job_graph.set_entry_point("parse_jd")
job_graph.add_edge("parse_jd", "parse_resume")
job_graph.add_edge("parse_resume", "score_fit")
job_graph.add_conditional_edges(
    "score_fit",
    route_by_score,
    {"reject": "reject", "draft_cover": "draft_cover"},
)
job_graph.add_edge("draft_cover", END)
job_graph.add_edge("reject", END)

job_app = job_graph.compile()
