from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from cpzutils import uvicorn_log_override
from cpzutils.spa_support import SPASupport


@asynccontextmanager
async def lifespan(app: FastAPI):
    uvicorn_log_override.override_access_log()
    yield


app = FastAPI(
    default_response_class=ORJSONResponse,  # orjson 比 python 原生 json 更高效
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
