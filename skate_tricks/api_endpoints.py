from fastapi import FastAPI, Depends
from pydantic import typing
from sqlalchemy.orm import Session

from skate_tricks.configs.db_config import get_db_session
from skate_tricks.schemas import pydantic_schemas as json_schemas
from skate_tricks.schemas import postgres_models as models
from skate_tricks import database_operations as db_op

app = FastAPI()


@app.get("/")
async def home() -> typing.Dict:
    return {"Home": "A Skateboarding tricks database"}


@app.get("/trick-book/all/", response_model=typing.List[json_schemas.SkateTricks])
async def get_all_tricks(
    db: Session = Depends(get_db_session),
) -> typing.List[models.SkateTricks]:
    trick_book = db_op.get_all_tricks(db=db)
    return trick_book


@app.post("/trick-book/", response_model=json_schemas.SkateTricksBase)
async def post_new_trick(
    trick: json_schemas.SkateTricksBase, db: Session = Depends(get_db_session)
) -> models.SkateTricks:
    new_trick = db_op.post_new_trick(trick=trick, db=db)
    return new_trick
