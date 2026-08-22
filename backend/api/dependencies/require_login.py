from config import SESSION_COOKIE_NAME
from fastapi import Depends, HTTPException, Request
from infrastructure.mysql.user_db import get_session
from sqlalchemy.orm import Session

from api.services.auth.session_service import resolve_user_id


class NotLoggedInError(Exception):
    pass


def _get_user_id_or_raise(request: Request, db: Session, error: Exception) -> int:
    token = request.cookies.get(SESSION_COOKIE_NAME)
    user_id = resolve_user_id(db, token)
    if user_id is None:
        raise error
    return user_id


# JSのfetch()から呼ばれるAPI用。fetch()はリダイレクトを自動追跡してしまうため、
# ここでリダイレクトを返すとJS側が401を検知できず壊れる。必ず401を返すこと。
def require_login_api(request: Request, db: Session = Depends(get_session)) -> int:
    return _get_user_id_or_raise(
        request, db, HTTPException(status_code=401, detail="ログインが必要です")
    )


# ブラウザが直接開くページ用。401(生のJSON)をそのまま返すと画面に表示されて
# しまうため、NotLoggedInErrorを投げてmain.pyの例外ハンドラーで/loginへ
# リダイレクトさせる。
def require_login_page(request: Request, db: Session = Depends(get_session)) -> int:
    return _get_user_id_or_raise(request, db, NotLoggedInError())
