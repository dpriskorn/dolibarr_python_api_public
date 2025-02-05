# import logging
#
# from consolemenu.console_menu import SelectionMenu
# #from consolemenu import SelectionMenu  # type: ignore
#
# import config
# # from src.helpers.utilities import ask_yes_no_question
# from src.models.dolibarr.supplier import DolibarrSupplier
# from src.models.suppliers.enums import SupportedSupplier
#
# logging.basicConfig(level=config.loglevel)
# logger = logging.getLogger(__name__)
#
#
# def select_supplier():
#     """Generalized select menu"""
#     menu = SelectionMenu(SupportedSupplier.__members__.keys(), "Select a supplier")
#     menu.show()
#     menu.join()
#     selected_index = menu.selected_option
#     mapping = {}
#     for index, item in enumerate(SupportedSupplier):
#         mapping[index] = item
#     selected_entity = mapping[selected_index]
#     logger.debug(f"selected:{selected_index}=" f"{selected_entity}")
#     return selected_entity
#
#
# def main():
#     supplier: SupportedSupplier = select_supplier()
#     # if supplier is SupportedSupplier.MESSINGSCHLAGER:
#     #     ms = DolibarrSupplier('MS')
#     #     answer = ask_yes_no_question("Do you want to enrich all?")
#     #     if answer:
#     #         ms.enrich_all()
#     #     else:
#     #         answer = ask_yes_no_question("Do you want to enrich those with stock warning set?")
#     #         if answer:
#     #             ms.enrich_those_with_stock_warning_set()
#     #     ms.overview()
#     if supplier is SupportedSupplier.SHIMANO:
#         sh = DolibarrSupplier(codename=SupportedSupplier.SHIMANO)
#         answer = ask_yes_no_question("Do you want to enrich all?")
#         if answer:
#             sh.enrich_all()
#         else:
#             answer = ask_yes_no_question(
#                 "Do you want to enrich those with stock warning set?"
#             )
#             if answer:
#                 sh.enrich_those_with_stock_warning_set()
#         sh.overview()
#     else:
#         print("Not implemented yet for this supplier")
#     # jo = dolibarr_supplier.DolibarrSupplier('JO')
#     # jo.overview()
#     # csn = dolibarr_supplier.DolibarrSupplier('CSN')
#     # csn.overview()
#     # jv = dolibarr_supplier.DolibarrSupplier('JV')
#     # jv.overview()
#     # bt = dolibarr_supplier.DolibarrSupplier('BT')
#     # bt.overview()
#
#
# if __name__ == "__main__":
#     main()
