"""
運行此程式的方式:
    1. uv run example/fastapi-template/main.py
    2. uv run uvicorn example.fastapi-template.app:app
    3. uv run fastapi run example/fastapi-template/app.py
"""

import uvicorn

from app import app


if __name__ == "__main__":
    uvicorn.run(app)
