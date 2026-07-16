from api.schemas.register_info import RegisterInfo
from api.validators.username_validator import UsernameValidator
from infrastructure.mysql.insert_user import insert_user
from infrastructure.security.password_hasher import hash_password
from sqlalchemy.orm import Session


def register(db: Session, register_info: RegisterInfo) -> None:
    UsernameValidator(db, register_info.username).validate()
    hashed = hash_password(register_info.password)
    insert_user(db, register_info.username, hashed)
