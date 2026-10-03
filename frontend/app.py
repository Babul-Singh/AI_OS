from asyncio import timeout
from fastapi.responses import StreamingResponse
import chainlit as cl
import httpx

@cl.on_message
async def main(message: cl.Message):

    print("HANDLER STARTED")

    timeout = httpx.Timeout(
        connect=30.0,
        read=None,
        write=30.0,
        pool=30.0
    )

    async with httpx.AsyncClient(timeout=timeout) as client:

        response = await client.post(
            "http://127.0.0.1:8000/chat",
            json={
                "query": message.content
            }
        )

    print("STATUS:", response.status_code)

    if response.status_code != 200:
        await cl.Message(
            content=f"Backend Error ({response.status_code})\n\n{response.text}"
        ).send()
        return

    data = response.json()

    print("DATA RECEIVED")

    response_text = str(data["response"])

    print("RESPONSE LENGTH:", len(response_text))

    response_text = str(data["response"])

    print("TYPE:", type(response_text))
    print("LENGTH:", len(response_text))

    await cl.Message(
        content=response_text
    ).send()

    print("MESSAGE SENT")

    #await msg.send()
    #async for token in httpx.stream:
        #await msg.stream_token(token)
    #await msg.update()

    
  