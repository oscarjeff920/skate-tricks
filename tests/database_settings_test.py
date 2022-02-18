import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import pydantic.error_wrappers
import pytest

from skate_tricks.configs.db_config import get_db_settings, get_db_session

DATABASE_DSN = (
    "postgresql+psycopg2://postgres:postgres@127.0.0.1:5000/skate_tricks_db_mock"
)


def test_database_settings_dsn_builder() -> None:
    os.environ["DATABASE_USER"] = "postgres"
    os.environ["DATABASE_PASS"] = "postgres"
    os.environ["DATABASE_HOST"] = "127.0.0.1"
    os.environ["DATABASE_PORT"] = "5432"
    os.environ["DATABASE_NAME"] = "skate_tricks_db_mock"
    assert get_db_settings().DATABASE_DSN == DATABASE_DSN


def test_database_settings_validation_missing_required_variables() -> None:
    with pytest.raises(pydantic.error_wrappers.ValidationError):
        return get_db_settings().DATABASE_DSN


def test_database_connection() -> None:
    engine = create_engine(DATABASE_DSN)
    db = sessionmaker(bind=engine)()
    try:
        assert isinstance(db, Session)
    finally:
        db.close()
