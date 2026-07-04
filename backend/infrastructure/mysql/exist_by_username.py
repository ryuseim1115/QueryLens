from sqlalchemy import exists
from sqlalchemy.orm import Session

from infrastructure.mysql.models import User


def exist_by_username(db: Session, username: str) -> bool:
    return db.query(exists().where(User.username == username)).scalar()
