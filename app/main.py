from fastapi import FastAPI, Request, UploadFile, File, Form
from typing import Optional
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.utils import extract_zip, clone_github_repo
from app.rag_pipeline import create_qa_pipeline
import shutil
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

qa_chain = None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_repo(
    githubUrl: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    repo_path = "repo"
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)

    if githubUrl:
        success = clone_github_repo(githubUrl, repo_path)
        if not success:
            return {"message": "❌ Failed to clone GitHub repository."}
    elif file:
        with open("uploaded.zip", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        extract_zip("uploaded.zip", repo_path)
    else:
        return {"message": "❌ Please provide either a GitHub URL or a ZIP file."}
    global qa_chain
    qa_chain = create_qa_pipeline(repo_path)
    return {"message": "✅ Repository indexed successfully."}

@app.post("/ask")
async def ask_question(request: Request, question: str = Form(...)):
    if not qa_chain:
        return {"answer": "⚠️ Please upload a repository first!"}
    answer = qa_chain.run(question)
    return {"answer": answer}