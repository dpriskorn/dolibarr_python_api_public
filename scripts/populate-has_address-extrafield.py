# """The purpose of this code is to populate an
# extrafield so we can easily find customers with no address.
#
# The reason for this is regulatory.
# I have to store the address of all customers it seems."""
# import logging
#
# from src.helpers.crud.create import Create
# from src.models.dolibarr.enums import DolibarrEndpoint, DolibarrTable
# #
# logger = logging.getLogger(__name__)
# #
# # main
# count = 0
# r = self.api.call_list_api(
#     # get customers only
#     endpoint=DolibarrEndpoint.THIRDPARTIES,
#     params={"mode": "1", "limit": "400"},
# )
# if r.status_code == 200:
#     customers = r.json()
#     logger.info(f"got {len(customers)} customers")
#     for customer in customers:
#         # ignore traderaköpare och upwork kund
#         ignorelist = [730, 737]
#         if customer["id"] not in ignorelist:
#             has_address = self.extrafield(customer, "has_address")
#             # only check those not already set to 1
#             if has_address != "1" or not has_address:
#                 logger.info(f"processing {customer['name']}")
#                 logger.debug(customer["address"])
#                 count += 1
#                 if customer["address"] == "" or customer["address"] is None:
#                     self.create.insert_extrafield(
#                         DolibarrTable.THIRDPARTY, customer["id"], "has_address", 0
#                     )
#                 else:
#                     self.create.insert_extrafield(
#                         DolibarrTable.THIRDPARTY, customer["id"], "has_address", 1
#                     )
# print(f"{count} customers were updated")
