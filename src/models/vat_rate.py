from enum import Enum

# This class is by itself because it is used by both
# DolibarrProduct and ??


class VatRate(Enum):
    TWENTYFIVE = 25
    TWELVE = 12
    # SIX = 6  # no longer legal for my business to use
    ZERO = 0
