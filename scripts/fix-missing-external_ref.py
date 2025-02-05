# pseudo code
# get all products
import logging

import config
from src.views.dolibarr.entities import DolibarrEntitiesView

logging.basicConfig(level=config.loglevel)
logger = logging.getLogger(__name__)

e = DolibarrEntitiesView()
e.get_stocked_and_for_sale_with_missing_external_ref()
# products = e.get_stockable_products()
# print(f"Got {len(products)} products")
# for product in products:
#     if not product.external_ref:
#         print(f"no external ref found on: {product.url}")
