import logging
import sys
from pprint import pprint

import config
from src.helpers import utilities
from src.models.suppliers.biltema import BiltemaOrder

logging.basicConfig(level=config.loglevel)
logger = logging.getLogger(__name__)

# pseudo code
# accept list of refs
# for each external_ref ask how many were bought
# add everything to an order
# use current date by default
# add invoice
# validate invoice
# ask user to handle the shipping
# done


def main():
    # raise DeprecationWarning("Update to new model")
    args = utilities.parse_args()
    refs = args.list
    if not refs:
        logger.error("Missing list of refs")
        print("Usage: python import-bt-order.py --list REF [REF...]")
        print(
            "Where list consists of a space-delimited list of refs with dashes"
            + "e.g. 27-1234 or 27-12345"
        )
        sys.exit(0)
    if config.loglevel == logging.DEBUG:
        pprint(refs)
    # exit(0)
    biltema = BiltemaOrder()
    biltema.import_purchase(refs=refs)


if __name__ == "__main__":
    main()
