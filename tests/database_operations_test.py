import os
import typing

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from skate_tricks.configs.db_config import get_db_settings, create_db, get_db_session
from skate_tricks.database_operations import get_all_tricks
from skate_tricks.schemas import postgres_models as models

os.environ["DATABASE_HOST"] = "127.0.0.1"
os.environ["DATABASE_PORT"] = "5432"
os.environ["DATABASE_NAME"] = "skate_tricks_db_mock"

create_db()


def session_test(func):  # type: ignore # TODO: work out type
    def pass_conn():  # type: ignore # TODO: work out type
        engine = create_engine(get_db_settings().DATABASE_DSN)
        db = sessionmaker(autoflush=False, autocommit=False, bind=engine)()
        try:
            output = func(db)
        finally:
            db.close()
        return output

    return pass_conn


def test_database_empty() -> None:
    @session_test
    def query_games(*args) -> typing.List:  # type: ignore # TODO: work out type
        db = args[0]
        tricks = get_all_tricks(db)
        return tricks

    db_tricks = query_games()
    assert db_tricks == []


def post_to_database() -> None:
    @session_test
    def post_trick(*args) -> models.SkateTricks:  # type: ignore # TODO: work out type
        pass


def test_database_empty2() -> None:
    engine = create_engine(url=get_db_settings().DATABASE_DSN)
    db = sessionmaker(bind=engine)()
    try:
        skate_tricks = get_all_tricks(db=db)
        assert skate_tricks == []
    finally:
        db.close()
