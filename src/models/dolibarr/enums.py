from enum import Enum


class Currency(Enum):
    SEK = "SEK"
    EUR = "EUR"
    GBP = "GBP"
    USD = "USD"


class DolibarrEndpoint(Enum):
    CATEGORIES = "categories"
    FACTORY = "factory"
    INVOICES = "invoices"
    CUSTOMER_ORDER = "orders"
    PRODUCTS = "products"
    SHIPMENTS = "shipments"
    SUPPLIER_ORDER = "supplierorders"
    SUPPLIER_INVOICE = "supplierinvoices"
    THIRDPARTIES = "thirdparties"
    DOCUMENTS = "documents"


class DolibarrEndpointAction(Enum):
    PAYMENTS = "payments"
    PURCHASE_PRICES = "purchase_prices"
    SET_TO_DRAFT = "settodraft"
    VALIDATE = "validate"


class DolibarrTable(Enum):
    ORDER = "commande"
    PRODUCT = "product"
    THIRDPARTY = "societe"
    SUPPLIER_INVOICE = "invoice_supplier"
    SUPPLIER_ORDER = "commande_fournisseur"


class Expired(Enum):
    """These should really be integers or booleans, but they are not"""

    TRUE = "1"
    FALSE = "0"


class OrderStatus(Enum):
    # See details at
    # https://github.com/Dolibarr/dolibarr/blob/
    # d1c6a9899cdff15c65f7a1ba0ab1a19679b0ffdc/htdocs/fourn/class/fournisseur.commande.class.php#L102
    DRAFT = (0,)
    VALIDATED = (1,)
    MADE = 2
    AWAITING_RECEPTION = (3,)
    PARTIALLY_RECEIVED = (4,)
    FULLY_RECEIVED_AND_INVOICED = 5


class Status(Enum):
    """These should really be integers or booleans, but they are not"""

    DISABLED = "0"
    ENABLED = "1"


class StockType(Enum):
    """These should really be integers or booleans, but they are not"""

    STOCKED = "0"
    SERVICE = "1"


class PriceBaseType(Enum):
    NET_PRICE = "HT"
    GROSS_PRICE = "TTC"


class DolibarrColumn(Enum):
    REF_SUPPLIER = "ref_supplier"
    REF_CLIENT = "ref_client"
