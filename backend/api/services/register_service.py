from api.schemas.register_info import RegisterInfo
from api.validators.username_validator import UsernameValidator
from infrastructure.mysql.insert_user import insert_user
from infrastructure.security.password_hasher import hash_password
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def register(db: Session, register_info: RegisterInfo) -> None:
    UsernameValidator(db, register_info.username).validate()
    hashed = hash_password(register_info.password)
    try:
        insert_user(db, register_info.username, hashed)
    except IntegrityError:
        # UsernameValidatorのチェックとinsertの間に同名ユーザーの登録が
        # 割り込んだ場合、ここでunique制約違反として検出される
        raise ValueError("このユーザー名はすでに使われています")
