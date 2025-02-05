import logging

import config
from src.helpers import utilities
from src.models.suppliers.cycleservicenordic.product import CycleServiceNordicProduct
from src.models.suppliers.enums import SupportedSupplier

logging.basicConfig(level=config.loglevel)


def main():
    args = utilities.parse_args()
    if not args.external_ref and not args.url:
        raise ValueError("Need external_ref or url, see -h.")
    product = CycleServiceNordicProduct(
        sku=str(args.external_ref),
        url=str(args.url) if args.url is not None else "",
        codename=SupportedSupplier.CYCLESERVICENORDIC,
    )
    if not product.codename:
        raise ValueError("no codename")
    product.update_and_import_if_missing()


if __name__ == "__main__":
    main()
