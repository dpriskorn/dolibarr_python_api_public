# import argparse
# import sys
#
# # pseudo code
# # parse xlsx from MS -> parse()
# #  check if already exist
# #  yes: -> update_price()
# #  no: -> import_missing_product()
# # import products if not found asking for cost and prices for level 1+2, find
# # weight, scrape picture url, scrape product url
# # import_as_order()
# #  create order based on quantity and product_refs
# #  validate order
# #  create invoice
# from src.helpers.utilities import ask_yes_no_question
# from src.models.suppliers.messingschlager.order import MessingschlagerOrder
#
#
# def main():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-f", "--file", help="XLSX file to parse")
#     parser.add_argument("--debug", help="Output debug messages.", action="store_true")
#     args = parser.parse_args()
#     file = args.file
#     if file:
#         if ask_yes_no_question(
#             "Did you update the config.py with the latest SEK/EUR rate from SEB on the transaction to MS?"
#         ):
#             mo = MessingschlagerOrder(file_path=file)
#             mo.parse_and_import_order()
#         else:
#             print("Please update the rate and run the script again")
#             sys.exit(1)
#     else:
#         print("No file specified. See -h for help.")
#
#
# if __name__ == "__main__":
#     main()
