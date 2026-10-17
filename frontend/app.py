import chainlit as cl
import httpx


BACKEND_URL = "http://127.0.0.1:8000"


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

        file_id = None

        # ==========================================
        # CHECK FOR ATTACHED FILE
        # ==========================================

        if message.elements:

            print("FILES ATTACHED:", len(message.elements))

            for element in message.elements:

                print("ELEMENT:", element)

                # Get file path
                file_path = getattr(
                    element,
                    "path",
                    None
                )

                if not file_path:
                    continue

                print("FILE PATH:", file_path)

                # Only PDF files
                mime = getattr(
                    element,
                    "mime",
                    ""
                )

                if mime and mime != "application/pdf":

                    await cl.Message(
                        content="Please upload a PDF file."
                    ).send()

                    return

                # ==========================================
                # UPLOAD PDF TO FASTAPI
                # ==========================================

                with open(file_path, "rb") as f:

                    files = {
                        "file": (
                            getattr(
                                element,
                                "name",
                                "document.pdf"
                            ),
                            f,
                            "application/pdf"
                        )
                    }

                    upload_response = await client.post(
                        f"{BACKEND_URL}/upload",
                        files=files
                    )

                print(
                    "UPLOAD STATUS:",
                    upload_response.status_code
                )

                if upload_response.status_code != 200:

                    await cl.Message(
                        content=(
                            f"File upload failed "
                            f"({upload_response.status_code})\n\n"
                            f"{upload_response.text}"
                        )
                    ).send()

                    return

                upload_data = upload_response.json()

                print(
                    "UPLOAD DATA:",
                    upload_data
                )

                file_id = upload_data["file_id"]

                print(
                    "FILE ID:",
                    file_id
                )

                break

        # ==========================================
        # SEND QUESTION TO BACKEND
        # ==========================================

        request_data = {
            "query": message.content
        }

        if file_id:

            request_data["file_id"] = file_id

            print(
                "Sending question with file:",
                file_id
            )

        response = await client.post(
            f"{BACKEND_URL}/chat",
            json=request_data
        )

    # ==========================================
    # BACKEND RESPONSE
    # ==========================================

    print(
        "STATUS:",
        response.status_code
    )

    if response.status_code != 200:

        await cl.Message(
            content=(
                f"Backend Error "
                f"({response.status_code})\n\n"
                f"{response.text}"
            )
        ).send()

        return

    data = response.json()

    print("DATA RECEIVED")

    response_text = data.get("response", "No response received.")

    print(
        "RESPONSE LENGTH:",
        len(response_text)
    )

    await cl.Message(content=str(response_text)).send()

    print("MESSAGE SENT")