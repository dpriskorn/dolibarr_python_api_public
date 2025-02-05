import logging
from typing import TYPE_CHECKING

from psycopg2 import sql  # type: ignore

import config
from src.helpers.crud.postgres import Postgres
from src.models.exceptions import DeprecatedMethodError

if TYPE_CHECKING:
    from src.models.dolibarr.product import DolibarrProduct

logger = logging.getLogger(__name__)


class Delete(Postgres):
    def delete_purchase_prices(self, product: "DolibarrProduct" = None):
        if config.deprecate_database_methods:
            raise DeprecatedMethodError()
        if not product:
            raise ValueError("Product was None")
        from src.models.dolibarr.product import DolibarrProduct

        if not isinstance(product, DolibarrProduct):
            raise ValueError("not a DolibarrProduct")
        # TODO lookup supplier_id from codename
        from src.models.dolibarr.supplier import DolibarrSupplier

        dolibarr_supplier = DolibarrSupplier(codename=product.codename)
        dolibarr_supplier.update_attributes_from_dolibarr()
        self.connect()
        # Create a cursor object
        cur = self.connection.cursor()
        # Delete and insert
        query = sql.SQL(
            "DELETE FROM "
            + "public.llx_product_fournisseur_price "
            + "WHERE fk_soc = %s AND ref_fourn=%s"
        )
        r = cur.mogrify(query, [dolibarr_supplier.id, product.external_ref])
        logger.debug(r)
        cur.execute(r)
        cur.close()
        try:
            self.connection.commit()
        except ConnectionError:
            logger.error("Could not commit to db")
        logger.info("Removed old purchase prices from this supplier")
