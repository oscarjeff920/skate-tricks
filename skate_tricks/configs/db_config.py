import pydantic.error_wrappers
from psycopg2.extras import DictCursor
from pydantic import BaseSettings, PostgresDsn, validator, typing
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DbSettings(BaseSettings):
    DATABASE_USER: str = "postgres"
    DATABASE_PASS: str = "postgres"
    DATABASE_HOST: str = "127.0.0.1"
    DATABASE_PORT: str = "5432"
    DATABASE_NAME: str = "skate_tricks_db_mock"
    DATABASE_DSN: typing.Optional[PostgresDsn] = None

    @validator("DATABASE_DSN")
    def create_db_dsn(
        cls, v: typing.Optional[str], values: typing.Dict[str, typing.Any]
    ) -> str:
        if v is None:
            try:
                return str(
                    PostgresDsn.build(
                        scheme="postgresql+psycopg2",
                        user=values.get("DATABASE_USER", ""),
                        password=values.get("DATABASE_PASS", ""),
                        host=values.get("DATABASE_HOST", ""),
                        port=values.get("DATABASE_PORT", ""),
                        path="/{}".format(values.get("DATABASE_NAME", "")),
                    )
                )
            except pydantic.error_wrappers.ValidationError as pyvaler:
                print(
                    """Validation Error:\nMissing at least one of the following required fields:
                    \nDATABASE_HOST
                    \nDATABASE_PORT
                    \nDATABASE_NAME."""
                )
                raise pyvaler

        else:
            return v


def get_db_settings() -> DbSettings:
    return DbSettings()


def get_db_session(db_settings: DbSettings = Depends(get_db_settings)) -> DictCursor:
    engine = create_engine(db_settings.DATABASE_DSN)
    db = sessionmaker(autoflush=False, autocommit=False, bind=engine)()
    try:
        yield db
    finally:
        db.close()
