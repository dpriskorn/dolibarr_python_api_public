import logging
from typing import Any, List, Optional

from bs4 import BeautifulSoup, Tag  # type: ignore
from requests import Session

import config
from src.helpers.enums import StripType
from src.models.supplier.order import SupplierOrder
from src.models.supplier.order_row import SupplierOrderRow
from src.models.suppliers.enums import SupplierBaseUrl, SupportedSupplier
from src.models.suppliers.shimano.order_row import ShimanoOrderRow
from src.models.suppliers.shimano.product import ShimanoProduct

logger = logging.getLogger(__name__)


class ShimanoOrder(SupplierOrder):
    """This correspond to the data Shimano exposes for orders"""

    base_url: SupplierBaseUrl = SupplierBaseUrl.SHIMANO
    codename: SupportedSupplier = SupportedSupplier.SHIMANO
    discount_percentage: float = 1.0
    dolibarr_supplier_order: Optional[Any] = None  # typing: DolibarrSupplierOrder
    form_id: str = ""
    free_freight: bool = False
    freight_price: float = 100.0
    freight_product_id: int = 1196
    insert_payment: bool = True
    order_history_table: Optional[Tag] = None
    order_numbers_found_on_invoice: List[str] = []
    round_up_on_order_total: bool = True
    rows: List[SupplierOrderRow] = []
    scraped: bool = False
    # already_imported_dir = f"{invoice_dir}/already_imported"
    session: Session = None
    credit_days: int = 10
    invoice_delay: int = 0

    def get_details(self):
        """Fetch and parse the details of the order"""
        logger.info(f"Fetching order details for new order {self.id}")
        if not self.session:
            raise ValueError("self.session was None")
        response = self.session.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, features="lxml")
            table: Tag = soup.select_one("div.order-list").select_one("ul")
            if not table:
                raise Exception(
                    f"Could not find product list for order {self.id}, see {self.url}."
                )
            if len(table) > 0:
                logger.info("Got order details")
                # logger.debug(table)
                self.__parse_order_details__(table)
                logger.info(self)
        else:
            raise ValueError(f"Got {response.status_code} from {self.codename}")

    def __parse_order_details__(self, table: Tag = None):
        """Parse the Shimano order details"""
        if not table:
            raise ValueError("table was None")
        # logger.debug(f"table:{table}")
        rows = table.select("li")
        # Remove the table header
        rows.pop(0)
        # Remove the freight line that is always last
        del rows[-1]
        logger.debug(f"order rows:{len(rows)}")
        # logger.debug(f"rows:{rows}")
        if len(rows) == 0:
            raise ValueError("row was 0, something is wrong")
        # order_rows = []
        for row in rows:
            # logger.debug(f"row:{row}")
            # raise Exception("debug exit")
            # get product_id
            link = row.select_one("a")
            # logger.debug(links)
            # logger.debug(len(links))
            product_id = link.get_text(strip=True)
            product_url = str(self.base_url.value) + link["href"]
            logger.debug(f"id:{product_id}, url:{product_url}")
            if not product_id or not product_url:
                raise ValueError("could not find link with product id")
            cost_price = float(
                self.price_cleanup(
                    price_stripping_type=StripType.KR_BEFORE,
                    price=row.select_one("div.ol-yourprice")
                    .select_one("a")
                    .get_text(strip=True),
                )
            )
            logger.debug(f"cost_price:{cost_price}")
            quantity = int(
                row.select_one("div.ol-quantity").select_one("a").get_text(strip=True)
            )
            logger.debug(f"quantity:{quantity}")
            # raise Exception("Format has changed, update parsing")
            product = ShimanoProduct(
                cost_price=cost_price,
                ref=product_id,
                url=product_url,
                session=self.session,
            )
            product.update_and_import_if_missing()
            if not product.ref:
                logger.warning(
                    "Not appending this product because no external_ref, "
                    "please fix the order manually"
                )
            else:
                if config.loglevel == logging.DEBUG:
                    print(product.model_dump())
                self.rows.append(ShimanoOrderRow(quantity=quantity, entity=product))
        logger.info("Order details:")
        for row in self.rows:
            logger.info(f"{row.entity.label}: {row.quantity} pcs")

    @property
    def url(self) -> str:
        return f"{self.base_url.value}/sv/login/order-history/order-detail.{self.reference}"
