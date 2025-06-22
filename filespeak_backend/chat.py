from fastapi import APIRouter
import gradio as gr
from .my_chromadb import collection
from openai import OpenAI
from decouple import config

client = OpenAI(api_key=config("OPENAI_API_KEY"))

chat_router = APIRouter()


def find_document(message, threshold=0.9):
    results = collection.query(
        query_texts=[message],
        n_results=2
    )

    if not results or not results['documents']:
        return "No se encontraron resultados."
    
    # Filtrar los resultados por distancia
    filtered_docs = []
    for doc, dist, metadata, doc_id in zip(
        results["documents"][0],
        results["distances"][0],
        results["metadatas"][0],
        results["ids"][0]
    ):
        if dist < threshold:
            filtered_docs.append({
                "id": doc_id,
                "document": doc,
                "distance": dist,
                "metadata": metadata
            })

    if len(filtered_docs) == 0:
        return "No relevant documents were found."
    
    source_first_doc = filtered_docs[0]["metadata"]["source"]

    docs = collection.get(
        where={"source": source_first_doc}
    )["documents"]

    for doc in filtered_docs[1:]:
        docs.append(doc)

    return docs


def chat_with_agent(message, history):
    documents = find_document(message)
    messages = [
        {"role": "system", "content": "You are document manager and you should use the document I passed you to answer. If document are not founding so please dont answer."},
        {"role": "user", "content": f"Here are the documents:\n{documents}\n"},
        {"role": "user", "content": f"Here the history of the chat: {str(history)}"},
        {"role": "user", "content": message}
    ]
    print("documents:", len(documents))

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        temperature=0.3
    )

    return response.choices[0].message.content

def respond(message, history):
    return chat_with_agent(message, history)

chat_interface = gr.ChatInterface(fn=respond, title="Docuement Agent")