import os

from config import TEMPLATES_DIR
from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, RedirectResponse

from api.dependencies.require_login import is_logged_in

router = APIRouter()


@router.get("/result")
def result(request: Request):
    if not is_logged_in(request):
        return RedirectResponse(url="/login")
    return FileResponse(os.path.join(TEMPLATES_DIR, "html", "result.html"))
