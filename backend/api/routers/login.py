import os

from config import TEMPLATES_DIR
from fastapi import APIRouter, Depends, Request
from fastapi.responses import FileResponse
from infrastructure.mysql.user_db import get_session
from sqlalchemy.orm import Session

from api.schemas.auth_info import AuthInfo
from api.services import auth_service

router = APIRouter()


@router.get("/login")
def login():
    return FileResponse(os.path.join(TEMPLATES_DIR, "html", "login.html"))


@router.post("/login")
def login_user(*, request: Request, db: Session = Depends(get_session), auth_info: AuthInfo):
    user_id = auth_service.authenticate(db, auth_info)
    request.session["user_id"] = user_id
    return {"message": "Authenticated"}
