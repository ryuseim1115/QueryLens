from config import SESSION_COOKIE_NAME
from fastapi import APIRouter, Depends, Request, Response
from infrastructure.mysql.user_db import get_session
from sqlalchemy.orm import Session

from api.services.auth import session_service

router = APIRouter()


@router.post("/logout", status_code=204)
def logout_user(
    *, request: Request, response: Response, db: Session = Depends(get_session)
):
    token = request.cookies.get(SESSION_COOKIE_NAME)
    # サーバー側(sessionsテーブル)のトークンを失効させる。既にトークンが
    # 無効/期限切れの状態から呼ばれても正常終了させたいため、ログイン必須にはしない
    session_service.revoke_session(db, token)
    response.delete_cookie(SESSION_COOKIE_NAME)
