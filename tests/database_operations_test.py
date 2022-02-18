import os

from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database

from skate_tricks.configs.db_config import get_db_settings, get_db_session
from skate_tricks.schemas import postgres_models as models
