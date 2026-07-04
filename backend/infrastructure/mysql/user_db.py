from config import MYSQL_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

engine = create_engine(MYSQL_URL)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def get_session():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
