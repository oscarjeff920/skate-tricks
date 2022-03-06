import os
import sys

from skate_tricks.configs.db_config import create_db
from alembic import command
from alembic.config import Config

alembic_cfg = Config()

# For some reason the alembic path is not automatically directed to the project root
# This needs to be edited as depending on where the functions are run, the path will or wont be
# directed to /migrations
# TODO: need to make path to root VV be relative
project_root = os.path.dirname(os.getcwd())
alembic_cfg.set_main_option("script_location", f"{project_root}/migrations")

os.environ["DATABASE_HOST"] = "127.0.0.1"
os.environ["DATABASE_PORT"] = "5432"
os.environ["DATABASE_NAME"] = "trick_db_mock"


def upgrade_to_head() -> None:
    command.upgrade(alembic_cfg, "head")


def wipe_db_data() -> None:
    command.downgrade(alembic_cfg, "base")
    upgrade_to_head()


def create_new_revision(desc: str) -> None:
    command.revision(alembic_cfg, desc, True)


if __name__ == "__main__":
    create_db()
    # create_new_revision("First Revision")
    wipe_db_data()
    # upgrade_to_head()
