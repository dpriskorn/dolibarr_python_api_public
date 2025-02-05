import logging

import psycopg2  # type: ignore
from psycopg2 import extras, sql  # type: ignore

import config
from src.helpers.crud.postgres import Postgres
from src.models.dolibarr.enums import Currency
from src.models.exceptions import DeprecatedMethodError
from src.models.suppliers.enums import SupportedSupplier

logger = logging.getLogger(__name__)


class Read(Postgres):
    def get_currency_id(self, currency: Currency = None) -> int:
        if currency:
            self.connect()
            return self.get_fk_multicurrency(currency)
        else:
            raise ValueError("Got None.")

    def get_fk_multicurrency(self, multicurrency_code):
        if config.deprecate_database_methods:
            raise DeprecatedMethodError()
        if isinstance(multicurrency_code, Currency):
            multicurrency_code = multicurrency_code.value
        # Get fk_multicurrency
        self.connect()
        # Create a cursor object
        cur = self.connection.cursor()
        # Delete and insert
        query = sql.SQL(
            "SELECT rowid FROM " + "public.llx_multicurrency " + "WHERE code = %s"
        )
        r = cur.mogrify(query, [multicurrency_code])
        logger.debug(r)
        cur.execute(r)
        if cur.rowcount > 0:
            result = cur.fetchone()
            fk_multicurrency = result[0]
            cur.close()
            logger.debug(
                f"Found fk_multicurrency: {fk_multicurrency} for {multicurrency_code}"
            )
        else:
            raise ValueError(
                "Could not find fk_multicurrency " + f"for {multicurrency_code}"
            )

        return fk_multicurrency

    def list_tradera_categories(self, search_term):
        self.connect()
        # Create a cursor object
        cur = self.connection.cursor()
        # Check if Tradera ID was given
        try:
            int(search_term)
            query = sql.SQL(
                "SELECT rowid,ref_ext,label FROM "
                + "public.llx_categorie WHERE "
                + "ref_ext = %s ORDER BY label ASC"
            )
            r = cur.mogrify(query, [search_term])
            cur.execute(r)
            logger.debug(r)
            if cur.rowcount > 0:
                result = cur.fetchall()
                cur.close()

                return result
        except ValueError:
            query = sql.SQL(
                "SELECT rowid,ref_ext,label FROM "
                + "public.llx_categorie WHERE "
                + "LOWER(label) like %s AND ref_ext IS NOT NULL "
                + "ORDER BY label ASC"
            )
            r = cur.mogrify(query, [search_term.lower()])
            cur.execute(r)
            logger.debug(r)
            if cur.rowcount > 0:
                result = cur.fetchall()
                cur.close()

                return result

    def get_dolibarr_product_id_by_external_ref(
        self, external_ref: str, codename: SupportedSupplier
    ) -> int:
        self.connect()
        # Create a cursor object
        cur = self.connection.cursor()
        query = sql.SQL(
            "select fk_object  from llx_product_extrafields where external_ref = %s and main_supplier_codename = %s"
            # "SELECT rowid FROM " + "public.llx_multicurrency " + "WHERE code = %s"
        )
        r = cur.mogrify(query, [external_ref, codename.value])
        logger.debug(r)
        # raise DebugExit()
        cur.execute(r)
        if cur.rowcount > 0:
            result = cur.fetchone()
            product_id = int(result[0])
            logger.debug(f"Found id: {product_id}")
        else:
            product_id = 0
            logger.debug(f"Could not find id for '{external_ref}' from {codename.name}")
        cur.close()

        return product_id

    # def has_tradera_category(product_id):
    #     logger = logging.getLogger(__name__)
    #     self.connect()
    #     # Create a cursor object
    #     cur = self.connection.cursor()
    #     # Check if exist first
    #     query = sql.SQL(
    #         "SELECT fk_categorie "
    #         + "FROM public.llx_categorie_product "
    #         + "WHERE fk_product=%s"
    #     )
    #     r = cur.mogrify(query, [product_id])
    #     logger.debug(r)
    #     cur.execute(r)
    #     if cur.rowcount > 0:
    #         result = cur.fetchall()
    #         if result and len(result) > 0:
    #             for id in result:
    #                 query = sql.SQL(
    #                     "SELECT rowid,label FROM "
    #                     + "public.llx_categorie WHERE "
    #                     + "rowid=%s AND ref_ext IS NOT NULL"
    #                 )
    #                 r = cur.mogrify(query, [id[0]])
    #                 cur.execute(r)
    #                 logger.debug(r)
    #                 if cur.rowcount > 0:
    #                     result = cur.fetchone()
    #                     print(
    #                         "The product already has the tradera "
    #                         + f"category: {result[1]}."
    #                     )
    #                     cur.close()
    #
    #                     return True
    #     else:
    #         cur.close()
    #
    #         return False

    # def check_if_product_was_imported_with_python(supplier_product_id, supplier_id):
    #     logger = logging.getLogger(__name__)
    #     # Don't confuse with find_product_id_from_supplier_ref
    #     self.connect()
    #     # Create a cursor object
    #     cur = self.connection.cursor()
    #     query = sql.SQL(
    #         "SELECT fk_product FROM "
    #         + "public.llx_product_fournisseur_price WHERE "
    #         + "ref_fourn=%s AND fk_soc=%s "
    #         + "AND NOT import_key = 'script'"
    #     )
    #     r = cur.mogrify(query, [supplier_product_id, supplier_id])
    #     cur.execute(r)
    #     logger.debug(r)
    #     if cur.rowcount > 0:
    #         product_id = cur.fetchone()[0]
    #         cur.close()
    #
    #         return product_id
    #     else:
    #         cur.close()
    #
    #         return False
    # def get(id) -> Optional[Dict[Any, Any]]:
    #     logger = logging.getLogger(__name__)
    #     if int(id) != 0:
    #         # Get fk_multicurrency
    #         self.connect()
    #         # Create a cursor object
    #         cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #         # Delete and insert
    #         query = sql.SQL(
    #             "select label, external_ref " + "from llx_product " + "where rowid=%s"
    #         )
    #         r = cur.mogrify(query, [int(id)])
    #         logger.debug(r)
    #         cur.execute(r)
    #         if cur.rowcount > 0:
    #             result: Dict[Any, Any] = cur.fetchone()
    #             cur.close()
    #             logger.debug(f"Found row for {id}")
    #         else:
    #             print("Got no rows from postgresql")
    #             return None
    #
    #         return result
    #     else:
    #         raise ValueError("inventory id was 0")

    # def get_inventory(id: int = 0) -> Dict[Any, Any]:
    #     logger = logging.getLogger(__name__)
    #     if id != 0:
    #         # Get fk_multicurrency
    #         self.connect()
    #         # Create a cursor object
    #         cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #         # Delete and insert
    #         query = sql.SQL(
    #             "select date_inventory, status, "
    #             + "date_validation, title, external_ref "
    #             + "from llx_inventory "
    #             + "where rowid=%s"
    #         )
    #         r = cur.mogrify(query, [int(id)])
    #         logger.debug(r)
    #         cur.execute(r)
    #         if cur.rowcount > 0:
    #             result = cur.fetchone()
    #             cur.close()
    #             logger.debug(f"Found row for {id}")
    #         else:
    #             print("Got no rows from postgresql")
    #             return {}
    #
    #         return result
    #     else:
    #         raise ValueError("inventory id was 0")

    # def get_inventory_lines(inventory_id) -> List:
    #     logger = logging.getLogger(__name__)
    #     # Get fk_multicurrency
    #     self.connect()
    #     # Create a cursor object
    #     cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #     # Delete and insert
    #     query = sql.SQL(
    #         "select rowid, fk_product, qty_stock, qty_regulated "
    #         + "from llx_inventorydet "
    #         + "where fk_inventory=%s"
    #     )
    #     r = cur.mogrify(query, [int(inventory_id)])
    #     logger.debug(r)
    #     cur.execute(r)
    #     if cur.rowcount > 0:
    #         result: List[Any] = cur.fetchall()
    #         cur.close()
    #         logger.debug(f"Found child row(s) for {inventory_id}")
    #
    #         return result
    #     else:
    #
    #         return []

    # def get_product_children(product_id):
    #     logger = logging.getLogger(__name__)
    #     # Get fk_multicurrency
    #     self.connect()
    #     # Create a cursor object
    #     cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #     # Delete and insert
    #     query = sql.SQL(
    #         "select distinct fk_product_fils,qty "
    #         + "from llx_product_association "
    #         + "where incdec='1' and fk_product_pere=%s"
    #     )
    #     r = cur.mogrify(query, [int(product_id)])
    #     logger.debug(r)
    #     cur.execute(r)
    #     if cur.rowcount > 0:
    #         result = cur.fetchall()
    #         cur.close()
    #         logger.debug(f"Found child product(s) for {product_id}")
    #     else:
    #         return None
    #
    #     return result

    # def get_stock_movements_by_fk_origin(fk_origin):
    #     logger = logging.getLogger(__name__)
    #     self.connect()
    #     # Create a cursor object
    #     cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #     query = sql.SQL(
    #         "SELECT "
    #         + "public.llx_product.rowid as id"
    #         + ",public.llx_product.stock as total_stock"
    #         + ",public.llx_product.label"
    #         + ",public.llx_stock_mouvement.rowid as movement_id"
    #         + ",public.llx_stock_mouvement.value as transfer_value"
    #         + ",public.llx_stock_mouvement.label as order_label "
    #         + "FROM "
    #         + "public.llx_stock_mouvement "
    #         + "JOIN public.llx_product "
    #         + "ON llx_product.rowid=llx_stock_mouvement.fk_product "
    #         + "WHERE "
    #         + "fk_origin=%s and origintype='order_supplier' "
    #     )
    #     r = cur.mogrify(query, [fk_origin])
    #     cur.execute(r)
    #     logger.debug(r)
    #     if cur.rowcount > 0:
    #         results = cur.fetchall()
    #         cur.close()
    #
    #         return results
    #     else:
    #         cur.close()
    #
    #         return None

    # def get_product_categories_with_ref_ext(product_id):
    #     logger = logging.getLogger(__name__)
    #     self.connect()
    #     # Create a cursor object
    #     cur = self.connection.cursor()
    #     query = sql.SQL(
    #         "SELECT fk_categorie FROM "
    #         + "public.llx_categorie_product WHERE "
    #         + "fk_product = %s"
    #     )
    #     r = cur.mogrify(query, [product_id])
    #     cur.execute(r)
    #     logger.debug(r)
    #     if cur.rowcount > 0:
    #         result = cur.fetchall()
    #         if len(result) > 0:
    #             # collect ref_ext
    #             ref_ext = []
    #             for item in result:
    #                 category_id = item[0]
    #                 query = sql.SQL(
    #                     "SELECT ref_ext FROM "
    #                     + "public.llx_categorie WHERE "
    #                     + "rowid = %s "
    #                     + "and ref_ext IS NOT NULL"
    #                 )
    #                 r = cur.mogrify(query, [category_id])
    #                 cur.execute(r)
    #                 logger.debug(r)
    #                 if cur.rowcount > 0:
    #                     logger.debug("Tradera category " + "found in database")
    #                     result = cur.fetchone()
    #                     ref_ext.append(result[0])
    #             cur.close()
    #
    #             return ref_ext
    #         else:
    #             return None
    #     else:
    #         logger.debug("No ref_ext not found in database for this product")
    #         cur.close()
    #
    #         return None

    # def get_category_id_by_ref_ext(ref_ext):
    #     logger = logging.getLogger(__name__)
    #     self.connect()
    #     # Create a cursor object
    #     cur = self.connection.cursor()
    #     query = sql.SQL(
    #         "SELECT rowid FROM " + "public.llx_categorie WHERE " + "ref_ext = %s"
    #     )
    #     r = cur.mogrify(query, [ref_ext])
    #     cur.execute(r)
    #     logger.debug(r)
    #     if cur.rowcount > 0:
    #         print("ref_ext found in database")
    #         result = cur.fetchall()
    #         cur.close()
    #
    #         return result
    #     else:
    #         print("ref_ext not found in database")
    #         cur.close()
    #
    #         return None
