import json
import os
from datetime import datetime
from unittest import TestCase

from requests import Session

from src.controllers.suppliers.csn.login import CsnLoginContr
from src.models.basemodels.my_base_model import MyBaseModel
from src.models.suppliers.cycleservicenordic.order import CycleServiceNordicOrder
from src.models.suppliers.cycleservicenordic.order_row import CycleServiceNordicOrderRow


class CycleServiceNordicOrderTests(TestCase):
    @staticmethod
    def test_get_order_from_api():
        """Requires internet"""
        order = CycleServiceNordicOrder(
            session=CsnLoginContr().login(), reference=479978
        )
        order.populate_order_from_api()
        assert order.reference == 479978
        assert (
            order.order_date.date()
            == datetime(
                2024, 6, 17, 0, 0, tzinfo=MyBaseModel().stockholm_timezone
            ).date()
        )
        assert order.rows != []
        assert order.number_of_rows == 7
        row1: CycleServiceNordicOrderRow = order.rows[0]
        assert row1.quantity == 1
        assert row1.entity.cost_price == 492.42
        assert row1.entity.sku == "943031"

    @staticmethod
    def test__extract_data__():
        # Define the path to the JSON file
        file_path = (
            "/home/dpriskorn/src/python/dolibarr_python_api/test_data/csn/order.json"
        )

        # Check if the file exists
        assert os.path.exists(file_path), f"File {file_path} does not exist"

        # Open and read the JSON file
        with open(file_path) as file:
            data = json.load(file)
        if data is None:
            raise ValueError()
        order = CycleServiceNordicOrder(session=Session(), reference=0, data=data)
        order.__extract_data__()
        # We don't assert the reference because we don't extract that in this method
        # assert order.reference == 479978
        assert (
            order.order_date.date()
            == datetime(
                2024, 6, 17, 0, 0, tzinfo=MyBaseModel().stockholm_timezone
            ).date()
        )
        assert order.rows != []
        assert order.number_of_rows == 7
        row1: CycleServiceNordicOrderRow = order.rows[0]
        assert row1.quantity == 1
        assert row1.entity.cost_price == 492.42
        assert row1.entity.sku == "943031"
        # pprint(row1.entity.model_dump())
        # assert row1.entity.label == "freight"
