import os

from config import TEMPLATES_DIR
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/")
def landing():
    return FileResponse(os.path.join(TEMPLATES_DIR, "html", "landing.html"))
