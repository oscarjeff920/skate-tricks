import os
import typing

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from skate_tricks.configs.db_config import get_db_settings, create_db
from skate_tricks.configs.db_setup import wipe_db_data
from skate_tricks.database_operations import get_all_tricks, post_new_trick
from skate_tricks.schemas import postgres_models as models
from skate_tricks.schemas import pydantic_schemas as json_schemas

os.environ["DATABASE_HOST"] = "127.0.0.1"
os.environ["DATABASE_PORT"] = "5432"
os.environ["DATABASE_NAME"] = "tricks_db_mock"

if __name__ == "__main__":
    create_db()

# TODO: problem with alembic and dropping/recreating enums through upgrades and downgrades...


def pass_test_session(func):  # type: ignore # TODO: work out type
    def pass_conn():  # type: ignore # TODO: work out type
        engine = create_engine(get_db_settings().DATABASE_DSN)
        db = sessionmaker(autoflush=False, autocommit=False, bind=engine)()
        try:
            output = func(db=db)
        finally:
            db.close()
        return output

    return pass_conn


def test_database_empty() -> None:
    wipe_db_data()

    @pass_test_session
    def query_games(**kwargs) -> typing.List:  # type: ignore # TODO: work out type
        db = kwargs["db"]
        tricks = get_all_tricks(db)
        return tricks

    db_tricks = query_games()
    assert db_tricks == []


def test_post_to_database() -> None:
    @pass_test_session
    def post_trick(**kwargs):  # type: ignore # TODO: work out type
        db = kwargs["db"]
        wipe_db_data()
        trick = json_schemas.SkateTricksCreate(
            name="ollie", fundamental=True, flip="ollie"
        )
        db_trick = post_new_trick(db=db, trick=trick)

        query = (
            db.query(models.SkateTricks)
            .filter(models.SkateTricks.name == db_trick.name)
            .one_or_none()
        )
        return db_trick, query

    db_trick, db_query = post_trick()
    assert db_query != []
    assert db_query.name == db_trick.name


def test_get_all_tricks() -> None:
    @pass_test_session
    def query_tricks(**kwargs) -> typing.List[models.SkateTricks]:  # type: ignore # TODO: work out type
        db = kwargs["db"]
        tricks = get_all_tricks(db=db)
        return tricks

    db_tricks = query_tricks()
    assert db_tricks != []
