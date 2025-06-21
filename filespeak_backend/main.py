import sys

from fastapi import FastAPI
from .routers import documents, ui
from .chat import chat_interface
import gradio as gr
from fastapi.responses import RedirectResponse, FileResponse

version = f"{sys.version_info.major}.{sys.version_info.minor}"

app = FastAPI()

app.include_router(documents.router)
app.include_router(ui.router)

@app.get("/")
async def read_root():
    return RedirectResponse(url="/chat")

favicon_path = "static/favicon.ico"
@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

app = gr.mount_gradio_app(app, chat_interface, path="/chat")