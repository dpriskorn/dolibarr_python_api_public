import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import config
from src.models.basemodels.my_base_model import MyBaseModel
from src.models.dolibarr.enums import (
    DolibarrEndpoint,
    OrderStatus,
)
from src.models.vat_rate import VatRate

logger = logging.getLogger(__name__)


class DolibarrSupplierOrder(MyBaseModel):
    """This models a supplier order in Dolibarrs datamodel

    Use of this is to pass in a supplier_order
    and then usually using the public method create_order_with_lines_and_correct_amounts()
    to create the order with all the lines.
    """

    array_options: Any = None  # does the API always output this?
    approved_and_made: Optional[bool] = None
    currency_rate: Optional[float] = None  # multicurrency_tx in Dolibarr
    delivery_date: datetime | str | None = None
    id: Optional[int] = None
    invoiced: Optional[bool] = None
    lines: List[Any] = []  # typing: DolibarrSupplierOrderLine
    order_date: datetime | None = None
    ref: Optional[str] = ""
    status: OrderStatus | str = None
    supplier_order: Any = (
        None  # "SupplierOrder" # we dont type this because of pydantic errors
    )
    total_ht: Optional[float] = None
    total_ttc: Optional[float] = None
    total_tva: Optional[float] = None
    validated: Optional[bool] = None
    vat_rate: Optional[VatRate] = None  # This is the purchase VAT rate
    linkedObjectsIds: Union[Dict[str, Dict[str, str]] | List[Any]] = []

    class Config:  # dead: disable
        arbitrary_types_allowed = True
        # todo support all fields
        # extra = "forbid"

    @property
    def delivery_url(self):
        return f"{self._base_url}fourn/commande/dispatch.php?id={self.id}"

    @property
    def external_ref(self):
        """This is the ref for the order that we get from the supplier"""
        return self.ref

    @property
    def url(self):
        return f"{self._base_url}fourn/commande/" + f"card.php?id={self.id}"

    def __fetch_from_dolibarr__(self):
        """Fetches an order by id or external_ref and dolibarr supplier"""
        if self.id:
            raise NotImplementedError("fetch by id not implemented yet")
        elif self.ref is not None and self.supplier_order.dolibarr_supplier:
            raise Exception("fetch by supplier and external_ref not implemented yet")
        else:
            raise Exception("this should never be reached")

    def __get_dolibarr_supplier__(self):
        if not self.supplier_order.dolibarr_supplier:
            self.supplier_order.__get_dolibarr_supplier__()

    def __already_imported__(self) -> bool:
        """Use codename and ref to check"""
        logger.debug("__already_imported__: running")
        result = self.api.get_id_by_external_ref(
            codename=self.supplier_order.codename,
            external_ref=str(self.supplier_order.reference),
            endpoint=DolibarrEndpoint.SUPPLIER_ORDER,
        )
        if result:
            self.id = int(result)
            print(f"This order has already been imported, see {self.url}")
            return True
        else:
            logger.debug("supplier order not found in dolibarr")
            return False

    @property
    def supplier_url(self) -> str:
        """Extrafield method"""
        if self.array_options and self.array_options.get("options_supplier_url"):
            return self.array_options.get("options_supplier_url")

    @supplier_url.setter
    def supplier_url(self, value):
        """Extrafield method"""
        if not self.array_options:
            self.array_options = {}
        self.array_options["options_supplier_url"] = value

    def get_by_id(self) -> Any:
        """This does not update the current product,
        but instead returns a new instance"""
        if not self.id:
            raise ValueError("self.id was None")

        r = self.api.get_supplier_order_by_id(object_id=self.id)
        if r.status_code == 200:
            data = r.json()
            if config.debug_responses:
                print(data)
            if isinstance(data, list):
                logger.debug("got list from Dolibarr")
                # we choose the first object
                data = data[0]
            else:
                logger.debug("got dict from Dolibarr")
            dolibarr_supplier_order = DolibarrSupplierOrder(**data)
            dolibarr_supplier_order.api = self.api
            return dolibarr_supplier_order
        else:
            raise ValueError(f"Got {r.status_code} from Dolibarr")

    @property
    def has_linked_invoice(self) -> bool:
        if (
            self.linkedObjectsIds is not None
            and isinstance(self.linkedObjectsIds, dict)
            and str(self.linkedObjectsIds.get("invoice_supplier", ""))
        ):
            return True
        return False
