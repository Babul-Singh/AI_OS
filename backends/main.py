import os
import uuid
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from backends.utils.response_formatter import format_response
from backends.services.voice_chat import text_to_speech
from backends.workflow.graph import app_graph


app = FastAPI()


# --------------------------------
# TEMPORARY FILE STORAGE
# --------------------------------

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

uploaded_files = {}


# --------------------------------
# REQUEST MODEL
# --------------------------------

class ChatRequest(BaseModel):
    query: str
    file_id: str | None = None


# --------------------------------
# HOME
# --------------------------------

@app.get("/")
def home():

    return {
        "message": "AI Multi-Agent OS Running"
    }


# --------------------------------
# CHAT
# --------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    query = request.query.strip()

    if not query:

        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty"
        )

    state = {
        "user_input": query
    }

    # If a file is attached
    if request.file_id:

        file_path = uploaded_files.get(
            request.file_id
        )

        if not file_path:

            raise HTTPException(
                status_code=404,
                detail="Uploaded file not found"
            )

        state["file_path"] = file_path

    result = app_graph.invoke(state)

    print("GRAPH RESULT:")
    print(result)

    return {
    "response": format_response(result["response"])
}


# --------------------------------
# UPLOAD
# --------------------------------

@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="Filename is missing"
        )

    # Only PDF for now
    if Path(file.filename).suffix.lower() != ".pdf":

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    # Generate unique ID
    file_id = str(uuid.uuid4())

    # Safe filename
    safe_filename = Path(
        file.filename
    ).name

    file_path = UPLOAD_DIR / f"{file_id}_{safe_filename}"

    # Save file
    with open(file_path, "wb") as f:

        f.write(
            await file.read()
        )

    # Remember file
    uploaded_files[file_id] = str(
        file_path
    )

    print("FILE UPLOADED:")
    print(file_id)
    print(file_path)

    return {

        "message": "File uploaded successfully",

        "file_id": file_id,

        "filename": safe_filename
    }


# --------------------------------
# SPEAK
# --------------------------------

@app.get("/speak")
async def speak(query: str):

    result = app_graph.invoke({
        "user_input": query
    })

    response_text = result["response"]

    audio_file = await text_to_speech(
        response_text
    )

    return {

        "text": response_text,

        "audio": audio_file
    }