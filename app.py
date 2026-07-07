import os
import json
import asyncio
import tempfile
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Resume Scoring Agent")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    # Save uploaded PDF to a temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, run_evaluation, tmp_path)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def run_evaluation(pdf_path: str) -> dict:
    """Runs the full hiring-agent pipeline and returns a dict."""
    from pdf import PDFHandler
    from github import GitHubHandler
    from evaluator import Evaluator
    from llm_utils import get_llm
    from transform import transform_resume
    import models

    llm = get_llm()
    pdf_handler = PDFHandler(llm)
    raw_resume = pdf_handler.process(pdf_path)
    resume = transform_resume(raw_resume)

    github_username = None
    github_data = {}
    profiles = resume.get("basics", {}).get("profiles", [])
    for p in profiles:
        if isinstance(p, dict) and "github" in p.get("url", "").lower():
            github_username = p.get("username") or p.get("url", "").rstrip("/").split("/")[-1]
            break

    if github_username:
        gh_handler = GitHubHandler(llm)
        github_data = gh_handler.analyze(github_username)

    evaluator = Evaluator(llm)
    evaluation = evaluator.evaluate(resume, github_data)

    scores = evaluation.get("scores", {})
    return {
        "name": resume.get("basics", {}).get("name", "Unknown Candidate"),
        "github_username": github_username or "Not found in resume",
        "scores": {
            "open_source": scores.get("open_source", 0),
            "self_projects": scores.get("self_projects", 0),
            "production": scores.get("production", 0),
            "technical_skills": scores.get("technical_skills", 0),
            "bonus": scores.get("bonus", 0),
            "deductions": scores.get("deductions", 0),
            "total": scores.get("total", 0),
        },
        "evidence": evaluation.get("evidence", []),
        "summary": evaluation.get("summary", ""),
    }
