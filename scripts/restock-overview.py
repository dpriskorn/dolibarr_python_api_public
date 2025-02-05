# import logging
#
# from rich import print
#
# import config
# from src.models.dolibarr.enums import Expired
# from src.models.dolibarr.supplier import DolibarrSupplier
# from src.models.suppliers.enums import SupportedSupplier
#
# logging.basicConfig(level=config.loglevel)
# logger = logging.getLogger(__name__)
#
#
# def print_restock_overview(codename: SupportedSupplier):
#     print("Fetching products")
#     s = DolibarrSupplier(codename=codename)
#     products = s.get_stockable_and_for_sale()
#     print(f"Got {len(products)} products")
#     for p in products:
#         logger.debug(f"Processing {p.label} from {p.url()}")
#         if not p.stock_quantity:
#             logger.debug("No stock quantity")
#             p.stock_quantity = 0
#         if not p.stock_warning_quantity:
#             logger.debug("No warning quantity")
#             p.stock_warning_quantity = 0
#         if p.expired == Expired.FALSE:
#             if p.external_stock > 0:
#                 if (
#                     p.stock_quantity < p.stock_warning_quantity
#                     or p.stock_quantity == p.stock_warning_quantity
#                 ):
#                     print(
#                         f"{p.label} needs to be ordered from {codename} "
#                         f"and is available (last update {p.last_update})"
#                     )
#                 else:
#                     logger.debug("Quantity less than warning threshold")
#             else:
#                 logger.debug("External stock was 0")
#         else:
#             logger.debug("Skipping. Expired")
#
#
# def main():
#     # pseudo code
#     # get products for sale but where the stock is less than we want
#     # attributes we have:
#     # desired_stock_quantity
#     # stock_quantity
#     # stock_warning_quantity
#     # TODO also factor in desired_stock?
#     # bi = DolibarrSupplier(codename=SupportedSupplier.BIKESTER)
#     # bi.enrich_those_with_stock_warning_set()
#     # jo = DolibarrSupplier(codename=SupportedSupplier.JOFRAB)
#     # jo.enrich_those_with_stock_warning_set()
#     ms = DolibarrSupplier(codename=SupportedSupplier.MESSINGSCHLAGER)
#     ms.enrich_those_with_stock_warning_set()
#     # csn = supplier.Supplier('CSN')
#     # csn.enrich_those_with_stock_warning_set()
#     # jv = supplier.Supplier('JV')
#     # jv.enrich_those_with_stock_warning_set()
#     # bt = DolibarrSupplier("BT")
#     # bt.enrich_those_with_stock_warning_set()
#     # print("Symaskin:")
#     # nt = supplier.Supplier('NT')
#     # nt.enrich_those_with_stock_warning_set()
#     # print_restock_overview(codename=SupportedSupplier.BIKESTER)
#     # print_restock_overview(codename=SupportedSupplier.JOFRAB)
#     print_restock_overview(codename=SupportedSupplier.MESSINGSCHLAGER)
#
#
# if __name__ == "__main__":
#     main()
