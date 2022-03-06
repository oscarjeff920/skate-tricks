import fastapi
from sqlalchemy.orm import Session
from pydantic import typing
from skate_tricks.schemas import pydantic_schemas as json_schemas
from skate_tricks.schemas import postgres_models as models


def get_all_tricks(db: Session) -> typing.List[models.SkateTricks]:
    db_query = (
        db.query(models.SkateTricks)
        .order_by(models.SkateTricks.fundamental)
        .order_by(models.SkateTricks.flip)
        .order_by(models.SkateTricks.board_rotation)
        .order_by(models.SkateTricks.board_spin)
        .order_by(models.SkateTricks.body_rotation)
        .order_by(models.SkateTricks.body_spin)
        .all()
    )
    return db_query


def post_new_trick(
    db: Session, trick: json_schemas.SkateTricksCreate
) -> models.SkateTricks:
    db_new_trick = models.SkateTricks(
        name=trick.name,
        fundamental=trick.fundamental,
        flip=trick.flip,
        board_rotation=trick.board_rotation,
        board_spin=trick.board_spin,
        body_rotation=trick.body_rotation,
        body_spin=trick.body_spin,
    )
    db.add(db_new_trick)
    db.flush()
    if trick.fundamental_tricks is not None:
        for fundamental_trick in trick.fundamental_tricks:
            db_trick = (
                db.query(models.SkateTricks)
                .filter(models.SkateTricks.name == fundamental_trick)
                .filter(models.SkateTricks.fundamental)
                .one_or_none()
            )
            if db_trick is None:
                raise fastapi.HTTPException(
                    status_code=404,
                    detail=f"""The fundamental trick {fundamental_trick} is either not fundamental,
                           or doesn't exist in the database""",
                )
    db.commit()
    db.refresh(db_new_trick)
    return db_new_trick


def post_variation_trick_fundamentals(
    db: Session, trick_name: str, fundamental_trick_name: str
) -> json_schemas.TrickFundamentalsCreate:
    db_trick = (
        db.query(models.SkateTricks)
        .filter(models.SkateTricks.name == trick_name.lower())
        .one_or_none()
    )
    if db_trick is None:
        raise fastapi.HTTPException(
            status_code=404,
            detail=f"{trick_name} doesn't exist in the database, add trick first then try again.",
        )

    db_fundamental_trick = (
        db.query(models.SkateTricks)
        .filter(models.SkateTricks.name == fundamental_trick_name.lower())
        .filter(models.SkateTricks.fundamental is True)
        .one_or_none()
    )
    if db_fundamental_trick is None:
        raise fastapi.HTTPException(
            status_code=404,
            detail=f"""The fundamental trick {fundamental_trick_name} is either not fundamental,
            or doesn't exist in the database.""",
        )
    db_trick_fundamentals = json_schemas.TrickFundamentalsCreate(
        trick_name=trick_name.lower(),
        fundamental_trick_name=fundamental_trick_name.lower(),
    )
    db.add(db_trick_fundamentals)
    db.commit()
    db.refresh(db_trick_fundamentals)
    return db_trick_fundamentals
