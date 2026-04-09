"""
Self-Hosted AI API - OpenAI-Compatible Endpoint
Powered by Ollama, FastAPI, and ngrok
"""

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import requests
import os

app = FastAPI(
    title="Self-Hosted AI API",
    description="OpenAI-compatible chat completions endpoint powered by Ollama",
    version="1.0.0"
)

# Configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "127.0.0.1")
OLLAMA_PORT = os.getenv("OLLAMA_PORT", "11434")
OLLAMA_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/generate"
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "qwen:1.8b")


class Message(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    messages: List[Message]
    model: Optional[str] = DEFAULT_MODEL
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False


class ChatCompletionChoice(BaseModel):
    index: int = 0
    message: Message
    finish_reason: Optional[str] = "stop"


class ChatCompletionResponse(BaseModel):
    id: str = "chatcmpl-1"
    object: str = "chat.completion"
    created: int = 0
    model: str
    choices: List[ChatCompletionChoice]
    usage: Optional[Dict[str, int]] = None


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "ollama_url": OLLAMA_URL}


@app.get("/v1/models")
async def list_models():
    """List available models (OpenAI-compatible)"""
    return {
        "object": "list",
        "data": [
            {
                "id": DEFAULT_MODEL,
                "object": "model",
                "created": 1234567890,
                "owned_by": "ollama"
            }
        ]
    }


@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(request: ChatCompletionRequest):
    """
    Chat completions endpoint (OpenAI-compatible)

    Accepts messages in the same format as OpenAI's API
    and returns responses using Ollama's generate endpoint
    """
    try:
        # Extract the latest user message
        latest_message = request.messages[-1]
        prompt = latest_message.content

        # Build conversation history (optional - simple concatenation)
        conversation = "\n\n".join([
            f"{msg.role}: {msg.content}" for msg in request.messages
        ])

        # Call Ollama
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": request.model,
                "prompt": conversation,
                "stream": False,
                "options": {
                    "temperature": request.temperature,
                    "num_predict": request.max_tokens or 512
                }
            },
            timeout=120
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail=f"Ollama error: {response.status_code}"
            )

        result = response.json()
        assistant_message = result.get("response", "")

        return ChatCompletionResponse(
            model=request.model,
            choices=[
                ChatCompletionChoice(
                    message=Message(
                        role="assistant",
                        content=assistant_message
                    )
                )
            ],
            usage={
                "prompt_tokens": len(conversation.split()) // 4,
                "completion_tokens": len(assistant_message.split()) // 4,
                "total_tokens": (len(conversation.split()) + len(assistant_message.split())) // 4
            }
        )

    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to Ollama. Ensure it's running."
        )
    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=504,
            detail="Ollama request timed out"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/api/generate")
async def generate(request: Request):
    """Direct Ollama-compatible generate endpoint"""
    from fastapi import Request
    body = await request.json()

    try:
        response = requests.post(
            OLLAMA_URL,
            json=body,
            timeout=120
        )
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
