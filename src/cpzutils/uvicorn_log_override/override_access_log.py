import logging
import logging.config
from pathlib import Path


def main():
    """
    覆寫 uvicorn 的 access log 設定

    使其加上時間標誌的同時輸出到終端和每日輪轉的日誌文件中。

    使用範例:
    ```python
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

    ```
    """
    Path("log").mkdir(parents=True, exist_ok=True)  # 確保 log 目錄存在
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "access": {
                    "()": "uvicorn.logging.AccessFormatter",
                    "use_colors": False,  # 關閉顏色以避免日誌文件中出現亂碼
                    "fmt": '%(asctime)s - %(client_addr)s - "%(request_line)s" %(status_code)s',
                },
            },
            "handlers": {
                "access_stream": {
                    "formatter": "access",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                },
                "access_file": {
                    "formatter": "access",
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "filename": "log/uvicorn.access.log",
                    "when": "midnight",  # 每天午夜輪轉日誌文件
                    "interval": 1,
                    "backupCount": 0,  # 0 表示保留所有日誌文件，其餘數字表示保留的備份數量
                    "encoding": "utf-8",
                },
            },
            "loggers": {
                "uvicorn.access": {
                    "handlers": ["access_stream", "access_file"],
                    "level": "INFO",
                    "propagate": False,
                },
            },
        }
    )
