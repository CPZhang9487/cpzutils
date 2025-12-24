from contextlib import asynccontextmanager

from fastapi import FastAPI

from cpzutils import uvicorn_log_override


@asynccontextmanager
async def lifespan(app: FastAPI):
    uvicorn_log_override.override_access_log()
    yield


app = FastAPI(
    lifespan=lifespan,
)
