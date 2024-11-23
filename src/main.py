# built-in imports
from typing import List


# fastapi imports
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn

# Mangum
from mangum import Mangum


# Clients
from src.clients.openai_client import openai_client

# Tools & Constants
from src.tools import WEATHER_TOOL, get_current_weather
from src.utils.constants import SYSTEM_PROMPT


# Utils
from src.utils import ClientMessage, convert_to_openai_messages

# Handlers
from src.handlers import handle_text_protocol, handle_data_protocol

# Config
from src.utils.config import settings

load_dotenv(".env.local")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    debug=settings.DEBUG,
)


class Request(BaseModel):
    messages: List[ClientMessage]


available_tools = {
    "get_current_weather": get_current_weather,
}


def stream_text(messages: List[ClientMessage], protocol: str = "data"):
    """
    Stream text from the OpenAI API using the provided messages and protocol.
    """
    stream = openai_client.chat.completions.create(
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
        model="gpt-4",
        stream=True,
        tools=[WEATHER_TOOL],
    )

    if protocol == "text":
        return handle_text_protocol(stream)
    elif protocol == "data":
        return handle_data_protocol(stream, available_tools)


# -------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------- #
# Routes


@app.get("/")
async def root():
    """
    Root endpoint to check if the API is running.
    """
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    """
    Health check endpoint to ensure the API is running.
    """
    return {"status": "Healthy!"}


@app.post("/api/chat")
async def chat(request: Request, protocol: str = Query("data")):
    """
    Basic chat endpoint with handling for both streaming text and data protocol.
    """
    messages = request.messages
    openai_messages = convert_to_openai_messages(messages)

    response = StreamingResponse(stream_text(openai_messages, protocol))
    response.headers["x-vercel-ai-data-stream"] = "v1"
    return response


if settings.ENVIRONMENT != "development":
    app = Mangum(app)


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
