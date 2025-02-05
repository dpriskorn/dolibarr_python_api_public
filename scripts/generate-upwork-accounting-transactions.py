# # parse the csv
# # create an invoice for all entries except withdrawals
# # we have to manually do the withdrawals from Upwork->SEB because there is no Dolibarr API yet
# import logging
#
# import config
# from src.helpers import utilities
# from src.models.banks.upwork import Upwork
#
# logging.basicConfig(level=config.loglevel)
# logger = logging.getLogger(__name__)
#
#
# def main():
#     args = utilities.parse_args()
#     if args.seb and args.upwork:
#         # print("test")
#         upwork = Upwork(
#             seb_csv_file_path=args.seb,
#             upwork_csv_file_path=args.upwork,
#         )
#         upwork.parse_all()
#         # for tr in upwork.seb_transactions:
#         #     print(tr)
#         print(f"Total number of transactions: {len(upwork.accounting_transactions)}")
#         upwork.present()
#     else:
#         print("Did not get all we need. Specify files with --seb and --upwork")
#
#
# if __name__ == "__main__":
#     main()
