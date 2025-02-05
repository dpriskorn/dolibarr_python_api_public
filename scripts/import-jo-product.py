import logging
import sys

import config
from src.helpers import utilities
from src.models.suppliers.hoj24.product import Hoj24Product

logging.basicConfig(level=config.loglevel)
logger = logging.getLogger(__name__)


def main():
    args = utilities.parse_args()
    if not args.url and not args.external_ref:
        if not args.external_ref:
            logger.error("Missing external_ref")
            print("Usage: python import-jo-test -r REF")
            print("Where REF is e.g. 18-639-031")
            sys.exit(0)
        if not args.url:
            logger.error("Missing url")
            print("Usage: python import-jo-test -u URL")
            sys.exit(0)
    # jo = Jofrab(args=args)
    if args.external_ref is not None:
        product = Hoj24Product(ref=args.external_ref)
        product.update_and_import_if_missing()
    elif args.url is not None:
        product = Hoj24Product(url=args.url)
        product.update_and_import_if_missing()
    else:
        raise ValueError("got neither ref or url")


if __name__ == "__main__":
    main()
