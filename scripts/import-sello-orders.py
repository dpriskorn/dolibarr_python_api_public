import logging

import config
from src.controllers.marketplaces.sello.orders import SelloOrdersContr

logging.basicConfig(level=config.loglevel)


selloorders = SelloOrdersContr()
selloorders.import_orders()

# om order finns i sello:
# om delivered_at er not null:
# kolla om leveransdatum är inlagd i dolibarr
# lägg till leverans och skapa shipment och
# valider shipment och stäng shipment
