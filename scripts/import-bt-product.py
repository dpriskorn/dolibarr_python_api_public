import logging
import sys

# Setup logger
import config
from src.helpers import utilities
from src.models.dolibarr.product import DolibarrProduct
from src.models.suppliers.biltema import BiltemaProduct
from src.models.suppliers.enums import SupportedSupplier

logging.basicConfig(level=config.loglevel)


def main():
    logger = logging.getLogger(__name__)
    args = utilities.parse_args()
    ref = args.external_ref
    if not ref:
        logger.error("Missing external_ref")
        print("Usage: python import-bt-test REF")
        print("Where REF is e.g. 27-12345")
        sys.exit(0)
    # url = args.url
    # get it if it already exists
    p = DolibarrProduct()
    p = p.get_by_external_ref(codename=SupportedSupplier.BILTEMA, external_ref=ref)
    if p:
        logger.info(
            f"Skipping existing external_ref: {ref} "
            f"for product {p.label}, see {p.url()}"
        )
    else:
        logger.debug("Not found")
        bt = BiltemaProduct(sku=ref)
        bt.update_and_import_if_missing()


if __name__ == "__main__":
    main()
