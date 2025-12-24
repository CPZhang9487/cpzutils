from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from cpzutils import uvicorn_log_override
from cpzutils.spa_support import SPASupport


@asynccontextmanager
async def lifespan(app: FastAPI):
    uvicorn_log_override.override_access_log()
    yield


app = FastAPI(
    lifespan=lifespan,
)


# exceptions


# middlewares


# routes


# services
app.mount(
    "/",
    SPASupport(
        directory=Path(__file__).parent / "static",
        routes=[
            r"test(/.*)?",  # 匹配 test、test/、test/abc 等
        ],
        page_404="404.html",
    ),
)
