# 🧠 GitHub Repo Helper (RAG + LangChain + FastAPI + Gradio)

This is a Retrieval-Augmented Generation (RAG) app that allows users to upload a zipped GitHub repository and ask natural language questions about its content.

### Features
- 📁 Upload and index GitHub repos
- 🤖 Ask AI questions about the code
- 🚀 FastAPI backend
- 🎨 Gradio interface for Hugging Face Spaces

### How to Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
# OR
python app/gradio_ui.py