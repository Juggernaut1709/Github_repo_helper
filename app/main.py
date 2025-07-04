from fastapi import FastAPI, UploadFile, File
from app.rag_pipeline import create_qa_pipeline
from app.utils import extract_zip
from pydantic import BaseModel
import shutil
import os

app = FastAPI()
qa_chain = None

@app.post("/upload")
async def upload_repo(file: UploadFile = File(...)):
    path = f"uploaded.zip"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    extract_zip(path)
    global qa_chain
    qa_chain = create_qa_pipeline()
    return {"message": "Repository uploaded and indexed."}

class Question(BaseModel):
    query: str

@app.post("/ask")
def ask_q(question: Question):
    if not qa_chain:
        return {"error": "Please upload a repository first."}
    answer = qa_chain.run(question.query)
    return {"answer": answer}