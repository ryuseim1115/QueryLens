from sqlalchemy.orm import Session

from infrastructure.mysql.models import User


def find_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()
