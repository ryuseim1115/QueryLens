from fastapi import HTTPException, Request


def is_logged_in(request: Request) -> bool:
    return request.session.get("user_id") is not None


def require_login(request: Request) -> int:
    user_id = request.session.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="ログインが必要です")
    return user_id
