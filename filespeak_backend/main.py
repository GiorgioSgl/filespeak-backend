import sys

from fastapi import FastAPI
from .routers import documents, ui
from .chat import chat_interface
import gradio as gr
from fastapi.responses import HTMLResponse, FileResponse

version = f"{sys.version_info.major}.{sys.version_info.minor}"

app = FastAPI()

app.include_router(documents.router)
app.include_router(ui.router)

@app.get("/", response_class=HTMLResponse)
async def homepage():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Project Access Info</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
            a { color: #007acc; text-decoration: none; }
            a:hover { text-decoration: underline; }
            .note { background: #f9f9f9; padding: 1em; border-left: 4px solid #ccc; margin-top: 2em; }
        </style>
    </head>
        <body>
            <h1>Access the Project</h1>

            <h2>Try the Application</h2>
            <ul>
                <li><a href="/upload/ui" target="_blank">Document Upload UI</a></li>
                <li><a href="/chat/" target="_blank">Chat with Agent UI</a></li>
            </ul>

            <div class="note">
                <strong>Important:</strong>
                <ul>
                    <li>You must upload one or more documents using the Document Upload UI before using the Chat with Agent feature.</li>
                    <li>The chat is designed to answer questions based only on the uploaded documents.</li>
                    <li>Both interfaces are in an early prototype stage; improvements to design and usability are planned.</li>
                </ul>
            </div>

            <p>For setup instructions and technical details, please refer to the <code>README.md</code> file in the repository.</p>
        </body>
    </html>
    """

favicon_path = "static/favicon.ico"
@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

app = gr.mount_gradio_app(app, chat_interface, path="/chat")