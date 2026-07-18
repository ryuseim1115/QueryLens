import os

from config import TEMPLATES_DIR
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from api.dependencies.require_login import require_login_page

router = APIRouter()


@router.get("/result-view")
def result_view(user_id: int = Depends(require_login_page)):
    return FileResponse(os.path.join(TEMPLATES_DIR, "html", "result-view.html"))
