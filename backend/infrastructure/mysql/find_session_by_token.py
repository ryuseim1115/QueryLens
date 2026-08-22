from sqlalchemy.orm import Session

from infrastructure.mysql.models import UserSession


def find_session_by_token(db: Session, token: str) -> UserSession | None:
    return db.query(UserSession).filter(UserSession.token == token).first()
