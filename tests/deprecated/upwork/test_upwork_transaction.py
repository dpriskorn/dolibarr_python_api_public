# from unittest import TestCase
#
# from src.models.banks.upwork import Upwork, UpworkTransaction
#
#
# class TestUpworkTransaction(TestCase):
#     @staticmethod
#     def test_instantiation():
#         data = {
#             "Date": "Jun 29, 2022",
#             "Ref ID": "490949047",
#             "Type": "Withdrawal Fee",
#             "Description": "Withdrawal Fee - Direct to Local Bank",
#             "Agency": "",
#             "Freelancer": "",
#             "Team": "",
#             "Account Name": "Dennis Priskorn",
#             "PO": "",
#             "Amount": "-0.99",
#             "Amount in local currency": "",
#             "Currency": "",
#             "Balance": "5.00",
#         }
#         u = Upwork(upwork_csv_file_path="", seb_csv_file_path="")
#         tr = UpworkTransaction(**u.__clean_dictionary__(data))
#         assert tr.amount == -0.99
#         assert tr.ref_id == 490949047
#
#     @staticmethod
#     def test_get_date():
#         pass
