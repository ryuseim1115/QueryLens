from sqlalchemy.orm import Session

from infrastructure.mysql.models import User


def insert_user(db: Session, username: str, hashed_password: str) -> None:
    user = User(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
