import logging

import config
from src.helpers import utilities
from src.models.suppliers.hoj24 import Hoj24

# Setup logger
logging.basicConfig(level=config.loglevel)


def main():
    args = utilities.parse_args()
    j = Hoj24(args=args)
    j.scrape_orders()


if __name__ == "__main__":
    main()
