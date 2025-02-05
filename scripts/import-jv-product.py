import logging

# import pprint as pprint
import config

# from src.models import dolibarr_product

logging.basicConfig(level=config.loglevel)


def main():
    raise DeprecationWarning("Update to new model")
    # logger = logging.getLogger(__name__)
    # args = utilities.parse_args()
    # print(f"rootlogger loglevel:{logger.getEffectiveLevel()}")
    # if not args.url and not args.external_ref:
    #     if not args.external_ref:
    #         logger.error("Missing external_ref")
    #         print("Usage: python import-jo-test -r REF")
    #         print("Where REF is e.g. 10950805")
    #         exit(0)
    #     if not args.url:
    #         logger.error("Missing url")
    #         print("Usage: python import-jo-test -u URL")
    #         exit(0)
    # jv = jaguarverken.Jaguarverken(args=args)
    # if args.url:
    #     data = jv.scrape_product(url=args.url)
    # else:
    #     raise ValueError("Ref lookup is not supported yet")
    #     # data = jv.scrape_product(external_ref=args.external_ref)
    # if not data:
    #     raise ValueError("Data was None")
    # # Create new product
    # dolibarr_product.DolibarrProduct(data=data)
