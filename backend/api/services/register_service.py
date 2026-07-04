from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from infrastructure.mysql import user_repository
from api.schemas.register_info import RegisterInfo

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def register(db: Session, register_info: RegisterInfo) -> None:
    if user_repository.exists_by_username(db, register_info.username):
        raise HTTPException(status_code=400, detail="このユーザー名はすでに使われています")
    hashed = pwd_context.hash(register_info.password)
    user_repository.create_user(db, register_info.username, hashed)
