import logging
import sys

import config
from src.helpers import utilities
from src.models.suppliers.bikable.product import BikableProduct

# Setup logger
# from src.models import CykelgearProduct

logging.basicConfig(level=config.loglevel)


def main():
    logger = logging.getLogger(__name__)
    args = utilities.parse_args()
    if not args.url:
        logger.error("Missing url")
        print("Usage: python import-cg-test -u URL")
        # print("Where REF is e.g. 2712345")
        sys.exit(0)
    ref = args.external_ref
    if ref is None:
        ref = ""
    url = args.url
    product = BikableProduct(ref=ref, url=url)
    product.update_and_import_if_missing()


if __name__ == "__main__":
    main()
