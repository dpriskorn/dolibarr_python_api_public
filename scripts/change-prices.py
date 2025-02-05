# import logging
# import sys
#
# import config
# from src.helpers.utilities import parse_args
# from src.models.dolibarr.entities import Entities
#
# logging.basicConfig(level=config.loglevel)
# logger = logging.getLogger(__name__)
#
#
# def main():
#     args = parse_args()
#     if args.new_multiprice1 is None or not args.pattern:
#         logger.error("Missing new price or pattern")
#         print("Usage: python change-prices.py --pattern '%slang%' --new-multiprice1 95")
#         sys.exit(0)
#     # Prices are always net prices in the object
#     multiprice1 = float(args.new_multiprice1) / 1.25
#     pattern = args.pattern
#     print("Fetching matching products...")
#     entities = Entities()
#     products = entities.search_stocked_and_for_sale(label=pattern)
#     if len(products) > 0:
#         print(f"Updating to {multiprice1}")
#         for p in products:
#             print(f"Processing: {p.label}")
#             if p.multiprice1 is None or p.multiprice1 != multiprice1:
#                 answer = self.ask_yes_no_question("Update multiprice1?")
#                 if answer:
#                     p.multiprice1 = multiprice1
#                     p.update_multiprices()
#             else:
#                 logger.info("Price is already correct")
#     else:
#         raise ValueError("Got no products")
#
#
# if __name__ == "__main__":
#     main()
