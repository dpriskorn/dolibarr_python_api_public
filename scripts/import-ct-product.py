# import logging
# import sys
#
# # from src.models import dolibarr_product
# import config
# from src.helpers import utilities
# from src.models.suppliers.cycletech.product import CycletechProduct
#
# logging.basicConfig(level=config.loglevel)
# logger = logging.getLogger(__name__)
#
#
# def main():
#     # raise DeprecationWarning("Update to new model")
#     args = utilities.parse_args()
#     if not args.external_ref:
#         logger.error("Missing external_ref")
#         print("Usage: python import-ct-product.py -r REF")
#         print("Where REF is e.g. 1234")
#         sys.exit(0)
#     ct = CycletechProduct(ref=args.external_ref)
#     ct.update_and_import_if_missing()
#
#
# if __name__ == "__main__":
#     main()
