# from datetime import datetime
# from typing import List
# from unittest import TestCase
#
# import config
# from src.models.dolibarr.enums import Currency
# from src.models.supplier.order_row import SupplierOrderRow
# from src.models.suppliers.messingschlager.order import MessingschlagerOrder
#
#
# class MessingschlagerOrderTests(TestCase):
#     # DISABLED because it overlaps with the test below
#     # def test_parse_xlsx_invoice(self):
#     #     mo = MessingschlagerOrder(
#     #         file_path=f"{config.file_root}data/ms-test-invoice.xlsx"
#     #     )
#     #     mo.__parse_xlsx_invoice__()
#     #     assert len(mo.rows) == 45
#     #     first_row: MessingschlagerOrderRow = mo.rows[0]  # typing: ignore # mypy: ignore
#     #     assert first_row.quantity == 30
#     #     assert first_row.product.eur_cost_price == 0.38
#     #     assert first_row.product.sku == "420023"
#
#     @staticmethod
#     def test_parse_and_prepare_order():
#         # FIXME pydantic model error
#         mo = MessingschlagerOrder(
#             file_path=f"{config.file_root}test_data/ms-test-invoice.xlsx",
#             reference="test"
#         )
#         mo.__parse_xlsx_invoice__()
#         assert len(mo.rows) == 55
#         first_row = mo.rows[0]  # type: ignore # mypy: ignore
#         assert first_row.quantity == 30
#         assert first_row.product.eur_cost_price == 0.378
#         assert first_row.product.sku == "420023"
#         reflex_fram_list: List[SupplierOrderRow] = [
#             row for row in mo.rows if row.entity.sku == "466008"
#         ]
#         assert len(reflex_fram_list) == 1
#         reflex_fram = reflex_fram_list[0]
#         assert reflex_fram.entity.eur_cost_price == 0.147
#         mo.__update_products_and_import_if_missing__()
#         mo.order_date = datetime(day=1, month=1, year=2022)
#         mo.reference = "test"
#         mo.__prepare_for_import_of_order__()
#         assert mo.dolibarr_supplier.currency == Currency.EUR
