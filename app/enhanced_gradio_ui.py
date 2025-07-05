import gradio as gr
from app.rag_pipeline import create_qa_pipeline
from app.utils import extract_zip
import time
import random

qa_chain = None
question_count = 0
upload_time = None

def upload_file(file):
    if file is None:
        return "⚠️ Please select a file to upload!", update_stats()
    
    try:
        global upload_time
        upload_time = time.time()
        zip_path = file.name
        extract_zip(zip_path)
        global qa_chain
        qa_chain = create_qa_pipeline()
        return "✅ Repository uploaded and indexed successfully! 🎉", update_stats()
    except Exception as e:
        return f"❌ Error processing file: {str(e)}", update_stats()

def answer_question(question):
    global question_count
    if not qa_chain:
        return "⚠️ Please upload a repository first!", update_stats()
    
    if not question.strip():
        return "⚠️ Please enter a question!", update_stats()
    
    try:
        question_count += 1
        response = qa_chain.run(question)
        return response, update_stats()
    except Exception as e:
        return f"❌ Error processing question: {str(e)}", update_stats()

def update_stats():
    if qa_chain:
        elapsed = int(time.time() - upload_time) if upload_time else 0
        return f"📊 Repository: ✅ Active | Questions Asked: {question_count} | Session Time: {elapsed}s"
    return "📊 No repository uploaded yet. Upload a ZIP file to get started!"

def get_example_questions():
    return [
        "What does the main function do?",
        "How is user authentication implemented?",
        "What are the key classes in this project?",
        "How does the database connection work?",
        "What APIs are exposed by this service?",
        "How is error handling implemented?",
        "What dependencies does this project have?",
        "How is the project structured?",
        "What design patterns are used?",
        "How is data validation handled?"
    ]

def get_motivational_quote():
    quotes = [
        "💡 Code is like humor. When you have to explain it, it's bad.",
        "🚀 The best code is no code at all.",
        "✨ First, solve the problem. Then, write the code.",
        "🎯 Code never lies, comments sometimes do.",
        "🔥 Any code of your own that you haven't looked at for six or more months might as well have been written by someone else."
    ]
    return random.choice(quotes)

def change_theme(theme_name):
    theme_styles = {
        "Ocean": {
            "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "accent": "#4ecdc4",
            "secondary": "#ff6b6b"
        },
        "Sunset": {
            "gradient": "linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%)",
            "accent": "#ff6b6b",
            "secondary": "#4ecdc4"
        },
        "Forest": {
            "gradient": "linear-gradient(135deg, #134e5e 0%, #71b280 100%)",
            "accent": "#71b280",
            "secondary": "#134e5e"
        },
        "Galaxy": {
            "gradient": "linear-gradient(135deg, #434343 0%, #000000 100%)",
            "accent": "#bb86fc",
            "secondary": "#03dac6"
        },
        "Cyber": {
            "gradient": "linear-gradient(135deg, #0f3460 0%, #e94560 100%)",
            "accent": "#e94560",
            "secondary": "#0f3460"
        },
        "Mint": {
            "gradient": "linear-gradient(135deg, #2afadf 0%, #4c83ff 100%)",
            "accent": "#2afadf",
            "secondary": "#4c83ff"
        },
        "Neon": {
            "gradient": "linear-gradient(135deg, #ff00ff 0%, #00ffff 100%)",
            "accent": "#ff00ff",
            "secondary": "#00ffff"
        },
        "Fire": {
            "gradient": "linear-gradient(135deg, #ff4500 0%, #ff6347 50%, #ff8c00 100%)",
            "accent": "#ff4500",
            "secondary": "#ff8c00"
        },
        "Purple Rain": {
            "gradient": "linear-gradient(135deg, #8a2be2 0%, #9932cc 50%, #ba55d3 100%)",
            "accent": "#8a2be2",
            "secondary": "#ba55d3"
        },
        "Electric": {
            "gradient": "linear-gradient(135deg, #00ff00 0%, #32cd32 50%, #7fff00 100%)",
            "accent": "#00ff00",
            "secondary": "#32cd32"
        }
    }
    
    selected_theme = theme_styles.get(theme_name, theme_styles["Ocean"])
    
    # Return CSS that will be injected
    return f"""
    <style>
        .gradio-container {{
            background: {selected_theme['gradient']} !important;
        }}
        :root {{
            --primary-gradient: {selected_theme['gradient']} !important;
            --accent-color: {selected_theme['accent']} !important;
            --accent-secondary: {selected_theme['secondary']} !important;
        }}
        .btn-primary {{
            background: linear-gradient(45deg, {selected_theme['secondary']}, {selected_theme['accent']}) !important;
        }}
    </style>
    """

# Enhanced CSS with working theme system
custom_css = """
/* Global styles */
:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --accent-color: #4ecdc4;
    --accent-secondary: #ff6b6b;
    --text-light: #ffffff;
    --text-dark: #333333;
    --glass-bg: rgba(255, 255, 255, 0.15);
    --glass-border: rgba(255, 255, 255, 0.25);
}

.gradio-container {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    background: var(--primary-gradient) !important;
    min-height: 100vh !important;
    position: relative !important;
    overflow-x: hidden !important;
}

/* Animated background particles */
.gradio-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        radial-gradient(circle at 25% 25%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 75% 75%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
    animation: float 6s ease-in-out infinite;
    pointer-events: none;
    z-index: -1;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
}

/* Compact theme selector in top right corner */
.theme-selector {
    position: absolute !important;
    top: 15px !important;
    right: 15px !important;
    z-index: 1000 !important;
    width: 140px !important;
    background: var(--glass-bg) !important;
    backdrop-filter: blur(10px) !important;
    border-radius: 10px !important;
    border: 1px solid var(--glass-border) !important;
    padding: 8px 10px !important;
    box-shadow: 0 2px 15px rgba(0, 0, 0, 0.2) !important;
    font-size: 12px !important;
}

.theme-selector .gr-label {
    font-size: 11px !important;
    margin-bottom: 3px !important;
    color: var(--text-light) !important;
    font-weight: 500 !important;
}

.theme-selector .gr-dropdown {
    min-height: 25px !important;
}

.theme-selector .gr-dropdown .gr-button {
    min-height: 25px !important;
    font-size: 11px !important;
    padding: 3px 8px !important;
    border-radius: 6px !important;
    background: rgba(255, 255, 255, 0.9) !important;
    border: 1px solid var(--glass-border) !important;
}

.theme-selector .gr-dropdown .gr-button:hover {
    background: rgba(255, 255, 255, 1) !important;
}

/* Header styling with large logo */
.main-header {
    background: var(--glass-bg) !important;
    backdrop-filter: blur(20px) !important;
    border-radius: 30px !important;
    border: 2px solid var(--glass-border) !important;
    padding: 50px 40px !important;
    margin: 60px 0 30px 0 !important;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3) !important;
    text-align: center !important;
    position: relative !important;
    overflow: hidden !important;
}

.main-header::before {
    content: '';
    position: absolute;
    top: -50px;
    right: -50px;
    width: 150px;
    height: 150px;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
    animation: rotate 15s linear infinite;
}

@keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

/* Large attractive title */
.main-title {
    font-size: 4rem !important;
    font-weight: 900 !important;
    color: var(--text-light) !important;
    margin: 0 !important;
    text-shadow: 0 4px 8px rgba(0, 0, 0, 0.5) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 20px !important;
    animation: pulse 3s ease-in-out infinite !important;
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3)) !important;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

.github-logo {
    font-size: 4rem !important;
    filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3)) !important;
    animation: bounce 2s ease-in-out infinite !important;
}

@keyframes bounce {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

/* Card styling */
.upload-card, .question-card, .stats-card {
    background: var(--glass-bg) !important;
    backdrop-filter: blur(15px) !important;
    border-radius: 25px !important;
    border: 1px solid var(--glass-border) !important;
    padding: 35px !important;
    margin: 25px 0 !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
    transition: all 0.3s ease !important;
    position: relative !important;
    overflow: hidden !important;
}

.upload-card::before {
    content: '📁';
    position: absolute;
    top: -20px;
    right: -20px;
    font-size: 120px;
    opacity: 0.08;
}

.question-card::before {
    content: '🧠';
    position: absolute;
    top: -20px;
    right: -20px;
    font-size: 120px;
    opacity: 0.08;
}

.stats-card::before {
    content: '📊';
    position: absolute;
    top: -20px;
    right: -20px;
    font-size: 120px;
    opacity: 0.08;
}

.upload-card:hover, .question-card:hover, .stats-card:hover {
    transform: translateY(-8px) !important;
    box-shadow: 0 16px 50px rgba(0, 0, 0, 0.4) !important;
}

/* Enhanced button styling */
.btn-primary {
    background: linear-gradient(45deg, var(--accent-secondary), var(--accent-color)) !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 18px 40px !important;
    font-weight: bold !important;
    font-size: 18px !important;
    color: var(--text-light) !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3) !important;
    position: relative !important;
    overflow: hidden !important;
}

.btn-primary::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
    transition: left 0.5s;
}

.btn-primary:hover::before {
    left: 100%;
}

.btn-primary:hover {
    transform: translateY(-4px) scale(1.05) !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4) !important;
}

/* Textbox styling */
.large-textbox textarea, .answer-textbox textarea {
    min-height: 120px !important;
    font-size: 16px !important;
    border-radius: 15px !important;
    border: 2px solid var(--glass-border) !important;
    background: rgba(255, 255, 255, 0.95) !important;
    color: var(--text-dark) !important;
    padding: 20px !important;
    transition: all 0.3s ease !important;
    box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.1) !important;
}

.answer-textbox textarea {
    min-height: 220px !important;
    font-family: 'Courier New', monospace !important;
}

.large-textbox textarea:focus, .answer-textbox textarea:focus {
    border-color: var(--accent-color) !important;
    box-shadow: 0 0 20px rgba(78, 205, 196, 0.4) !important;
    transform: scale(1.02) !important;
}

/* Status box styling */
.status-box input {
    border-radius: 15px !important;
    border: 2px solid var(--glass-border) !important;
    background: rgba(255, 255, 255, 0.95) !important;
    color: var(--text-dark) !important;
    padding: 20px !important;
    font-size: 16px !important;
    font-weight: bold !important;
    transition: all 0.3s ease !important;
}

/* File upload styling */
.file-upload {
    border: 3px dashed var(--glass-border) !important;
    border-radius: 20px !important;
    background: var(--glass-bg) !important;
    padding: 35px !important;
    transition: all 0.3s ease !important;
    position: relative !important;
}

.file-upload::before {
    content: '📤';
    position: absolute;
    top: 15px;
    right: 15px;
    font-size: 50px;
    opacity: 0.3;
}

.file-upload:hover {
    border-color: var(--accent-color) !important;
    background: rgba(255, 255, 255, 0.2) !important;
    transform: scale(1.02) !important;
}

/* Example buttons */
.example-btn {
    background: var(--glass-bg) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 25px !important;
    padding: 12px 24px !important;
    margin: 8px !important;
    color: var(--text-light) !important;
    font-size: 14px !important;
    transition: all 0.3s ease !important;
    cursor: pointer !important;
    backdrop-filter: blur(5px) !important;
}

.example-btn:hover {
    background: rgba(255, 255, 255, 0.3) !important;
    transform: scale(1.05) translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3) !important;
}

/* Labels and text */
.gr-label {
    color: var(--text-light) !important;
    font-weight: bold !important;
    font-size: 20px !important;
    margin-bottom: 15px !important;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.4) !important;
}

.markdown-text {
    color: var(--text-light) !important;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5) !important;
}

.markdown-text h1 {
    color: var(--text-light) !important;
    font-size: 2.5em !important;
    margin-bottom: 20px !important;
}

.markdown-text h2 {
    color: var(--text-light) !important;
    font-size: 2em !important;
    margin-bottom: 15px !important;
}

.markdown-text h3 {
    color: var(--text-light) !important;
    font-size: 1.5em !important;
    margin-bottom: 10px !important;
}

/* Input and textarea general styling */
input, textarea {
    color: var(--text-dark) !important;
    background: rgba(255, 255, 255, 0.95) !important;
}

input::placeholder, textarea::placeholder {
    color: #666666 !important;
    font-style: italic !important;
}

/* Responsive design */
@media (max-width: 768px) {
    .main-title {
        font-size: 2.5rem !important;
        flex-direction: column !important;
        gap: 10px !important;
    }
    
    .github-logo {
        font-size: 2.5rem !important;
    }
    
    .upload-card, .question-card, .stats-card {
        padding: 25px !important;
        margin: 15px 0 !important;
    }
    
    .main-header {
        padding: 30px 20px !important;
        margin: 50px 0 30px 0 !important;
    }
    
    .btn-primary {
        padding: 15px 30px !important;
        font-size: 16px !important;
    }
    
    .theme-selector {
        width: 120px !important;
        font-size: 10px !important;
        padding: 6px 8px !important;
    }
    
    .theme-selector .gr-label {
        font-size: 10px !important;
    }
    
    .theme-selector .gr-dropdown .gr-button {
        font-size: 10px !important;
        padding: 2px 6px !important;
    }
}
"""

# Create the enhanced Gradio interface
with gr.Blocks(css=custom_css, title="🐙 GitHub Repo Helper", theme=gr.themes.Base()) as demo:
    
    # Compact theme selector in top right corner
    with gr.Column(elem_classes="theme-selector"):
        theme_dropdown = gr.Dropdown(
            choices=["Ocean", "Sunset", "Forest", "Galaxy", "Cyber", "Mint", "Neon", "Fire", "Purple Rain", "Electric"],
            value="Ocean",
            label="🎨 Theme",
            interactive=True,
            container=False,
            scale=1
        )
    
    # Dynamic theme injection
    theme_css = gr.HTML(visible=False)
    
    # Header section with large attractive title
    with gr.Column(elem_classes="main-header"):
        gr.HTML("""
        <div class="main-title">
            <span class="github-logo">🐙</span>
            <span>GitHub Repo Helper</span>
        </div>
        """)
        gr.Markdown("""
        ## Intelligent Repository Analysis with RAG Technology
        
        🚀 **Upload your GitHub repository and unlock the power of AI-driven code analysis!**
        
        ✨ Get instant insights • 🔍 Understand complex functions • 📊 Explore your codebase with natural language
        """, elem_classes="markdown-text")
    
    # Upload section
    with gr.Column(elem_classes="upload-card"):
        gr.Markdown("## 📁 Upload Your Repository", elem_classes="markdown-text")
        
        with gr.Row():
            with gr.Column(scale=3):
                uploader = gr.File(
                    label="📂 Drop your ZIP file here or click to browse", 
                    file_types=[".zip"],
                    elem_classes="file-upload"
                )
            with gr.Column(scale=1):
                upload_button = gr.Button(
                    "🚀 Upload & Process", 
                    variant="primary",
                    elem_classes="btn-primary"
                )
        
        upload_status = gr.Textbox(
            label="📊 Upload Status", 
            interactive=False,
            elem_classes="status-box"
        )
    
    # Question section
    with gr.Column(elem_classes="question-card"):
        gr.Markdown("## 🧠 Ask Questions About Your Code", elem_classes="markdown-text")
        
        with gr.Row():
            with gr.Column(scale=4):
                question = gr.Textbox(
                    label="💬 What would you like to know?",
                    placeholder="e.g., How does the authentication system work? What are the main components?",
                    elem_classes="large-textbox"
                )
            with gr.Column(scale=1):
                ask_button = gr.Button(
                    "🔍 Analyze", 
                    variant="primary",
                    elem_classes="btn-primary"
                )
        
        # Example questions
        gr.Markdown("### 💡 Quick Questions to Get Started:", elem_classes="markdown-text")
        with gr.Row():
            example_questions = get_example_questions()
            for i in range(0, len(example_questions), 2):
                with gr.Column():
                    if i < len(example_questions):
                        gr.Button(
                            f"🎯 {example_questions[i]}", 
                            elem_classes="example-btn"
                        ).click(
                            lambda x=example_questions[i]: x,
                            outputs=question
                        )
                    if i + 1 < len(example_questions):
                        gr.Button(
                            f"🎯 {example_questions[i + 1]}", 
                            elem_classes="example-btn"
                        ).click(
                            lambda x=example_questions[i + 1]: x,
                            outputs=question
                        )
        
        # Answer section
        answer = gr.Textbox(
            label="🤖 AI Analysis Results",
            interactive=False,
            elem_classes="answer-textbox"
        )
    
    # Stats section
    with gr.Column(elem_classes="stats-card"):
        gr.Markdown("## 📈 Session Dashboard", elem_classes="markdown-text")
        stats_display = gr.Textbox(
            label="📊 Live Statistics",
            value=update_stats(),
            interactive=False,
            elem_classes="status-box"
        )
        
        # Action buttons
        with gr.Row():
            clear_button = gr.Button(
                "🗑️ Clear Session", 
                variant="secondary",
                elem_classes="btn-primary"
            )
    
    # Event handlers
    def update_all_outputs(file):
        status, stats = upload_file(file)
        return status, stats
    
    def ask_and_update(question):
        answer_text, stats = answer_question(question)
        return answer_text, stats
    
    upload_button.click(
        update_all_outputs,
        inputs=uploader,
        outputs=[upload_status, stats_display]
    )
    
    ask_button.click(
        ask_and_update,
        inputs=question,
        outputs=[answer, stats_display]
    )
    
    def clear_all():
        global qa_chain, question_count, upload_time
        qa_chain = None
        question_count = 0
        upload_time = None
        return "", "", "🔄 Session cleared! Upload a new repository to start fresh.", update_stats()
    
    clear_button.click(
        clear_all,
        outputs=[question, answer, upload_status, stats_display]
    )
    
    # Theme change functionality
    def apply_theme(theme_name):
        css_code = change_theme(theme_name)
        return css_code
    
    theme_dropdown.change(
        apply_theme,
        inputs=theme_dropdown,
        outputs=[theme_css]
    )

# Launch configuration
if __name__ == "__main__":
    demo.launch(
        share=True,
        inbrowser=True,
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True,
        debug=True
    )