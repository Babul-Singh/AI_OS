from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
from backends.workflow.graph import app_graph
from backends.services.voice_chat import text_to_speech
from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str

app = FastAPI()

@app.get("/")
def home():

    return {
        "message": "AI Multi-Agent OS Running"
    }

@app.post("/chat")
def chat(request: ChatRequest):

    result = app_graph.invoke({

        "user_input": request.query

    })
    
    print("GRAPH RESULT:")
    print(result)

    return {
        "response": result["response"]
    }

@app.post("/upload")

async def upload_pdf(file: UploadFile = File(...)):

    file_location = f"uploaded_{file.filename}"

    with open(file_location, "wb") as f:

        f.write(await file.read())

    result = app_graph.invoke({

        "user_input": file.filename,

        "file_path": file_location
    })

    return {

        "response": result["response"]
    }

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