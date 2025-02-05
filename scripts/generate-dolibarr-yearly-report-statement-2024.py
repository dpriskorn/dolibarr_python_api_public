import logging

import config
from src.models.dolibarr.accounting.report import Report

logging.basicConfig(level=config.loglevel)


def main():
    dar = Report(year=2024, eu_goods=False)
    dar.start()


if __name__ == "__main__":
    main()
