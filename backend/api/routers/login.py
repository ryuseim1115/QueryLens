import os

from config import SESSION_COOKIE_NAME, SESSION_MAX_AGE_SECONDS, TEMPLATES_DIR
from fastapi import APIRouter, Depends, Response
from fastapi.responses import FileResponse
from infrastructure.mysql.user_db import get_session
from sqlalchemy.orm import Session

from api.schemas.auth_info import AuthInfo
from api.services.auth import auth_service, session_service

router = APIRouter()


@router.get("/login")
def login():
    return FileResponse(os.path.join(TEMPLATES_DIR, "html", "login.html"))


@router.post("/login")
def login_user(
    *,
    response: Response,
    db: Session = Depends(get_session),
    auth_info: AuthInfo,
):
    # 認証(user_idの算出)は業務ロジックなのでサービス層に委譲する
    user_id = auth_service.authenticate(db, auth_info)
    # セッションの発行(サーバー側=sessionsテーブルへのトークン永続化)も
    # 業務ロジックなのでサービス層に委譲する
    token = session_service.create_session(db, user_id)
    # Cookieへの書き込みはHTTP層(クッキー)の関心事なので、
    # サービス層にResponseを持ち込ませずルータ側で行う
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        max_age=SESSION_MAX_AGE_SECONDS,
        httponly=True,
        samesite="lax",
    )
    return {"message": "Authenticated"}
