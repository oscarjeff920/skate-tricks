from alchemy_mock.mocking import UnifiedAlchemyMagicMock

from skate_tricks.database_operations import get_all_tricks
from skate_tricks.schemas import postgres_models as models

session = UnifiedAlchemyMagicMock()

session.add(models.SkateTricks(name="ollie", fundamental=True, flip="ollie"))
session.add(models.SkateTricks(name="kickflip", fundamental=True, flip="kickflip"))
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
session.add(models.SkateTricks(name="heelflip", fundamental=True, flip="heelflip"))
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


def test_get_all_tricks_order() -> None:
    pass
