import logging
from datetime import datetime
from unittest import TestCase

from pydantic import ValidationError

import config
from src.models.basemodels.my_base_model import MyBaseModel
from src.models.suppliers.shimano.login import ShimanoLogin
from src.models.suppliers.shimano.pdfplumber import Pdfplumber

logging.basicConfig(level=config.loglevel)


class TestPdfplumber(TestCase):
    session = ShimanoLogin().login_and_get_session()

    def test_parse_into_shimano_order_no_args(self):
        with self.assertRaises(ValidationError):
            Pdfplumber()  # type: ignore # mypy: ignore

    def test_parse_into_shimano_order_too_few_args(self):
        with self.assertRaises(ValidationError):
            Pdfplumber(invoice_id="123", session=self.session)  # type: ignore # mypy: ignore

    def test_parse_into_shimano_order_wrong_type(self):
        with self.assertRaises(ValidationError):
            Pdfplumber(invoice_id=123, session=self.session)  # type: ignore # mypy: ignore

    # Disabled because it takes 23s and the test below covers the same
    # def test_parse_into_shimano_order_good_args_2pages(self):
    #     parser = Pdfplumber(
    #         invoice_id="123",
    #         file_path=f"{config.file_root}test_data/test.pdf",
    #     )
    #     due_date, order = parser.parse_into_shimano_order()
    #     assert order.id == "123"
    #     assert len(order.rows) == 7
    #     assert sum(row.quantity for row in order.rows) == 13
    #     assert order.rows[0].product.sku == "PTHBH2"
    #     assert order.rows[1].product.sku == "ESLC30007DXL210LA3R"
    #     assert due_date == datetime(year=2021, month=12, day=3)
    #     assert order.order_date == datetime(year=2021, month=11, day=3)

    # def test_parse_into_shimano_order_good_args_2pages_rows_on_second_page_also(self):
    #     """Takes 43s to run :/"""
    #     # raises error because the product number Y0BN98020 is no longer in the API for some reason
    #     with self.assertRaises(ProductNotFoundError):
    #         parser = Pdfplumber(
    #             invoice_id="123",
    #             file_path=f"{config.file_root}test_data/test2.pdf",
    #             session=self.session,
    #         )
    #         due_date, order = parser.parse_into_shimano_order()
    #         assert order.id == "123"
    #         assert len(order.rows) == 13
    #         assert sum(row.quantity for row in order.rows) == 18
    #         assert order.rows[0].entity.sku == "PRTLB043"
    #         assert order.rows[-1].entity.sku == "ECSHG418130"
    #         assert due_date == datetime(year=2022, month=8, day=19).astimezone(
    #             tz=MyBaseModel().stockholm_timezone
    #         )
    #         assert order.order_date == datetime(year=2022, month=7, day=20).astimezone(
    #             tz=MyBaseModel().stockholm_timezone
    #         )

    def test_parse_into_shimano_order_good_args_1_page(self):
        parser = Pdfplumber(
            invoice_id="123",
            file_path=f"{config.file_root}test_data/test1.pdf",
            session=self.session,
        )
        due_date, order = parser.parse_into_shimano_order()
        assert order.reference == "123"
        assert len(order.rows) == 1
        assert sum(row.quantity for row in order.rows) == 2
        assert order.rows[0].entity.sku == "Y65P98040"
        assert due_date == datetime(year=2022, month=2, day=14).astimezone(
            tz=MyBaseModel().stockholm_timezone
        )
        assert order.order_date == datetime(year=2022, month=1, day=15).astimezone(
            tz=MyBaseModel().stockholm_timezone
        )

    def test_find_order_numbers_in_invoice_text(self):
        parser = Pdfplumber(
            invoice_id="123",
            file_path=f"{config.file_root}test_data/test.pdf",
            session=self.session,
        )
        order_numbers = parser.find_order_numbers_in_invoice_text()
        if len(order_numbers) != 2:
            self.fail()

    def test_find_freight_in_invoice_text(self):
        parser = Pdfplumber(
            invoice_id="123",
            file_path=f"{config.file_root}test_data/test.pdf",
            session=self.session,
        )
        if not parser.find_freight_in_invoice_text():
            self.fail()
