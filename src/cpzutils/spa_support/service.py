import re

from starlette.exceptions import HTTPException
from starlette.responses import Response
from starlette.staticfiles import PathLike, StaticFiles
from starlette.types import Scope


class SPASupport(StaticFiles):
    """
    支援單頁式應用(SPA) 的 StaticFiles

    - directory: 靜態檔案所在目錄
    - routes: 需要回傳 index.html 的路由清單 (正規表達式字串)，注意開頭不該有 /
    - page_404: 404 Not Found 頁面檔案
    """

    def __init__(
        self,
        *,
        directory: PathLike,
        routes: list[str] | None = None,
        page_404: str = "index.html",
    ):
        super().__init__(
            directory=directory,
            html=True,
        )
        self.routes = [re.compile(route) for route in routes or []]
        self.page_404 = page_404

    async def get_response(self, path: str, scope: Scope) -> Response:
        path = path.replace("\\", "/").lstrip("/")
        try:
            response = await super().get_response(path, scope)
            if (
                response.status_code == 404
            ):  # 當目錄中有 404.html 時不會跳至下方的 except，這邊手動呼叫
                raise HTTPException(status_code=404)
        except HTTPException as e:
            if e.status_code == 404:
                if any(route.fullmatch(path) for route in self.routes):
                    response = await super().get_response("index.html", scope)
                else:
                    response = await super().get_response(self.page_404, scope)
                    response.status_code = 404
            else:
                raise e

        return response
