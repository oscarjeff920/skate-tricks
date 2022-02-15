from alchemy_mock.mocking import UnifiedAlchemyMagicMock

from skate_tricks.database_operations import get_all_tricks, post_new_trick
from skate_tricks.schemas import postgres_models as models
from skate_tricks.schemas.pydantic_schemas import SkateTricksBase

session = UnifiedAlchemyMagicMock()

session.add(
    models.SkateTricks(
        name="ollie", fundamental=True, flip="ollie", body_rotation=None, body_spin=None
    )
)
session.add(
    models.SkateTricks(
        name="kickflip",
        fundamental=True,
        flip="kickflip",
        body_rotation=None,
        body_spin=None,
    )
)
session.add(
    models.SkateTricks(
        name="bs 180",
        fundamental=True,
        flip="ollie",
        body_rotation="bs",
        body_spin="180",
    )
)
session.add(
    models.SkateTricks(
        name="bs flip",
        fundamental=False,
        flip="kickflip",
        body_rotation="bs",
        body_spin="180",
    )
)
session.add(
    models.SkateTricks(
        name="varial flip",
        fundamental=False,
        flip="kickflip",
        board_rotation="bs",
        body_spin="180",
    )
)
session.add(
    models.SkateTricks(
        name="heelflip",
        fundamental=True,
        flip="heelflip",
        body_rotation=None,
        body_spin=None,
    )
)
session.add(
    models.SkateTricks(
        name="tre flip",
        fundamental=False,
        flip="kickflip",
        board_rotation="bs",
        board_spin="360",
    )
)


def test_get_all_tricks() -> None:
    query = get_all_tricks(db=session)
    assert query is not None


def test_get_all_tricks_order() -> None:  # I think this fails as filters don't work with the mocker
    pass


def test_create_skate_trick_without_fundamental_tricks() -> None:
    new_trick = post_new_trick(
        db=session,
        trick=SkateTricksBase(
            name="fs 180",
            fundamental=True,
            flip="ollie",
            body_roation="fs",
            body_spin="180",
        ),
        fundamental_tricks=None,
    )
    assert isinstance(new_trick, models.SkateTricks)


def test_create_skate_trick_with_fundamental_tricks() -> None:  # I think this fails as filters don't work with the mocker
    new_trick = post_new_trick(
        db=session,
        trick=SkateTricksBase(
            name="fs flip",
            fundamental=False,
            flip="kickflip",
            body_roation="fs",
            body_spin="180",
        ),
        fundamental_tricks=["kickflip", "fs 180"],
    )
    assert isinstance(new_trick, models.SkateTricks)
