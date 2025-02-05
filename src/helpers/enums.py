from enum import Enum, auto


# noinspection PyArgumentList
class InputType(Enum):
    FLOAT = auto()
    INTEGER = auto()
    STRING = auto()


# noinspection PyArgumentList
class StripType(Enum):
    KR_BEFORE = auto()
    KR_AFTER = auto()
    COLON_DASH = auto()
    EUR_AFTER = auto()


# noinspection PyArgumentList
class FloatCleanType(Enum):
    AMERICAN = auto()
    SCANDINAVIAN = auto()
