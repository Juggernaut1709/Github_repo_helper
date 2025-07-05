from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.utils import extract_zip
from app.rag_pipeline import create_qa_pipeline
import shutil

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

qa_chain = None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    with open("uploaded.zip", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    global qa_chain
    extract_zip("uploaded.zip")
    qa_chain = create_qa_pipeline()
    return {"message": "Repository uploaded and indexed."}

@app.post("/ask")
async def ask_question(request: Request, question: str = Form(...)):
    if not qa_chain:
        return {"answer": "⚠️ Please upload a repository first!"}
    answer = qa_chain.run(question)
    return {"answer": answer}