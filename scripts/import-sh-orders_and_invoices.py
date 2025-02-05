import logging

import config
from src.helpers import utilities
from src.models.suppliers.shimano import Shimano

logging.basicConfig(level=config.loglevel)


def main():
    # logger = logging.getLogger(__name__)
    args = utilities.parse_args()
    sh = Shimano(args=args)
    sh.scrape_orders()


if __name__ == "__main__":
    main()
