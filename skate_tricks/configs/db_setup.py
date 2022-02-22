import os

from alembic import command
from alembic.config import Config

from skate_tricks.configs.db_config import create_db

os.environ["DATABASE_HOST"] = "127.0.0.1"
os.environ["DATABASE_PORT"] = "5432"
os.environ["DATABASE_NAME"] = "skate_tricks_db"


def upgrade_to_head() -> None:
    command.upgrade(Config(), "head")


if __name__ == "__main__":
    create_db()
