from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from pathlib import Path
from app.config import OPENAI_API_KEY, CHUNK_SIZE, CHUNK_OVERLAP
import os

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def load_and_chunk_repo(path, exts={".py", ".c", ".cpp", ".go"}, skip_dirs={"venv", ".git", "node_modules", "__pycache__"}):
    docs = []
    for file in Path(path).rglob("*"):
        if any(skip in file.parts for skip in skip_dirs):
            continue
        if not file.is_file() or file.suffix not in exts:
            continue
        try:
            loader = TextLoader(str(file), encoding="utf-8")
            loaded_docs = loader.load()
            for doc in loaded_docs:
                doc.metadata["source"] = str(file)
                docs.append(doc)
        except Exception as e:
            print(f"Skipped {file} due to {e}")
    return docs

def create_qa_pipeline(repo_path="repo"):
    docs = load_and_chunk_repo(repo_path)
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = splitter.split_documents(docs)
    embedding = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(chunks, embedding=embedding)
    retriever = vectordb.as_retriever(search_type="similarity", k=4)
    qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(temperature=0), retriever=retriever)
    return qa_chain