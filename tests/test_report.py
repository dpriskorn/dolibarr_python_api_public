from unittest import TestCase

from pandas import DataFrame

from src.models.dolibarr.accounting.report import Report


class TestReport(TestCase):
    def test_get_all_accounting_statements(self):
        dar = Report(year=2024, eu_goods=False)
        dar.get_all_accounting_statements()
        assert dar.data is not None
        # assert False

    def test_covnert_to_df(self):
        dar = Report(year=2024, eu_goods=False)
        dar.get_all_accounting_statements()
        dar.convert_to_dataframe()
        assert isinstance(dar.dataframe, DataFrame)
        # print(df.info())

    def test_calculate_income(self):
        dar = Report(year=2024, eu_goods=False)
        dar.get_data_and_calculate()
        assert dar.total_income != 0

    def test_calculate_expenses(self):
        dar = Report(year=2024, eu_goods=False)
        dar.get_data_and_calculate()
        assert dar.total_expenses != 0
        assert dar.eu_goods_expenses == 0
        assert dar.eu_service_expenses != 0
        assert dar.total_eu_expenses != 0

    def test_calculate_change_in_stock_value(self):
        dar = Report(year=2024, eu_goods=False)
        dar.get_data_and_calculate()
        assert dar.change_in_stock_value == -12708

    def test_calculate_profit(self):
        dar = Report(year=2024, eu_goods=False)
        dar.get_data_and_calculate()
        assert dar.profit != 0

    def test_calculate_tax(self):
        # todo add test for year with eu goods
        # 2024
        dar = Report(year=2024, eu_goods=False)
        dar.get_data_and_calculate()
        assert dar.total_eu_service_vat == 220
        assert dar.total_eu_goods_vat == 0
        assert dar.total_outgoing_vat_eu_25 == 220
        assert dar.incoming_vat_to_report == 10757
        assert dar.vat_debt == 8793
        assert dar.total_outgoing_vat == 19770

    def test_calculate_own_withdrawals(self):
        dar = Report(year=2024, eu_goods=False)
        dar.get_data_and_calculate()
        assert dar.own_withdrawal == 5767

    def test_check_own_withdrawal(self):
        dar = Report(year=2024, eu_goods=False)
        dar.get_data_and_calculate()
        dar.check_own_withdrawal()
        assert dar.own_withdrawal == 5767
