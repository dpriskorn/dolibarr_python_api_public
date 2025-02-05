# class TestAccountingTransaction:
#     # fixme test the whole thing
#     # def test_parse_csv(self):
#     #     u = Upwork(file_path="../../test_data/upwork.csv", total_amount_in_sek=0.0)
#     #     u.__parse_upwork_csv__()
#     #     assert u.number_of_transactions == 10
#     #
#     # def test_gross_income(self):
#     #     u = Upwork(file_path="../../test_data/upwork.csv", total_amount_in_sek=0.0)
#     #     u.__parse_upwork_csv__()
#     #     assert u.gross_income == 1905.0
#     #
#     # def test_gross_fees(self):
#     #     u = Upwork(file_path="../../test_data/upwork.csv", total_amount_in_sek=0.0)
#     #     u.__parse_upwork_csv__()
#     #     assert u.gross_fees == 97.24
#     #
#     # def test_payouts(self):
#     #     u = Upwork(file_path="../../test_data/upwork.csv", total_amount_in_sek=0.0)
#     #     u.__parse_upwork_csv__()
#     #     assert u.payouts == 7735.76
#     #
#     # def test_total_vat(self):
#     #     u = Upwork(file_path="../../test_data/upwork.csv", total_amount_in_sek=0.0)
#     #     u.__parse_upwork_csv__()
#     #     assert u.total_vat == 400.448
#     #     assert u.vat_left_to_pay + u.vat_already_paid == u.total_vat
#     #
#     # def test_total_vat_on_income(self):
#     #     u = Upwork(file_path="../../test_data/upwork.csv", total_amount_in_sek=0.0)
#     #     u.__parse_upwork_csv__()
#     #     assert u.income_vat == 381.0
#     #
#     # def test_total_vat_on_fees(self):
#     #     u = Upwork(file_path="../../test_data/upwork.csv", total_amount_in_sek=0.0)
#     #     u.__parse_upwork_csv__()
#     #     assert u.vat_on_fees == 19.447999999999993
#     #
#     # def test_vat_left_to_pay(self):
#     #     u = Upwork(file_path="../../test_data/upwork.csv", total_amount_in_sek=0.0)
#     #     u.__parse_upwork_csv__()
#     #     assert u.vat_left_to_pay == 399.568
#     #
#     # def test_vat_already_paid(self):
#     #     u = Upwork(file_path="../../test_data/upwork.csv", total_amount_in_sek=0.0)
#     #     u.__parse_upwork_csv__()
#     #     assert u.vat_already_paid == 0.88
#     #
#     # def test_net_income_before_fees(self):
#     #     u = Upwork(file_path="../../test_data/upwork.csv", total_amount_in_sek=0.0)
#     #     u.__parse_upwork_csv__()
#     #     assert u.net_income_before_fees == 1524.0
#     #
#     # def test_net_fees(self):
#     #     u = Upwork(file_path="../../test_data/upwork.csv", total_amount_in_sek=0.0)
#     #     u.__parse_upwork_csv__()
#     #     assert u.net_fees == 77.792
#     #
#     # def test_net_income_after_net_fees(self):
#     #     u = Upwork(file_path="../../test_data/upwork.csv", total_amount_in_sek=0.0)
#     #     u.__parse_upwork_csv__()
#     #     assert u.net_income_after_net_fees == 1446.208
#     #
#     # def test_gross_income_minus_vat_already_paid(self):
#     #     u = Upwork(file_path="../../test_data/upwork.csv", total_amount_in_sek=0.0)
#     #     u.__parse_upwork_csv__()
#     #     assert u.gross_income_minus_vat_already_paid == 1904.12
#     #
#     # def test_withdrawn_by_upwork_before_payout(self):
#     #     u = Upwork(file_path="../../test_data/upwork.csv", total_amount_in_sek=0.0)
#     #     u.__parse_upwork_csv__()
#     #     assert u.withdrawn_by_upwork_before_payout == 98.11999999999999
#     #
#     # def test_income_vs_withdrawn_balance(self):
#     #     u = Upwork(file_path="../../test_data/upwork.csv", total_amount_in_sek=0.0)
#     #     u.__parse_upwork_csv__()
#     #     assert u.income_vs_withdrawn_balance == -5928.88
#     #
#     # # def test_net_income_after_fees_and_vat(self):
#     # #     u = Upwork(file_path="../test_data/upwork.csv", total_amount_in_sek=0.0)
#     # #     u.parse_csv()
#     # #     assert u.net_ == 1446.208
#     #
#     # def test_expected_payout(self):
#     #     u = Upwork(file_path="../../test_data/upwork.csv", total_amount_in_sek=0.0)
#     #     u.__parse_upwork_csv__()
#     #     assert u.expected_payout == 1806.88
#
#     # def test_generate_account_statement(self):
#     #     u = Upwork(file_path="../../test_data/upwork.csv", total_amount_in_sek=0.0)
#     #     u.generate_account_statement()
#     #     assert u.accounting_transactions == AccountingTransaction(
#     #         debet_1931=1904.12,
#     #         credit_2610=399.568,
#     #         debet_2610=0.88,
#     #         credit_6900=77.792,
#     #         credit_3003=1446.208,
#     #     )
#     #     assert u.accounting_transactions.is_balanced is True
#     def test_sek_amount(self):
#         raise AssertionError()
#
#     def test_number_of_transactions(self):
#         raise AssertionError()
#
#     def test_is_balanced(self):
#         raise AssertionError()
#
#     def test_net_fees(self):
#         raise AssertionError()
#
#     def test_net_income_before_fees(self):
#         raise AssertionError()
#
#     def test_vat_on_fees(self):
#         raise AssertionError()
#
#     def test_net_income_after_net_fees(self):
#         raise AssertionError()
#
#     def test_income_vat(self):
#         raise AssertionError()
#
#     def test_total_vat(self):
#         raise AssertionError()
#
#     def test_vat_left_to_pay(self):
#         raise AssertionError()
#
#     def test_gross_income_minus_vat_already_paid(self):
#         raise AssertionError()
#
#     def test_withdrawn_by_upwork_before_payout(self):
#         raise AssertionError()
#
#     def test_income_vs_withdrawn_balance(self):
#         raise AssertionError()
#
#     def test_expected_payout(self):
#         raise AssertionError()
#
#     def test_fee_percentage(self):
#         raise AssertionError()
#
#     def test_gross_income(self):
#         raise AssertionError()
#
#     def test_gross_fees(self):
#         raise AssertionError()
#
#     def test_vat_already_paid(self):
#         raise AssertionError()
#
#     def test_withdrawal_amount(self):
#         raise AssertionError()
#
#     def test_rate(self):
#         raise AssertionError()
#
#     def test_seb_date(self):
#         raise AssertionError()
#
#     def test_calculate_and_output_results(self):
#         raise AssertionError()
