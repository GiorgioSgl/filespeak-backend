
from fastapi.responses import HTMLResponse
from fastapi import APIRouter

router = APIRouter()

@router.get("/upload/ui", response_class=HTMLResponse, include_in_schema=False)
async def upload_ui():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>File Upload</title>
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
                margin: 10px 5px;
                padding: 10px 20px;
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .btn-danger {
                background-color: #dc3545;
            }
            #result, #file-list {
                margin-top: 20px;
                white-space: pre-wrap;
                text-align: left;
                max-width: 600px;
                margin-left: auto;
                margin-right: auto;
                background: #f9f9f9;
                padding: 15px;
                border-radius: 10px;
            }
        </style>
    </head>
    <body>
        <h2>Upload your files (PDF, DOCX, TXT, HTML)</h2>
        <div id="drop-area">
            <form class="my-form">
                <p>Drag and drop files here, or</p>
                <input type="file" id="fileElem" multiple onchange="handleFiles(this.files)">
                <label class="btn" for="fileElem">Select files</label>
            </form>
        </div>

        <div>
            <button class="btn" onclick="refreshFileList()">🔄 Refresh list</button>
            <button class="btn btn-danger" onclick="resetFiles()">🗑️ Reset</button>
        </div>

        <h3>Uploaded Files:</h3>
        <div id="file-list">The list of files will appear here.</div>

        <h3>Result:</h3>
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

            dropArea.addEventListener('dragenter', () => dropArea.classList.add('highlight'), false);
            dropArea.addEventListener('dragover', () => dropArea.classList.add('highlight'), false);
            dropArea.addEventListener('dragleave', () => dropArea.classList.remove('highlight'), false);
            dropArea.addEventListener('drop', () => dropArea.classList.remove('highlight'), false);

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
                refreshFileList(); // Refresh after upload
            }

            async function refreshFileList() {
                const response = await fetch("/ls");
                const files = await response.json();
                document.getElementById("file-list").textContent = 
                    files.length ? files.join("\\n") : "No files found.";
            }

            async function resetFiles() {
                if (!confirm("Are you sure you want to delete all uploaded files?")) return;
                const response = await fetch("/reset", { method: "POST" });
                const text = await response.text();
                document.getElementById("result").textContent = text;
                refreshFileList();
            }

            // Load file list on page load
            refreshFileList();
        </script>
    </body>
    </html>
    """
