from enum import Enum, auto


class CollisionType(Enum):
    DEBRIS = auto()
    BULLET = auto()
    KILL_ZONE = auto()