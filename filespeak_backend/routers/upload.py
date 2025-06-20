from fastapi import UploadFile, File, HTTPException, APIRouter
from fastapi.responses import PlainTextResponse
import os
from typing import List
from io import BytesIO
from PyPDF2 import PdfReader
from docx import Document

router = APIRouter()

@router.post("/upload", response_class=PlainTextResponse, tags=["upload"])
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename.lower()
    content = ""

    if filename.endswith(".txt") or filename.endswith(".html"):
        content = (await file.read()).decode("utf-8")

    elif filename.endswith(".pdf"):
        try:
            reader = PdfReader(BytesIO(await file.read()))
            content = "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error leyendo PDF: {e}")

    elif filename.endswith(".docx"):
        try:
            doc = Document(BytesIO(await file.read()))
            content = "\n".join([p.text for p in doc.paragraphs])
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error leyendo DOCX: {e}")

    else:
        raise HTTPException(status_code=400, detail="Formato de archivo no soportado.")

    print(f"\n--- Contenido de {file.filename} ---\n{content}\n")

    return f"Archivo {file.filename} recibido y procesado."