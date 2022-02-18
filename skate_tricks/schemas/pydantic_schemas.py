from pydantic import BaseModel
from pydantic.typing import Optional, List

from skate_tricks.constants.enums import RotationDirection, FlipType, SpinDegrees


class SkateTricksBase(BaseModel):
    name: str
    fundamental: bool
    flip: FlipType
    board_rotation: Optional[RotationDirection] = None
    board_spin: Optional[SpinDegrees] = None
    body_rotation: Optional[RotationDirection] = None
    body_spin: Optional[SpinDegrees] = None


class SkateTricksCreate(SkateTricksBase):
    fundamental_tricks: Optional[List[str]] = None


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
