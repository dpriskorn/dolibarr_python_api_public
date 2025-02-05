# import logging
# import sys
#
# # from src.models import dolibarr_product
# import config
# from src.helpers import utilities
# from src.models.suppliers.messingschlager.product import MessingschlagerProduct
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
#         print("Usage: python import-ms-product.py -r REF")
#         print("Where REF is e.g. 1863031")
#         sys.exit(0)
#     ms = MessingschlagerProduct(ref=args.external_ref)
#     ms.update_and_import_if_missing()
#
#
# if __name__ == "__main__":
#     main()
