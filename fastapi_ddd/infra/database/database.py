from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from fastapi_ddd.common.config.infra_config import infra_settings
from fastapi_ddd.common.exception.custom_exceptions import DatabaseException
from fastapi_ddd.domain.entity import Base

SQLALCHEMY_DATABASE_URL = infra_settings.DB.URL


class Database:
    def __init__(self, database_url: str = SQLALCHEMY_DATABASE_URL) -> None:
        self._engine = create_engine(database_url, echo=True)
        self._session_maker = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

    def create_database(self) -> None:
        Base.metadata.create_all(self._engine)

    @contextmanager
    def session_factory(self):
        session: Session = self._session_maker()
        try:
            yield session
        except Exception as exc:
            session.rollback()
            raise DatabaseException("A database exception occurred.", exc) from exc
        finally:
            session.commit()
            session.close()
