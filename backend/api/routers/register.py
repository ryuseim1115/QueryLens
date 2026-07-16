import os

from config import TEMPLATES_DIR
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from infrastructure.mysql.user_db import get_session
from sqlalchemy.orm import Session

from api.schemas.register_info import RegisterInfo
from api.services import register_service

router = APIRouter()


@router.get("/register")
def register():
    return FileResponse(os.path.join(TEMPLATES_DIR, "html", "register.html"))


@router.post("/register")
def register_user(*, db: Session = Depends(get_session), register_info: RegisterInfo):
    try:
        register_service.register(db, register_info)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
