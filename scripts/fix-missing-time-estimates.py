# # pseudo code
# # get all services
# import logging
#
# import config
# # from src.helpers.enums import InputType
# from src.models.dolibarr.entities import Entities
# from src.models.dolibarr.enums import Status
#
# logging.basicConfig(level=config.loglevel)
# logger = logging.getLogger(__name__)
#
# e = Entities()
# services = e.get_services()
# print(f"Got {len(services)} services")
# service_missing_workminutes = []
# for service in services:
#     if (
#         service.ref is not None
#         and "cykel-product" in service.ref
#         and service.status_sell == Status.ENABLED
#         and not service.work_minutes
#     ):
#         service_missing_workminutes.append(service)
#         # print(product.dict())
#         # if :
#         # raise DebugExit()
# #     if ref starting with cykel-product
# #         if no time estimate
# print(
#     f"{len(service_missing_workminutes)} bike services are misisng a time estimate"
# )
# for service in service_missing_workminutes:
#     minutes = self.ask_mandatory(
#         input_type=InputType.INTEGER,
#         text=f"{service.label}: {service.multiprice1} kr: how many minutes does this take?",
#         unit="min",
#     )
#     service.set_work_minutes(minutes=minutes)
#     service.update_extrafields()
#     print(service.url)
#     # raise DebugExit()
# #             ask user for estimate
# #             save estimate
