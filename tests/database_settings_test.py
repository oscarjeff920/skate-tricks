import os

import pydantic.error_wrappers
import pytest

from skate_tricks.configs.db_config import get_db_settings

DATABASE_DSN = "postgresql+psycopg2://postgres:postgres@10.0.0.2:5000/skate_tricks_db"


def test_database_settings_dsn_builder() -> None:
    os.environ["DATABASE_USER"] = "postgres"
    os.environ["DATABASE_PASS"] = "postgres"
    os.environ["DATABASE_HOST"] = "10.0.0.2"
    os.environ["DATABASE_PORT"] = "5000"
    os.environ["DATABASE_NAME"] = "skate_tricks_db"
    assert get_db_settings().DATABASE_DSN == DATABASE_DSN


def test_database_settings_validation_missing_required_variables() -> None:
    with pytest.raises(pydantic.error_wrappers.ValidationError):
        get_db_settings().DATABASE_DSN
