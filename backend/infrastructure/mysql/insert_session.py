from datetime import datetime

from sqlalchemy.orm import Session

from infrastructure.mysql.models import UserSession


def insert_session(db: Session, user_id: int, token: str, expires_at: datetime) -> None:
    db.add(UserSession(token=token, user_id=user_id, expires_at=expires_at))
    db.commit()
