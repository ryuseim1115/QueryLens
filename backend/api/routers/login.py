import os

from config import TEMPLATES_DIR
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/login")
def login():
    return FileResponse(os.path.join(TEMPLATES_DIR, "html", "login.html"))
