import logging
from typing import Any, List

from config.enums import PaymentSource
from src.models.dolibarr.product import DolibarrProduct
from src.models.supplier.order import SupplierOrder
from src.models.suppliers.biltema.order_row import BiltemaOrderRow
from src.models.suppliers.enums import SupplierBaseUrl, SupportedSupplier
from src.views.dolibarr.product import DolibarrProductView
from src.views.my_base_view import MyBaseView

logger = logging.getLogger(__name__)


class BiltemaOrder(SupplierOrder, MyBaseView):
    """MyBaseView is needed for the ask_mandatory and ask_date methods"""

    base_url: SupplierBaseUrl = SupplierBaseUrl.BILTEMA
    codename: SupportedSupplier = SupportedSupplier.BILTEMA
    insert_payment: bool = True
    apply_freight: bool = False
    reference: str = ""  # We don't have references for Biltema orders
    credit_days: int = 0
    invoice_delay: int = 0

    @property
    def url(self):
        """N/A"""
        return ""

    @staticmethod
    def __ask_quantity_default_one():
        answer = input("How many of these? [1]:")
        if answer == "" or answer is None:
            return 1
        else:
            return int(answer)

    def __get_existing_product__(self, ref: str) -> Any:  # "DolibarrProduct"|None
        # get it if it already exists
        p = DolibarrProduct(api=self.api)
        if "-" not in ref:
            raise ValueError(f"missing '-' in ref: {ref}")
        return p.get_by_external_ref(codename=self.codename, external_ref=ref)

    def __get_order_row__(self, ref: str) -> BiltemaOrderRow:
        from src.models.suppliers.biltema import BiltemaProduct

        # DISABLED we only store friendly refs right now
        # remove dash before lookup because we no longer store the friendly refs
        # product = p.get_by_external_ref(
        #     codename=self.codename, external_ref=ref.replace("-", "")
        # )
        product = self.__get_existing_product__(ref=ref)
        if product is not None:
            logger.info(f"Found product {product.label}, see {product.url}")
            biltema_product = BiltemaProduct(sku=ref)
            biltema_product.scrape_product()
            return BiltemaOrderRow(
                entity=biltema_product,
            )
        else:
            logger.info(f"Importing {ref}")
            biltema_product = BiltemaProduct(sku=ref)
            biltema_product.scrape_product()
            from src.models.dolibarr.product import DolibarrProduct

            p = DolibarrProductView(supplier_product=biltema_product)
            p.create_from_supplier_product()
            return BiltemaOrderRow(
                entity=biltema_product,
            )

    def import_purchase(self, refs: List[str]):
        """Imports the purchase from Biltema

        First we create a BiltemaOrder object with all the products
        Then we feed it as usual to DolibarrOrder which takes care
        of the rest"""

        logger.debug("import_purchase: running")
        print("Importing and getting products from the database")
        biltema_order: BiltemaOrder = BiltemaOrder(base_url=SupplierBaseUrl.BILTEMA)

        for ref in refs:
            biltema_order.rows.append(self.__get_order_row__(ref=ref))

        # Get quantities
        # Weird mypy error here which we ignore
        for row in biltema_order.rows:  # type: ignore
            logger.debug(row)
            logger.debug(row.entity)
            print(row.entity.label)
            quantity = self.__ask_quantity_default_one()
            row.quantity = quantity
        # check 0
        for row in biltema_order.rows:
            if row.quantity == 0:
                raise ValueError(
                    f"quantity of row with product: {row.entity.label} was 0"
                )
        # Import order
        biltema_order.reference = self.ask_mandatory(
            text="Order ref (describe what was bought):"
        )
        biltema_order.order_date = self.ask_date("order")

        biltema_order.payment_source = PaymentSource.OWNERS_INSERT
        biltema_order.import_order()
        # todo invoice
