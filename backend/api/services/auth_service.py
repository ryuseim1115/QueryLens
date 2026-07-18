from api.schemas.auth_info import AuthInfo
from fastapi import HTTPException
from infrastructure.mysql.find_user_by_username import find_user_by_username
from infrastructure.security.password_hasher import verify_password
from sqlalchemy.orm import Session


def authenticate(db: Session, auth_info: AuthInfo) -> int:
    user = find_user_by_username(db, auth_info.username)
    if user is None or not verify_password(
        plain_password=auth_info.password, hashed_password=user.hashed_password
    ):
        raise HTTPException(
            status_code=401, detail="ユーザー名またはパスワードが正しくありません"
        )
    return user.id
