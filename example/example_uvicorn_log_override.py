"""
運行此程式的方式:
    1. uv run example/example_uvicorn_log_override.py
    2. uv run uvicorn example.example_uvicorn_log_override:app
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from cpzutils import uvicorn_log_override


@asynccontextmanager
async def lifespan(app: FastAPI):
    uvicorn_log_override.override_access_log()
    yield


app = FastAPI(
    lifespan=lifespan,
)


if __name__ == "__main__":
    uvicorn.run(app)
