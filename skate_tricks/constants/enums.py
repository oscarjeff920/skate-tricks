from enum import Enum


class FlipType(Enum):
    ollie = "ollie"
    kickflip = "kickflip"
    heelflip = "heelflip"


class RotationDirection(Enum):
    bs = "bs"
    fs = "fs"


class SpinDegrees(Enum):
    d180 = "180"
    d360 = "360"
    d540 = "540"
    d720 = "720"
