# pseudo code
# get all services
import logging

import config

logging.basicConfig(level=config.loglevel)
logger = logging.getLogger(__name__)

# if p.status_sell == Status.ENABLED and p.multiprice1 is None:
#     print(product)
#     raise DebugExit()

# e = Entities()
# services = e.get_services()
# print(f"Got {len(services)} services")
# for service in services:
#     if (
#         service.is_bike_entity
#     ):
#         service.fetch_purchase_data_and_finish_parsing()
#         if service.selling_vat_rate is not VatRate.SIX:
#             print(f"service.multiprice1 was {service.multiprice1} before the update")
#             print(f"Updating VAT of {service.label} to 6%")
#             service.selling_vat_rate = VatRate.SIX
#             service.update()
#             print(service.selling_price_url)
#             raise DebugExit()
#     else:
#         print(f"{service.label} was not a bike entity")
#         print(service.dict())
#         raise DebugExit()
