
from fastapi.responses import HTMLResponse
from fastapi import APIRouter

router = APIRouter()

@router.get("/upload/ui", response_class=HTMLResponse, include_in_schema=False)
async def upload_ui():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Subida de Archivos</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
            }
            #drop-area {
                border: 2px dashed #ccc;
                border-radius: 20px;
                width: 100%;
                max-width: 600px;
                margin: auto;
                padding: 30px;
                transition: background-color 0.3s;
            }
            #drop-area.highlight {
                background-color: #f0f8ff;
            }
            #fileElem {
                display: none;
            }
            .btn {
                margin-top: 10px;
                padding: 10px 20px;
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            #result {
                margin-top: 20px;
                white-space: pre-wrap;
                text-align: left;
                max-width: 600px;
                margin-left: auto;
                margin-right: auto;
            }
        </style>
    </head>
    <body>
        <h2>Sube tus archivos (PDF, DOCX, TXT, HTML)</h2>
        <div id="drop-area">
            <form class="my-form">
                <p>Arrastra y suelta los archivos aquí, o</p>
                <input type="file" id="fileElem" multiple onchange="handleFiles(this.files)">
                <label class="btn" for="fileElem">Selecciona archivos</label>
            </form>
        </div>
        <div id="result"></div>

        <script>
            const dropArea = document.getElementById('drop-area');

            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
                dropArea.addEventListener(eventName, preventDefaults, false);
            });

            function preventDefaults(e) {
                e.preventDefault();
                e.stopPropagation();
            }

            ['dragenter', 'dragover'].forEach(eventName => {
                dropArea.addEventListener(eventName, () => dropArea.classList.add('highlight'), false);
            });

            ['dragleave', 'drop'].forEach(eventName => {
                dropArea.addEventListener(eventName, () => dropArea.classList.remove('highlight'), false);
            });

            dropArea.addEventListener('drop', handleDrop, false);

            function handleDrop(e) {
                const dt = e.dataTransfer;
                const files = dt.files;
                handleFiles(files);
            }

            async function handleFiles(files) {
                const formData = new FormData();
                for (let i = 0; i < files.length; i++) {
                    formData.append("files", files[i]);
                }

                const response = await fetch("/upload_multiple", {
                    method: "POST",
                    body: formData
                });

                const text = await response.text();
                document.getElementById("result").textContent = text;
            }
        </script>
    </body>
    </html>
    """
