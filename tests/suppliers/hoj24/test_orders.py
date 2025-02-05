import json
import logging
from datetime import datetime
from typing import Any
from unittest import TestCase

from requests import Session

import config
from src.models.basemodels.my_base_model import MyBaseModel
from src.models.suppliers.hoj24 import Hoj24
from src.models.suppliers.hoj24.order_row import Hoj24OrderRow
from src.models.suppliers.hoj24.orders import Hoj24Orders

logging.basicConfig(level=config.loglevel)


class TestHoj24Orders(TestCase):
    data: Any | None = None

    def setUp(self):
        file_path = f"{config.file_root}test_data/hoj24/orders_data.json"

        try:
            with open(file_path) as file:
                self.data = json.load(file)
        except FileNotFoundError:
            print(f"The file at {file_path} was not found.")
        except json.JSONDecodeError:
            print("Failed to decode JSON from the file.")

    def test_get(self):
        hoj24 = Hoj24()
        hoj24.login()
        orders = Hoj24Orders(session=hoj24.session)
        orders.__fetch__()
        assert orders.data is not None

    def test_parse(self):
        tz = MyBaseModel().stockholm_timezone
        if self.data is None:
            raise ValueError()
        orders = Hoj24Orders(data=self.data, session=Session())
        orders.__parse__()
        assert len(orders.orders) == 2
        first_order = orders.orders[0]
        assert first_order.reference == 4655665
        assert first_order.freight_price == 119
        assert first_order.delivery_date.replace(tzinfo=tz) == datetime(
            2024, 5, 16, 0, 0, tzinfo=tz
        )
        assert first_order.order_date.replace(tzinfo=tz) == datetime(
            2024, 5, 16, 0, 0, tzinfo=tz
        )
        assert len(first_order.rows) == 6
        first_row: Hoj24OrderRow = first_order.rows[0]
        assert first_row.entity is not None
        assert first_row.entity.sku == "18-128-121"
        assert first_row.quantity == 1
