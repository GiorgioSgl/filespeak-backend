from fastapi import APIRouter
import gradio as gr
from .my_chromadb import collection
from openai import OpenAI
from decouple import config

client = OpenAI(api_key=config("OPENAI_API_KEY"))

chat_router = APIRouter()


def find_document(message):
    results = collection.query(
        query_texts=[message],
        n_results=1
    )

    if not results or not results['documents']:
        return "No se encontraron resultados."

    return results["documents"][0]


def chat_with_agent(message, history):
    
    messages = [
        {"role": "system", "content": "You are document manager and you should use the document I passed you to answer. If document are not founding so please dont answer."},
        {"role": "user", "content": f"Here are the documents:\n{find_document(message)}\n"},
        {"role": "user", "content": f"Here the history of the chat: {str(history)}"},
        {"role": "user", "content": message}
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.3
    )

    return response.choices[0].message.content

def respond(message, history):
    return chat_with_agent(message, history)

chat_interface = gr.ChatInterface(fn=respond, title="Chat desde router")