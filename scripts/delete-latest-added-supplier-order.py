from src.models.dolibarr import DolibarrEndpoint
from src.views.dolibarr.entities import DolibarrEntitiesView

# main
e = DolibarrEntitiesView()
e.delete_latest_added_entity(endpoint=DolibarrEndpoint.SUPPLIER_ORDER)
