from sqlalchemy.orm import Session

from infrastructure.mysql.models import UserSession


def delete_session_by_token(db: Session, token: str) -> None:
    db.query(UserSession).filter(UserSession.token == token).delete()
    db.commit()
