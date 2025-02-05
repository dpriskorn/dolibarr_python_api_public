import logging

# from src.models import CycleServiceNordic
import config
from src.models.suppliers.cycleservicenordic.__init__ import CycleServiceNordic

logging.basicConfig(level=config.loglevel)

# raise Exception("Not finished")
# raise DeprecationWarning("Update to new model")
csn = CycleServiceNordic()
csn.scrape_orders()
