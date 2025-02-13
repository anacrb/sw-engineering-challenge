from typing import Generator

from sqlalchemy.orm import Session

from persistence.postgres_config import SessionLocal


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
