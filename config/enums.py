from enum import Enum


class Database(Enum):
    PRODUCTION = "dolibarr"
    TESTING = "dolidev"


class AccountId(Enum):
    """See http://dolibarr.localhost/compta/bank/list.php?mainmenu=bank&leftmenu= and hover to get the id="""

    SEB = 2
    # UPWORK = 6
    OWNERS_INSERT = 54


class PaymentSource(Enum):
    """See http://dolibarr.localhost/admin/dict.php -> Betalningslägen"""

    # TODO where are these found?
    VIRTUAL_TRANSFER = 2
    OWNERS_INSERT = 3


class DatabaseUser(Enum):
    DOLIBARR = "dolibarr"
    # TESTING = "dolibarr"


class DolibarrBaseUrl(Enum):
    PRODUCTION = "http://162.19.226.24/"
    TESTING = "http://162.19.226.24:8000/"


class FreightProductId(Enum):
    MESSINGSCHLAGER = 1376
