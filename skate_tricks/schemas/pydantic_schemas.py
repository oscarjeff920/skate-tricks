from pydantic import BaseModel
from pydantic.typing import Optional

from skate_tricks.constants.enums import RotationDirection, FlipType, SpinDegrees


class SkateTricksBase(BaseModel):
    name: str
    basic: bool
    flip: FlipType
    board_rotation: Optional[RotationDirection]
    board_spin: Optional[SpinDegrees]
    body_rotation: Optional[RotationDirection]
    body_spin: Optional[SpinDegrees]


class SkateTricks(SkateTricksBase):
    id: int

    class Config:
        orm_mode = True


# Associative
class TrickFundamentalsCreate(BaseModel):
    trick_id: int
    fundamental_trick_id: int


class TrickFundamentals(BaseModel):
    trick_name: str
    fundamental_trick_name: str
