from sqlalchemy.orm import Session

from infrastructure.mysql.models import User


def exists_by_username(db: Session, username: str) -> bool:
    return db.query(User).filter(User.username == username).first() is not None


def create_user(db: Session, username: str, hashed_password: str) -> None:
    user = User(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
