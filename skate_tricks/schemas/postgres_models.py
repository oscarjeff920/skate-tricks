from sqlalchemy import Column, Integer, Boolean, Enum, Text, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base as base
from sqlalchemy.orm import relationship

from skate_tricks.constants.enums import FlipType, RotationDirection, SpinDegrees

# Associative Tables
combo_tricks = Table(
    "combo_tricks",
    base.metadata,
    Column(
        "trick_id",
        Integer,
        ForeignKey("skate_tricks.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "basic_trick_id",
        Integer,
        ForeignKey("skate_tricks.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    ),
)


# Tables
class SkateTricks(base):
    __tablename__ = "skate_tricks"

    id = Column(Integer, primary_key=True)
    name = Column(Text, index=True, unique=True, nullable=False)
    basic = Column(Boolean, index=True, nullable=False)
    flip = Column(Enum(FlipType), nullable=True)
    board_rotation = Column(Enum(RotationDirection), nullable=True)
    board_spin = Column(Enum(SpinDegrees), nullable=True)
    body_rotation = Column(Enum(RotationDirection), nullable=True)
    body_spin = Column(Enum(SpinDegrees), nullable=True)

    # Relationships
    basic_tricks_combo = relationship(
        "SkateTricks", secondary=combo_tricks, back_populates="basic_tricks_combo"
    )
