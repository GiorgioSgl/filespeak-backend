import sys

from fastapi import FastAPI
from .routers import users
from .chat import chat_interface
import gradio as gr

version = f"{sys.version_info.major}.{sys.version_info.minor}"

app = FastAPI()

app.include_router(users.router)
#app.include_router(chat.router)

@app.get("/")
async def read_root():
    message = f"Hello world! From FastAPI running on Uvicorn with Gunicorn. Using Python {version}"
    return {"message": message}

# Montar Gradio como subaplicación en /chat
app = gr.mount_gradio_app(app, chat_interface, path="/chat")