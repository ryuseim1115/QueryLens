import os

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from infrastructure.mysql.user_db import get_db
from api.schemas.register_info import RegisterInfo
from api.services import register_service
from config import TEMPLATES_DIR

router = APIRouter()


@router.get("/register")
def register():
    return FileResponse(os.path.join(TEMPLATES_DIR, "html", "register.html"))


@router.post("/register")
def register_user(*, db: Session = Depends(get_db), register_info: RegisterInfo):
    register_service.register(db, register_info)
