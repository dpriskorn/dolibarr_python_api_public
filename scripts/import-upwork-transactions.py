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
#     if args.file:
#         print("test")
#         ut = Upwork(file_path=args.file)
#         ut.parse_csv()
#         print(f"got {len(ut.transactions)} transactions")
#         ut.import_invoices()
#         pass
#     else:
#         print("Got no file. Specify it with --file")
#
#
# if __name__ == "__main__":
#     main()
