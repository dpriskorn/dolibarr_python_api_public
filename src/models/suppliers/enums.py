from enum import Enum, auto


class SupplierBaseUrl(Enum):
    """The base url including the forward slash in the end"""

    BIKESTER = "https://www.bikester.se/"
    CYTECH = "https://www.cytech.se/"
    CYCLETECH = "https://en.cycletech.nl/"
    CYCLESERVICENORDIC = "https://www.cycleservicenordic.com/"
    BIKABLE = "https://bikable.se/"
    BILTEMA = "https://www.biltema.se/"
    HOJ24 = "https://shop.hoj24.se/"
    MESSINGSCHLAGER = "https://www.messingschlager.com/"
    SHIMANO = "https://b2b.shimano.com/"


class SupportedSupplier(Enum):
    """The values are used as a prefix on
    the ref in the database of products
    to avoid https://en.wikipedia.org/wiki/Name_collision
    between suppliers"""

    # ALIEXPRESS = "AE"
    # BACHMANN = "BM"
    # BIKESTER = "BI" # DISABLED because the test fails because of Google tag manager data not being found
    BILTEMA = "BT"  # disabled because parsing test failed
    CYTECH = "CY"  # SE
    # CYCLETECH = "CT" # EU
    # CYCLEGEAR = "CG" # supplier changed name
    BIKABLE = "CG"  # CG renamed everything to Bikable
    # CYCLEUROPE = "CE"
    CYCLESERVICENORDIC = "CSN"
    ECORIDE_PRO_NORDIC_GROUP = "ER"
    # ELECTROKIT = "EK"
    # JOFRAB = "JO" # supplier changed name
    HOJ24 = "JO"
    # JAGUARVERKEN = "JV" # supplier no longer exists
    JULA = "JU"
    KULLAGERSE = "KU"
    # NIVATEX = "NT"
    MESSINGSCHLAGER = "MS"  # EU
    SHIMANO = "SH"
    # SYMASKINSHOPEN = "SS"
    TRADERASALJARE = "TRS"
    # VARTEX = "VA"
    # WISH = "WIS"


class BadDataSuppliers(Enum):
    """These suppliers do not publish their order and/or
    invoice data in a way that can be automated"""

    # ALIEXPRESS = "AE"
    # BACHMANN = "BM"
    # CYCLEUROPE = "CE"
    CYCLESERVICENORDIC = "CSN"
    ECORIDE_PRO_NORDIC_GROUP = "ER"
    ELECTROKIT = "EK"
    JAGUARVERKEN = "JV"
    JULA = "JU"
    KULLAGERSE = "KU"
    # NIVATEX = "NT"
    MESSINGSCHLAGER = "MS"
    SHIMANO = "SH"
    SYMASKINSHOPEN = "SS"
    TRADERASALJARE = "TRS"
    VARTEX = "VA"
    WISH = "WIS"


# EUR_suppliers = [SupportedSupplier.MESSINGSCHLAGER, SupportedSupplier.CYCLETECH]
EUR_suppliers = [SupportedSupplier.MESSINGSCHLAGER]


class Unit(Enum):
    KG = auto()
