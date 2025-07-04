import gradio as gr
from app.rag_pipeline import create_qa_pipeline
from app.utils import extract_zip

qa_chain = None

def upload_file(file):
    zip_path = file.name
    extract_zip(zip_path)
    global qa_chain
    qa_chain = create_qa_pipeline()
    return "✅ Repository uploaded and indexed."

def answer_question(question):
    if not qa_chain:
        return "⚠️ Please upload a repo first!"
    return qa_chain.run(question)

with gr.Blocks() as demo:
    gr.Markdown("# 🤖 GitHub Repo Assistant\nUpload a zipped GitHub repo and ask questions about its contents.")

    with gr.Row():
        uploader = gr.File(label="Upload ZIP", file_types=[".zip"])
        upload_button = gr.Button("Upload & Index")

    upload_status = gr.Textbox(label="Status")

    upload_button.click(upload_file, inputs=uploader, outputs=upload_status)

    with gr.Row():
        question = gr.Textbox(label="Ask a Question")
        answer = gr.Textbox(label="Answer")
        ask_button = gr.Button("Ask")

    ask_button.click(answer_question, inputs=question, outputs=answer)

demo.launch()