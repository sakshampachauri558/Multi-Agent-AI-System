import json
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, Field

load_dotenv(Path(__file__).with_name(".env"))

app = FastAPI(title="ResearchMind")
INDEX_FILE = Path(__file__).parent / "public" / "index.html"
logger = logging.getLogger(__name__)


class ResearchRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=200)


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(INDEX_FILE)


@app.get("/api/health")
def health():
    return {"status": "ok"}


def _stream_pipeline(topic: str):
    from pipeline import iter_research_pipeline

    try:
        for event in iter_research_pipeline(topic):
            yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"
    except Exception as exc:
        logger.exception("Research pipeline failed")
        error_event = {
            "step": "error",
            "status": "error",
            "message": str(exc) or type(exc).__name__,
        }
        yield f"data: {json.dumps(error_event, ensure_ascii=False)}\n\n"


@app.post("/api/research")
def research(request: ResearchRequest):
    topic = request.topic.strip()
    if not topic:
        raise HTTPException(status_code=400, detail="Enter a research topic.")

    missing_keys = [
        key for key in ("MISTRAL_API_KEY", "TAVILY_API_KEY") if not os.getenv(key)
    ]
    if missing_keys:
        raise HTTPException(
            status_code=503,
            detail=f"Configure the required environment variables: {', '.join(missing_keys)}.",
        )

    return StreamingResponse(
        _stream_pipeline(topic),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "X-Accel-Buffering": "no",
        },
    )
