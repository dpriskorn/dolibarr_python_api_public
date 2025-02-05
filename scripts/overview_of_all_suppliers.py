# import logging
#
# import config
# from src.models.dolibarr.supplier import DolibarrSupplier
# from src.models.suppliers.enums import SupportedSupplier
#
# logging.basicConfig(level=config.loglevel)
# logger = logging.getLogger(__name__)
#
# print("Cykel:")
# ms = DolibarrSupplier(codename=SupportedSupplier.MESSINGSCHLAGER)
# ms.overview()
# jo = DolibarrSupplier(codename=SupportedSupplier.JOFRAB)
# jo.overview()
# csn = DolibarrSupplier(codename=SupportedSupplier.CYCLESERVICENORDIC)
# csn.overview()
# jv = DolibarrSupplier(codename=SupportedSupplier.JAGUARVERKEN)
# jv.overview()
# bt = DolibarrSupplier(codename=SupportedSupplier.BILTEMA)
# bt.overview()
# # print("Symaskin:")
# # nt = DolibarrSupplier('NT')
# # nt.overview()
