import logging

# from src.models import NivatexProduct
import config

logging.basicConfig(level=config.loglevel)


def main():
    raise DeprecationWarning("Update to new model")
    # logger = logging.getLogger(__name__)
    # args = utilities.parse_args()
    # if not args.external_ref:
    #     logger.error("Missing external_ref")
    #     print("Usage: python import-jo-test -r REF")
    #     print("Where REF is e.g. 10950805")
    #     exit(0)
    # else:
    #     product = NivatexProduct(ref=args.external_ref)
    #     product.import_if_missing()


if __name__ == "__main__":
    main()
