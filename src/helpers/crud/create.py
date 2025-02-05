"""This should only be imported locally in DolibarrProduct"""
import logging
from datetime import datetime
from typing import TYPE_CHECKING, Union

import psycopg2  # type: ignore
from psycopg2 import extras, sql  # type: ignore

import config
from src.helpers.crud.postgres import Postgres
from src.helpers.crud.read import Read
from src.helpers.utilities import vat_rate_to_float_multiplier
from src.models.dolibarr.enums import (
    Currency,
    DolibarrTable,
    StockType,
)
from src.models.dolibarr.supplier.order import DolibarrSupplierOrder
from src.models.dolibarr.supplier.order_line import DolibarrSupplierOrderLine
from src.models.exceptions import DeprecatedMethodError, MissingInformationError

if TYPE_CHECKING:
    from src.models.dolibarr.product import DolibarrProduct

logger = logging.getLogger(__name__)


class Create(Postgres):
    # @staticmethod
    # def insert_category(parent, label, ref_ext, desc):
    #     if config.deprecate_database_methods:
    #         raise DeprecatedMethod()
    #     # Check if ref_ext is already inserted from before
    #     self.connect()
    #     # Create a cursor object
    #     cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #     query = sql.SQL(
    #         "SELECT rowid,label FROM " + "public.llx_categorie " + "WHERE ref_ext=%s"
    #     )
    #     r = cur.mogrify(query, [ref_ext])
    #     logger.debug(r)
    #     cur.execute(r)
    #     if cur.rowcount > 0:
    #         # already exit - update the label
    #         result = cur.fetchone()
    #         logger.debug(result)
    #         print(f"Updating existing label: {result[1]}")
    #         cur = self.connection.cursor()
    #         query = sql.SQL(
    #             "UPDATE public.llx_categorie "
    #             + "SET tms=now(),label=%s "
    #             + "WHERE rowid=%s"
    #         )
    #         r = cur.mogrify(
    #             query,
    #             (
    #                 label,
    #                 result[0],
    #             ),
    #         )
    #         logger.debug(r)
    #         cur.execute(r)
    #         cur.close()
    #         try:
    #             self.connection.commit()
    #         except ConnectionError:
    #             print("Could not commit to db")
    #         print("Category added.")
    #
    #     else:
    #         # Insert new
    #         print(f"Inserting new category with label: {label}")
    #         self.connect()
    #         cur = self.connection.cursor()
    #         query = sql.SQL(
    #             "INSERT INTO public.llx_categorie "
    #             + "(date_creation,tms,fk_parent,label,"
    #             + "ref_ext,description,"
    #             + "fk_user_creat,type,visible) "
    #             + "VALUES (now(),now(),%s,%s,%s,%s,1,0,0)"
    #         )
    #         r = cur.mogrify(query, (parent, label, ref_ext, desc))
    #         logger.debug(r)
    #         cur.execute(r)
    #         cur.close()
    #         try:
    #             self.connection.commit()
    #         except ConnectionError:
    #             print("Could not commit to db")
    #         print("Category added.")
    #

    def insert_extrafield(
        self,
        table: DolibarrTable,
        dolibarr_id: int,
        extrafield: str,
        value: Union[str, int, float],
    ):
        if config.deprecate_database_methods:
            raise DeprecatedMethodError()
        """Set an extrafield
        if value is True it will be converted to true in the database"""
        # product is called product
        self.connect()
        # Create a cursor object
        cur = self.connection.cursor()
        query = sql.SQL(
            "UPDATE public.llx_"
            + str(table.value)
            + "_extrafields "
            + "SET "
            + extrafield
            + "=%s, tms=now() "
            + "WHERE fk_object=%s"
        )
        r = cur.mogrify(query, (value, dolibarr_id))
        logger.debug(r)
        cur.execute(r)
        row = cur.rowcount
        logger.debug(row)
        cur.close()
        try:
            self.connection.commit()
        except ConnectionError:
            print("Could not commit to db")
        logging.info(f"{extrafield} updated")
        if row == 0:
            self.connect()
            # Create a cursor object
            cur = self.connection.cursor()
            # No row found from earlier that we could update. Insert one.
            query = sql.SQL(
                "INSERT INTO public.llx_"
                + str(table.value)
                + "_extrafields "
                + "(fk_object, tms, "
                + extrafield
                + ") "
                + "VALUES (%s,now(),%s)"
            )
            r = cur.mogrify(query, (dolibarr_id, value))
            logger.debug(r)
            cur.execute(r)
            cur.close()
            try:
                self.connection.commit()
            except ConnectionError:
                print("Could not commit to db")
            logging.info(f"{extrafield} added.")

    def insert_extrafield_date(
        self, table: DolibarrTable, dolibarr_id: int, extrafield: str, date: datetime
    ):
        if config.deprecate_database_methods:
            raise DeprecatedMethodError()
        logger.debug(f"Got type {type(date)}, {date}")
        # product is called product
        self.connect()
        # Create a cursor object
        cur = self.connection.cursor()
        query = sql.SQL(
            "UPDATE public.llx_"
            + str(table.value)
            + "_extrafields "
            + "SET "
            + extrafield
            + "=%s, tms=now() "
            + "WHERE fk_object=%s"
        )
        r = cur.mogrify(query, (date, dolibarr_id))
        logger.debug(r)
        cur.execute(r)
        row = cur.rowcount
        logger.debug(cur.rowcount)
        cur.close()
        try:
            self.connection.commit()
        except ConnectionError:
            print("Could not commit to db")
        logging.info(f"{extrafield} updated")
        if row == 0:
            self.connect()
            # Create a cursor object
            cur = self.connection.cursor()
            # No row found from earlier that we could update. Insert one.
            query = sql.SQL(
                "INSERT INTO public.llx_"
                + str(table.value)
                + "_extrafields "
                + "(fk_object, tms, "
                + extrafield
                + ") "
                + "VALUES (%s,now(),%s)"
            )
            r = cur.mogrify(query, (dolibarr_id, date))
            logger.debug(r)
            cur.execute(r)
            cur.close()
            try:
                self.connection.commit()
            except ConnectionError:
                print("Could not commit to db")
            logging.info(f"{extrafield} added.")

    # TODO use enum for extrafields
    def insert_extrafield_date_now(
        self, table: DolibarrTable, dolibarr_id: int, extrafield: str
    ):
        if config.deprecate_database_methods:
            raise DeprecatedMethodError()
        """Set an extrafield
        if value is True it will be converted to true in the database"""
        self.connect()
        # Create a cursor object
        cur = self.connection.cursor()
        query = sql.SQL(
            "UPDATE public.llx_"
            + str(table.value)
            + "_extrafields "
            + "SET "
            + extrafield
            + "=now(), tms=now() "
            + "WHERE fk_object=%s"
        )
        # https://zetcode.com/python/psycopg2/
        r = cur.mogrify(query, (dolibarr_id,))
        logger.debug(r)
        cur.execute(r)
        row = cur.rowcount
        logger.debug(cur.rowcount)
        cur.close()
        try:
            self.connection.commit()
        except ConnectionError:
            print("Could not commit to db")
        logging.info(f"{extrafield} updated")
        if row == 0:
            self.connect()
            # Create a cursor object
            cur = self.connection.cursor()
            # No row found from earlier that we could update. Insert one.
            query = sql.SQL(
                "INSERT INTO public.llx_"
                + str(table.value)
                + "_extrafields "
                + "(fk_object, tms, "
                + extrafield
                + ") "
                + "VALUES (%s,now(),now())"
            )
            # https://zetcode.com/python/psycopg2/
            r = cur.mogrify(query, (dolibarr_id,))
            logger.debug(r)
            cur.execute(r)
            cur.close()
            try:
                self.connection.commit()
            except ConnectionError:
                print("Could not commit to db")
            logging.info(f"{extrafield} added.")

    # @staticmethod
    # def insert_dispatch_shipment(order_id: int):
    #     if config.deprecate_database_methods:
    #         raise DeprecatedMethod()
    #     """Insert dispatch shipment
    #     param: take ORDER_ID
    #     return: nothing
    #     """
    #
    #     # disable because it is not ready for production
    #     raise NotImplementedError("FIXME insert_dispatch_shipment() is not finished")
    #     # TODO is there not an API endpoint for this?
    #     # 1) Insert supplier shipment received line
    #     # 2) Insert stock_mouvement line
    #     # 3) Increase stock-column in product
    #     # 4) Calculate pmp (only based on this shipment) unitprice/quantity and
    #     #    insert into product.
    #     # order_lines = get_supplier_order_lines_or_exit(order_id)
    #     # # pseudo code
    #     # for line in order_lines:
    #     #     label = line["product_label"]
    #     #     answer = yes_no_question("Did you receive all of {label}")
    #     #     #  what happens if it is true? how do we get the right number?
    #     #     if answer is False:
    #     #         answer = yes_no_question("Did you receive 0 of {label}")
    #     #         if answer is False:
    #     #             answer = ask_mandatory("int", "Quantity received")
    #     #     if helpers.config.debug:
    #     #         print(answer)
    #     #     # do something with this answer
    #     #     fk_commande = order_id
    #     #     fk_product = line["fk_product"]
    #     #     fk_commandefourndet = line["id"]
    #     #     quantity = answer
    #     #     fk_entrepot = 1       # we only support 1 warehouse
    #     #     fk_user = 1
    #     #     comment = f"Receiving purchase order {order_id}"
    #     #     status = 1            # what does this do?
    #
    #     #     # Insert supplier shipment received line
    #     #     connection = helpers.crud.postgresql.db_connect()
    #     #     cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #     #     query = sql.SQL("INSERT INTO " +
    #     #                     "public.llx_commande_fournisseur_dispatch " +
    #     #                     "(datec,tms," +
    #     #                     "fk_commande," +
    #     #                     "fk_product," +
    #     #                     "fk_commandefourndet," +
    #     #                     "qty," +
    #     #                     "fk_entrepot," +
    #     #                     "fk_user," +
    #     #                     "comment," +
    #     #                     "status,"
    #     #                     "VALUES (now(),now(),%s,%s,%s,%s," +
    #     #                     "%s,%s,%s,%s)")
    #     #     r = cur.mogrify(query, (
    #     #         fk_commande,
    #     #         fk_product,
    #     #         fk_commandefourndet,
    #     #         quantity,
    #     #         fk_entrepot,
    #     #         fk_user,
    #     #         comment,
    #     #         status,
    #     #     ))
    #     #     if helpers.config.debug:
    #     #         print(r)
    #     #     #cur.execute(r)
    #     #     cur.close()
    #     #     try:
    #     #         connection.commit()
    #     #     except ConnectionError:
    #     #         print("Could not commit to db")
    #     #         exit(1)
    #     #     print("Inserted supplier shipment received line")

    def insert_link(
        self,
        fk_source: int,
        source_table: DolibarrTable,
        fk_target: int,
        target_table: DolibarrTable,
    ):
        if config.deprecate_database_methods:
            raise DeprecatedMethodError()
        # protect against duplicates?
        self.connect()
        # Create a cursor object
        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = sql.SQL(
            "INSERT INTO public.llx_element_element "
            + "(fk_source,sourcetype,fk_target,targettype) "
            + "VALUES (%s,%s,%s,%s)"
        )
        r = cur.mogrify(
            query, [fk_source, source_table.value, fk_target, target_table.value]
        )
        logger.debug(r)
        cur.execute(r)
        cur.close()
        try:
            self.connection.commit()
        except ConnectionError:
            print("Could not commit to db")
        print("Link inserted")

    def insert_multiprice(self, product: "DolibarrProduct"):
        if config.deprecate_database_methods:
            raise DeprecatedMethodError()
        if not product.sales_vat_rate:
            raise MissingInformationError("product.vatrate is None")
        multiplier = vat_rate_to_float_multiplier(product.sales_vat_rate)
        self.connect()
        # Create a cursor object
        cur = self.connection.cursor()
        query = sql.SQL(
            "INSERT INTO public.llx_product_price "
            + "(fk_product, price, price_ttc, tva_tx, "
            + "date_price, price_base_type, price_level,"
            + "fk_user_author) "
            + "VALUES (%s,%s,%s,%s,now(),'TTC',%s,1)"
        )
        # exec for each pricelevel:
        multiprice1 = cur.mogrify(
            query,
            (
                product.id,
                product.multiprice1,
                product.multiprice1 * multiplier,
                product.sales_vat_rate.value,
                1,
            ),
        )
        logger.debug(multiprice1)
        cur.execute(multiprice1)
        multiprice2 = cur.mogrify(
            query,
            (
                product.id,
                product.multiprice2,
                product.multiprice2 * multiplier,
                product.sales_vat_rate.value,
                2,
            ),
        )
        logger.debug(multiprice2)
        cur.execute(multiprice2)
        cur.close()
        try:
            self.connection.commit()
        except ConnectionError:
            print("Could not commit to db")
        logger.info("Multiprices added")

    def insert_product_category(
        self,
        category_id: int,
        product_id: int,
    ):
        if config.deprecate_database_methods:
            raise DeprecatedMethodError()
        self.connect()
        # Create a cursor object
        cur = self.connection.cursor()
        # Check if exist first
        query = sql.SQL(
            "SELECT * FROM public.llx_categorie_product "
            + "WHERE fk_categorie=%s AND fk_product=%s"
        )
        r = cur.mogrify(query, (category_id, product_id))
        logger.debug(r)
        cur.execute(r)
        if cur.rowcount > 0:
            print(f"The product already has category id: {category_id}.")
        else:
            query = sql.SQL(
                "INSERT INTO public.llx_categorie_product "
                + "(fk_categorie, fk_product) VALUES (%s,%s)"
            )
            r = cur.mogrify(query, (category_id, product_id))
            logger.debug(r)
            cur.execute(r)
            try:
                self.connection.commit()
            except ConnectionError:
                print("Could not commit to db")
            print(
                f"Category added, see {self.__base_url}"
                + "categories/viewcat.php?id="
                + f"{category_id}&type=0"
            )
        cur.close()

    # @staticmethod
    # def insert_revert_stock_movement(rowid: int, total_stock: int):
    #     if config.deprecate_database_methods:
    #         raise DeprecatedMethod()
    #     """Completely revert a received shipment by decreasing the stock and
    #     inserting a revert movement line for every original movement line"""
    #
    #     # Get the row contents
    #     self.connect()
    #     cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #     query = sql.SQL(
    #         "SELECT * FROM public.llx_stock_mouvement " + "WHERE rowid = %s"
    #     )
    #     r = cur.mogrify(query, [rowid])
    #     logger.debug(r)
    #     cur.execute(r)
    #     if cur.rowcount > 0:
    #         # Insert reverted line
    #         result = cur.fetchone()
    #         logger.debug(result)
    #         transfer_value = result["value"] * -1
    #         fk_product = result["fk_product"]
    #         query = sql.SQL(
    #             "INSERT INTO public.llx_stock_mouvement "
    #             + "(datem,tms,fk_product,fk_entrepot"
    #             + ",value,price,type_mouvement,fk_user_author"
    #             + ",label,fk_origin,origintype,fk_projet) "
    #             "VALUES " + "(now(),now(),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    #         )
    #         r = cur.mogrify(
    #             query,
    #             (
    #                 fk_product,
    #                 result["fk_entrepot"],
    #                 transfer_value,
    #                 result["price"],
    #                 2,
    #                 result["fk_user_author"],
    #                 "Revert via Python of: " + result["label"],
    #                 result["fk_origin"],
    #                 result["origintype"],
    #                 result["fk_projet"],
    #             ),
    #         )
    #         logger.debug(r)
    #         cur.execute(r)
    #         cur.close()
    #         try:
    #             self.connection.commit()
    #         except ConnectionError:
    #             print("Could not commit to db")
    #         print("Inserted revert stock movement line")
    #
    #         # Update llx_product also
    #         cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #         query = sql.SQL(
    #             "UPDATE public.llx_product " + "SET stock=%s " + "WHERE rowid=%s"
    #         )
    #         # We add the negative transfer value to subtract from the total.
    #         r = cur.mogrify(query, [total_stock + transfer_value, fk_product])
    #         logger.debug(r)
    #         cur.execute(r)
    #         cur.close()
    #         try:
    #             self.connection.commit()
    #         except ConnectionError:
    #             print("Could not commit to db")
    #         print("Product stock column updated.")
    #
    #     else:
    #         print("Error. No such rowid. Exit.")
    #
    #         sys.exit(1)

    def insert_supplier_order_line(
        self,
        line: DolibarrSupplierOrderLine,
        order: DolibarrSupplierOrder,
    ):
        if config.deprecate_database_methods:
            raise DeprecatedMethodError()
        # switch to named parameters and OOP
        """
        param: QUANTITY is quantity
        param: VAT_SRC_CODE is referring to the dictionary setup and needed
        in Sweden for putting import VAT on special accounts and reporting them
        separately.
        """
        if config.loglevel == logging.DEBUG:
            logger.debug("Inserting line:")
            print(line.model_dump())
        if not order.supplier_order:
            raise MissingInformationError("order.supplier_order was None")
        if not line.product:
            raise MissingInformationError("line.product was None")
        from src.models.dolibarr.product import DolibarrProduct

        if not isinstance(line.product, DolibarrProduct):
            raise MissingInformationError("line.product was None")
        if not line.product.type:
            # print(line.product.dict())
            raise MissingInformationError("line product has no type.")
        if not line.product.array_options.get("options_external_ref"):
            if line.product.type == StockType.SERVICE:
                line.product.array_options["options_external_ref"] = ""
            else:
                raise MissingInformationError(
                    f"line.product.external_ref was None for {line.product.label}"
                )
        if not line.product.purchase_vat_rate:
            raise MissingInformationError(
                "line product {line.product.label} has no purchase vat rate"
            )
        if line.product.currency == Currency.EUR and not line.multicurrency_total_ht:
            raise MissingInformationError(
                f"line.multicurrency_total_ht was None for {line.product.label}"
            )
        # Extract data
        # Get purchase data from product (this should be in the OOP object)
        if not line.product.multicurrency_cost_price and not line.product.cost_price:
            raise ValueError(
                "Error prices could not be found automatically "
                + f"for line with this product: {line.product.url()}"
                + ". Please fix"
            )
        if order.supplier_order.dolibarr_supplier:
            read = Read()
            dolibarr_currency_id = read.get_currency_id(
                order.supplier_order.dolibarr_supplier.currency
            )
        else:
            raise MissingInformationError(
                "order.supplier_order.dolibarr_supplier.currency was None"
            )
        if not order.supplier_order.dolibarr_supplier.vat_rate:
            raise MissingInformationError(
                "order.supplier_order.dolibarr_supplier.purchase_vat_rate was None"
            )
        # Calculate prices for Dolibarr
        if not line.vat_src_code:
            line.vat_src_code = ""

        # This is just a quick db query
        # fk_multicurrency = get_fk_multicurrency(
        #     line.product.currency.value,
        # )
        self.connect()
        # Create a cursor object
        cur = self.connection.cursor()
        query = sql.SQL(
            "INSERT INTO "
            + "public.llx_commande_fournisseurdet "
            + "(fk_commande, "
            + "fk_product, "
            + "qty, "
            + "product_type, "
            + "tva_tx, "
            + "subprice,"
            + "multicurrency_subprice, "
            + "total_ttc, "
            + "total_ht,"
            + "total_tva,"
            + "multicurrency_total_ttc,"
            + "multicurrency_total_ht, "
            + "fk_multicurrency,"
            + "multicurrency_code,"
            + "ref,"
            + "vat_src_code) "
            + "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        )
        r = cur.mogrify(
            query,
            (
                order.id,
                line.product.id,
                line.quantity,
                line.product.type.value,
                order.supplier_order.dolibarr_supplier.vat_rate.value,
                line.product.cost_price,
                line.product.multicurrency_cost_price,
                line.total_ttc,
                line.total_ht,
                line.total_tva,
                line.multicurrency_total_ttc,
                line.multicurrency_total_ht,
                dolibarr_currency_id,
                order.supplier_order.dolibarr_supplier.currency.value,
                line.product.external_ref,
                line.vat_src_code,
            ),
        )
        logger.debug(r)
        cur.execute(r)
        try:
            self.connection.commit()
        except ConnectionError:
            print("Could not commit to db")
        print(f"Supplier line with {line.quantity} pcs. of {line.product.label} added")
