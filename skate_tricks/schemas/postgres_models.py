from sqlalchemy import Column, Integer, Boolean, Enum, Text, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from skate_tricks.constants.enums import FlipType, RotationDirection, SpinDegrees


Base = declarative_base()

# Associative Tables
variation_tricks = Table(
    "combo_tricks",
    Base.metadata,
    Column(
        "trick_id",
        Integer,
        ForeignKey("skate_tricks.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "fundamental_trick_id",
        Integer,
        ForeignKey("skate_tricks.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    ),
)


# Tables
class SkateTricks(Base):  # type: ignore
    __tablename__ = "skate_tricks"

    id = Column(Integer, primary_key=True)
    name = Column(Text, index=True, unique=True, nullable=False)
    fundamental = Column(Boolean, index=True, nullable=False)
    flip = Column(Enum(FlipType), nullable=False)
    board_rotation = Column(Enum(RotationDirection), nullable=True)
    board_spin = Column(Enum(SpinDegrees), nullable=True)
    body_rotation = Column(Enum(RotationDirection), nullable=True)
    body_spin = Column(Enum(SpinDegrees), nullable=True)

    # Relationships
    combo_of_fundamental = relationship(
        "SkateTricks", secondary=variation_tricks, back_populates="combo_of_fundamental"
    )
