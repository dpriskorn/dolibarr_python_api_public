import logging
from unittest import TestCase

import config
from src.views.marketplaces.sello.order_row import SelloOrderRowView

logging.basicConfig(level=config.loglevel)


class TestSelloOrderRowView(TestCase):
    def test_order_row(self):
        data = {
            "created_at": "2022-05-22T21:18:20.000Z",
            "id": 37977455,
            "identifier": None,
            "identifier_type": None,
            "image": "https://images.sello.io/products/eac952b45bb694c2574a992020acb061.jpg",
            "integration_id": 46162,
            "item_no": "542607821",
            "item_type": None,
            "market_reference": None,
            "price": 29,
            "product_id": 42950441,
            "purchase_price": 0,
            "quantity": 1,
            "quantity_returned": 0,
            "reference": "596",
            "status": "accepted",
            "status_reason": None,
            "stock_location": "",
            "submitter": None,
            "tariff": None,
            "tax": 25,
            "title": "Bromsvajer universal",
            "total_vat": 5.8,
            "total_weight": 0,
            "tradera_order_id": 114711767,
        }
        sor = SelloOrderRowView(**data)
        assert sor.price == 29
        # assert sor.determine_dolibarr_reference == 596
        assert sor.item_no == 542607821
