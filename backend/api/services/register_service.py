from api.schemas.register_info import RegisterInfo
from fastapi import HTTPException
from infrastructure.mysql.exist_by_username import exist_by_username
from infrastructure.mysql.insert_user import insert_user
from infrastructure.security.password_hasher import hash_password
from sqlalchemy.orm import Session


def register(db: Session, register_info: RegisterInfo) -> None:
    if exist_by_username(db, register_info.username):
        raise HTTPException(
            status_code=400, detail="このユーザー名はすでに使われています"
        )
    hashed = hash_password(register_info.password)
    insert_user(db, register_info.username, hashed)
