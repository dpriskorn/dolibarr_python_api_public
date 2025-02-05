# pseudo code
# get all products
import logging

import config
from src.views.dolibarr.entities import DolibarrEntitiesView

logging.basicConfig(level=config.loglevel)
logger = logging.getLogger(__name__)

e = DolibarrEntitiesView()
products = e.get_stockable_products()
print(f"Got {len(products)} products")
for product in products:
    if not product.currency:
        product.__update_purchase_price__()
        # product.__insert_multiprices__()
        print(f"updated prices on: {product.url}")
    # raise DebugExit()
#             ask user for estimate
#             save estimate
