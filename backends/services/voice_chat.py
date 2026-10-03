import edge_tts
import uuid

async def text_to_speech(text):

    filename = f"audio_{uuid.uuid4()}.mp3"

    communicate = edge_tts.Communicate(
        text=text,
        voice="en-US-AriaNeural"
    )

    await communicate.save(filename)

    return filename