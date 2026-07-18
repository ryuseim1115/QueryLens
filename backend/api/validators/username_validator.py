from infrastructure.mysql.exist_by_username import exist_by_username
from sqlalchemy.orm import Session


class UsernameValidator:
    def __init__(self, db: Session, username: str):
        self.db = db
        self.username = username

    def validate(self) -> None:
        if exist_by_username(self.db, self.username):
            raise ValueError("このユーザー名はすでに使われています")
