import logging
import sys

import config
from src.helpers import utilities
from src.models.suppliers.shimano.product import ShimanoProduct

logging.basicConfig(level=config.loglevel)
logger = logging.getLogger(__name__)


def main():
    args = utilities.parse_args()
    if not args.external_ref:
        logger.error("Missing external_ref")
        print("Usage: python import-sh-test -r REF")
        print("Where REF is e.g. 2712345")
        sys.exit(0)
    # if not args.url:
    #     logger.error("Missing url")
    #     print("Usage: python import-sh-test -u URL")
    #     #print("Where REF is e.g. 2712345")
    #     exit(0)
    ref = args.external_ref
    # url = args.url
    product = ShimanoProduct(sku=ref, url="")
    product.update_and_import_if_missing()


# def main():
#     print('Number of arguments:', len(sys.argv), 'arguments.')
#     print('Argument List:', str(sys.argv))

# with shimano.login() as s:
#     data = shimano.scrape_product(external_ref=sys.argv[1],
#                                             session=s)
#     if not data:
#         raise ValueError("Data was None")
#     if "search_url" in data:
#         raise ValueError(f"Could not find product at {data['search_url']}")
#     # Create new product
#     models.dolibarr_product.DolibarrProduct(data=data)


if __name__ == "__main__":
    main()
