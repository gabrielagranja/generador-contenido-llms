"""Minimal provider-independent API foundation."""

from typing import Literal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class ReadinessResponse(BaseModel):
    """Stable response returned by the local readiness endpoint."""

    status: Literal["ready"] = "ready"
    service: Literal["api"] = "api"


app = FastAPI(
    title="Generador de contenido API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=[],
)


@app.get("/readiness", response_model=ReadinessResponse)
def readiness() -> ReadinessResponse:
    """Report local API readiness without contacting external providers."""

    return ReadinessResponse()
