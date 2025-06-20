from fastapi import APIRouter
import gradio as gr
from gradio.routes import mount_gradio_app  # importante si usas gradio<4.25
from fastapi import FastAPI

# Creamos un router FastAPI normal
chat_router = APIRouter()

# Lógica del agente
def chat_with_agent(message, history):
    return f"Echo desde router: {message}"

def respond(message, history):
    return chat_with_agent(message, history)

# Creamos la interfaz Gradio
chat_interface = gr.ChatInterface(fn=respond, title="Chat desde router")