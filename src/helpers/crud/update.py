import logging
import math
from datetime import datetime
from typing import TYPE_CHECKING

import psycopg2  # type: ignore
from psycopg2 import extras, sql  # type: ignore

import config
from src.helpers.crud.postgres import Postgres
from src.models.basemodels.my_base_model import MyBaseModel
from src.models.exceptions import DeprecatedMethodError, MissingInformationError

if TYPE_CHECKING:
    from src.models.dolibarr.supplier.order import DolibarrSupplierOrder
    from src.models.dolibarr.supplier.order_line import DolibarrSupplierOrderLine

logger = logging.getLogger(__name__)


class Update(Postgres):
    #  special typing because of pydantic
    def update_supplier_order_to_approved_and_made(
        self, order: "DolibarrSupplierOrder"
    ):
        if config.deprecate_database_methods:
            raise DeprecatedMethodError()
        """Update supplier order to approved status
        param: order_date is a datetime object
        param: delivery_date is a datetime object
        fk_statut:
        0 = draft
        1 = validated
        2 = approved
        3 = order made
        4 = partially received
        5 = fully received
        """
        self.connect()
        # TODO open a ticket for this to be supported in the API
        from src.models.dolibarr.supplier.order import DolibarrSupplierOrder

        if not isinstance(order, DolibarrSupplierOrder):
            raise ValueError("not a DolibarrSupplierOrder")

        # Check if order is validated
        if order and not order.validated:
            raise ValueError("Please validate the order first.")
        if not order.order_date:
            # Default to now, because with e.g. Jofrab we don't know.
            order_date_iso = datetime.now(tz=MyBaseModel().stockholm_timezone).strftime(
                "%Y-%m-%d"
            )
        else:
            # assuming datetime object
            order_date_iso = order.order_date.strftime("%Y-%m-%d")
        # delivery_date_iso = None
        if not order.delivery_date:
            # Default to now.
            logger.debug("Defaulting to delivery date today")
            delivery_date_iso = datetime.now(
                tz=MyBaseModel().stockholm_timezone
            ).strftime("%Y-%m-%d")
        else:
            logger.debug("Got delivery date from order")
            # assuming datetime object
            delivery_date_iso = order.delivery_date.strftime("%Y-%m-%d")
        # Insert the data
        self.connect()
        # Create a cursor object
        cur = self.connection.cursor()
        query = sql.SQL(
            "UPDATE public.llx_commande_fournisseur "
            + "SET date_approve=%s, "
            + "date_commande=%s, "
            + "date_livraison=%s, "
            + "fk_statut=%s, "
            "fk_input_method=%s " + "WHERE rowid=%s"
        )
        r = cur.mogrify(
            query,
            [
                order_date_iso,
                order_date_iso,
                delivery_date_iso,
                3,
                5,
                order.id,
            ],
        )
        logger.debug(r)
        cur.execute(r)
        try:
            self.connection.commit()
        except ConnectionError:
            print("Could not commit to db")
        print("Supplier order updated")

    # def update_invoice_prices(invoice_id: int):
    #     conn = postgresql.db_connect()
    #     # Create a cursor object
    #     cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #     # sum lines
    #     query = sql.SQL(
    #         "SELECT SUM(total_ttc) as total_ttc, "
    #         + "SUM(total_ht) as total_ht,"
    #         + "SUM(multicurrency_total_ttc) as multicurrency_total_ttc, "
    #         + "SUM(multicurrency_total_ht) as multicurrency_total_ht "
    #         + "FROM "
    #         + "public.llx_facture_fourn_det "
    #         + "WHERE fk_facture_fourn=%s and qty > 0"
    #     )
    #     r = cur.mogrify(query, [invoice_id])
    #     logger.debug(r)
    #     cur.execute(r)
    #     r = cur.fetchone()
    #     total_ht = str(round(float(r["total_ht"]), 2))
    #     total_ttc = str(round(float(r["total_ttc"]), 2))
    #     multicurrency_total_ht = str(round(float(r["multicurrency_total_ttc"]), 2))
    #     multicurrency_total_ttc = str(round(float(r["multicurrency_total_ht"]), 2))
    #     print(f"Total excl. tax: {total_ht}")
    #     print(f"Total incl. tax: {total_ttc}")
    #     print(f"Total excl. tax (currency): {multicurrency_total_ht}")
    #     print(f"Total incl. tax (currency): {multicurrency_total_ttc}")
    #     # update with the result
    #     query = sql.SQL(
    #         "UPDATE public.llx_facture_fourn "
    #         + "SET total_ttc=%s, total_ht=%s,"
    #         + "multicurrency_total_ttc=%s,"
    #         + "multicurrency_total_ht=%s"
    #         + "WHERE rowid=%s"
    #     )
    #     r = cur.mogrify(
    #         query,
    #         [
    #             total_ttc,
    #             total_ht,
    #             multicurrency_total_ttc,
    #             multicurrency_total_ht,
    #             invoice_id,
    #         ],
    #     )
    #     logger.debug(r)
    #     cur.execute(r)
    #     try:
    #         self.connection.commit()
    #     except ConnectionError:
    #         print("Could not commit to db")
    #     print("Supplier invoice totals updated")
    #
    #     # Fix line totals
    #     query = sql.SQL(
    #         "UPDATE public.llx_facture_fourn_det "
    #         + "SET total_ttc=0, total_ht=0,"
    #         + "multicurrency_total_ttc=0,"
    #         + "multicurrency_total_ht=0 "
    #         + "WHERE fk_facture_fourn=%s AND qty=0"
    #     )
    #     r = cur.mogrify(
    #         query,
    #         [
    #             invoice_id,
    #         ],
    #     )
    #     logger.debug(r)
    #     cur.execute(r)
    #     try:
    #         self.connection.commit()
    #     except ConnectionError:
    #         print("Could not commit to db")
    #     print("Supplier invoice lines totals updated")
    #     cur.close()
    #     postgresql.db_disconnect(conn)

    #  special typing because of pydantic
    def update_order_totals(self, order: "DolibarrSupplierOrder"):
        if config.deprecate_database_methods:
            raise DeprecatedMethodError()
        self.connect()
        from src.models.dolibarr.supplier.order import DolibarrSupplierOrder

        if not order.supplier_order:
            raise MissingInformationError("order.supplier_order was None")
        if not isinstance(order, DolibarrSupplierOrder):
            raise ValueError("not a DolibarrSupplierOrder")
        # Create a cursor object
        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # sum lines
        query = sql.SQL(
            "SELECT SUM(total_ttc) as total_ttc, "
            + "SUM(total_ht) as total_ht,"
            + "SUM(total_tva) as total_tva,"
            + "SUM(multicurrency_total_ttc) as multicurrency_total_ttc, "
            + "SUM(multicurrency_total_ht) as multicurrency_total_ht "
            + "FROM "
            + "public.llx_commande_fournisseurdet "
            + "WHERE fk_commande=%s"
        )
        cur.execute(query, [order.id])
        r = cur.fetchone()
        total_ht = str(int(r["total_ht"]))
        if order.supplier_order.round_up_on_order_total:
            sum_before = r["total_ttc"]
            total_ttc = str(math.ceil(sum_before))
            logger.debug(f"Rounding up order total from {sum_before} to {total_ttc}")
        else:
            total_ttc = str(int(r["total_ttc"]))
        total_tva = str(int(r["total_tva"]))
        multicurrency_total_ht = str(int(r["multicurrency_total_ttc"]))
        multicurrency_total_ttc = str(int(r["multicurrency_total_ht"]))
        print(f"Total excl. tax: {total_ht}")
        print(f"Total incl. tax: {total_ttc}")
        print(f"Total tax: {total_tva}")
        print(f"Total excl. tax (currency): {multicurrency_total_ht}")
        print(f"Total incl. tax (currency): {multicurrency_total_ttc}")
        # update order with the result
        query = sql.SQL(
            "UPDATE public.llx_commande_fournisseur "
            + "SET total_ttc=%s, total_ht=%s,"
            + "total_tva=%s,"
            + "multicurrency_total_ttc=%s,"
            + "multicurrency_total_ht=%s"
            + "WHERE rowid=%s"
        )
        r = cur.mogrify(
            query,
            [
                total_ttc,
                total_ht,
                total_tva,
                multicurrency_total_ttc,
                multicurrency_total_ht,
                order.id,
            ],
        )
        cur.execute(r)
        try:
            self.connection.commit()
        except ConnectionError:
            print("Could not commit to db")
        logger.info("Supplier order totals updated")
        cur.close()

    #  disabled because pydantic does not seem to support future annotations
    def update_vat_src_code_on_supplier_invoice_line(
        self,
        line: "DolibarrSupplierOrderLine",
    ):
        if config.deprecate_database_methods:
            raise DeprecatedMethodError()
        from src.models.dolibarr.supplier.order_line import DolibarrSupplierOrderLine

        if not isinstance(line, DolibarrSupplierOrderLine):
            raise ValueError("not a DolibarrSupplierOrderLine")
        self.connect()
        # Create a cursor object
        cur = self.connection.cursor()
        query = sql.SQL(
            "UPDATE public.llx_facture_fourn_det "
            + "SET vat_src_code=%s "
            + "WHERE rowid=%s"
        )
        r = cur.mogrify(query, [line.vat_src_code, line.id])
        logger.debug(r)
        cur.execute(r)
        cur.close()
        try:
            self.connectioncommit()
        except ConnectionError:
            logger.exception("Could not commit to db")
            logger.exception("vat_src_code updated on supplier invoice line")
