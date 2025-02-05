from enum import Enum, auto


class EntityType(Enum):
    PRODUCT = auto()
    SERVICE = auto()


class ProductCategory(Enum):
    BIKE = 0
    SEWING = 1
