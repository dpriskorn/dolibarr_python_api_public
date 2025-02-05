import logging
from datetime import datetime
from typing import Any, Dict, List

from src.models.exceptions import ScrapeError
from src.models.supplier.orders import SupplierOrders
from src.models.suppliers.hoj24.order import Hoj24Order
from src.models.suppliers.hoj24.order_row import Hoj24OrderRow
from src.models.suppliers.hoj24.product import Hoj24Product

logger = logging.getLogger(__name__)


class Hoj24Orders(SupplierOrders):
    orders: List[Hoj24Order] = []
    data: Any | None = None

    def get_and_parse_orders(self):
        self.__fetch__()
        self.__parse__()
        # Reverse order list so they get imported in ascending date order
        self.orders.reverse()

    def __fetch__(self):
        """Get list of orders"""
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            # 'Accept-Encoding': 'gzip, deflate, br, zstd',
            "maxAge": "300",
            "Origin": "https://shop.hoj24.se",
            "DNT": "1",
            "Connection": "keep-alive",
            "Referer": "https://shop.hoj24.se/",
            # 'Cookie': 'JSESSIONID=D4EFCB58814C939542817A5D08D9CD51',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
        }

        params = {
            "maxSize": "100",
        }

        response = self.session.get(
            "https://api.hoj24.se/json/orders/list/H725-765583",
            params=params,
            headers=headers,
        )
        if response.status_code == 200:
            logger.info("Got orders from Hoj24")
            self.data = response.json()
            # pprint(self.data)
        else:
            raise ScrapeError(
                f"Got {response.status_code} from Hoj24 when trying to scrape orders"
            )

    @staticmethod
    def freight_price(rows: Any) -> float:
        for row in rows:
            extra = row.get("extra", {})
            gung_sales_order_lines = extra.get("gungSalesOrderLines", {})
            if gung_sales_order_lines["description"] == "Fakturerade frakter Inrikes":
                return float(gung_sales_order_lines["netAmount"])
        raise ValueError("no freight price found for this order")

    def __parse__(self):
        if self.data is None:
            raise ValueError("self.data was None")
        for item in self.data:
            extra = item.get("extra", {})
            gung_sales_order = extra.get("gungSalesOrder", {})
            rows = self.parse_rows(item.get("rows", []))
            order = Hoj24Order(
                freight_price=self.freight_price(item.get("rows", [])),
                # reference=int(item["id"]), # what is this?
                order_date=datetime.strptime(
                    gung_sales_order["orderDate"], "%Y-%m-%d"
                ).astimezone(tz=self.stockholm_timezone)
                if gung_sales_order["orderDate"]
                else None,
                delivery_date=datetime.strptime(
                    gung_sales_order["shipmentDate"], "%Y-%m-%d"
                ).astimezone(tz=self.stockholm_timezone)
                if gung_sales_order["shipmentDate"]
                else None,
                reference=gung_sales_order["no"],
                # discount_percentage=gung_sales_order.get('discountAmount', 0.0),
                rows=rows,
                scraped=True,
            )
            self.orders.append(order)

    @staticmethod
    def parse_rows(rows_data: List[Dict[str, Any]]) -> List[Hoj24OrderRow]:
        rows = []
        for row_data in rows_data:
            extra = row_data.get("extra", {})
            gung_sales_order_lines = extra.get("gungSalesOrderLines", {})
            label = gung_sales_order_lines["description"]
            if label == "Fakturerade frakter Inrikes":
                logger.debug("Found and ignored freight line")
                continue
            id_ = row_data["productId"]
            product = Hoj24Product(
                sku=id_, cost_price=gung_sales_order_lines["unitPrice"], label=label
            )
            # We don't need to scrape them here
            # product.scrape_product()
            row = Hoj24OrderRow(
                entity=product,
                quantity=row_data["quantity"],
            )
            rows.append(row)
        return rows
