import logging
from pprint import pprint
from typing import Any, List

from src.models.supplier.orders import SupplierOrders
from src.models.suppliers.cycleservicenordic.order import CycleServiceNordicOrder

logger = logging.getLogger(__name__)


class CycleServiceNordicOrders(SupplierOrders):
    data: Any = None
    orders: List[CycleServiceNordicOrder] = []

    def __fetch__(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            # 'Accept-Encoding': 'gzip, deflate, br, zstd',
            "Referer": "https://www.cycleservicenordic.com/en/customer-area",
            "Content-Type": "application/json",
            "Origin": "https://www.cycleservicenordic.com",
            "DNT": "1",
            "Alt-Used": "www.cycleservicenordic.com",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Priority": "u=1",
            # Requests doesn't support trailers
            # 'TE': 'trailers',
        }

        json_data = {
            "limit": 24,
            "offset": 0,
            "keyword": "",
            "fromdate": None,
            "todate": None,
            "includeorderlines": True,
            "matchkeywordasphrase": True,
        }

        response = self.session.post(
            "https://www.cycleservicenordic.com/contextapi/b06086ad-b673-48a7-b1dc-1a5b700655aa/v1/order/archived",
            # cookies=cookies,
            headers=headers,
            json=json_data,
        )
        if response.status_code == 200:
            logger.info("Got orders from CSN")
            self.data = response.json()
            # pprint(self.data)

        # Note: json_data will not be serialized by requests
        # exactly as it was in the original request.
        # data = '{"limit":24,"offset":0,"keyword":"","fromdate":null,"todate":null,"includeorderlines":true,"matchkeywordasphrase":true}'
        # response = requests.post(
        #    'https://www.cycleservicenordic.com/contextapi/b06086ad-b673-48a7-b1dc-1a5b700655aa/v1/order/archived',
        #    cookies=cookies,
        #    headers=headers,
        #    data=data,
        # )

    def __parse__(self):
        """Parse list of orders and get the data for each one"""
        if self.data is None:
            raise ValueError("no data")
        print(f"Found {len(self.data["orders"])} archived orders from CSN")
        for order in self.data["orders"]:
            order = CycleServiceNordicOrder(
                session=self.session, reference=int(order["documentid"])
            )
            order.populate_order_from_api()
            if order.found:
                if order.order_date is None:
                    pprint(order.data)
                    raise ValueError("order_date was None")
                # noinspection PyTypeChecker
                self.orders.append(order)
            else:
                print("Ignoring order without details")
