import logging

import config
from src.controllers.my_base_contr import MyBaseContr
from src.helpers import utilities
from src.models.dolibarr import DolibarrEndpoint
from src.models.dolibarr.enums import (
    DolibarrEndpointAction,
    DolibarrTable,
    Expired,
    PriceBaseType,
    Status,
)
from src.models.dolibarr.product import DolibarrProduct
from src.models.exceptions import MissingInformationError
from src.models.suppliers.enums import EUR_suppliers, SupportedSupplier

logger = logging.getLogger(__name__)


class DolibarrProductContr(MyBaseContr, DolibarrProduct):
    """This class contains all the logic that manipulate data about products in Dolibarr"""

    # Optional
    sku: str = ""
    ean: str = ""

    def __create_product_and_add_prices_and_extrafields__(self):
        """Create product in Dolibarr"""
        data = dict(
            ref=self.supplier_product.generated_dolibarr_ref,
            cost_price=self.supplier_product.cost_price,
            label=self.supplier_product.label,
            status=self.status_sell.value,
            status_buy=self.status_buy.value,
            accountancy_code_sell=self.accountancy_code_sell,
            accountancy_code_buy=self.accountancy_code_buy,
            description=self.supplier_product.description,
            tva_tx=self.sales_vat_rate.value,
            type=self.type.value,
            url=self.url,
            note="Inserted with Python product module",
        )
        if config.loglevel == logging.DEBUG:
            print(f"data:{data}")
        r = self.api.call_create_api(endpoint=DolibarrEndpoint.PRODUCTS, params=data)
        self.id = self.response_to_int_or_fail(r.text)
        self.__insert_extrafields__()
        if self.status_sell == Status.ENABLED:
            self.__insert_multiprices__()
        self.__insert_purchase_price__()
        print(f"Product created successfully, see {self.dolibarr_product_url}")

    # def __insert_category__(self, category_id: int = None):
    #     if category_id:
    #         if not self.id:
    #             raise MissingInformationError("self.id was None")
    #         else:
    #             self.create.insert_product_category(category_id, self.id)
    #     else:
    #         logger.warning("category_id was None. Could not insert category")

    def __insert_label_en__(self):
        if self.label_en:
            self.create.insert_extrafield(
                table=DolibarrTable.PRODUCT,
                dolibarr_id=self.id,
                extrafield="label_en",
                value=self.label_en,
            )

    # Commented out because of test failure
    # def __insert_label_de__(self):
    #     if self.label_de:
    #         self.create.insert_extrafield(
    #             table=DolibarrTable.PRODUCT,
    #             dolibarr_id=self.id,
    #             extrafield="label_de",
    #             value=self.label_de,
    #         )

    def __insert_english_and_german_labels__(self):
        self.__insert_label_en__()
        # self.__insert_label_de__()

    def __insert_codename__(self):
        if self.codename:
            self.create.insert_extrafield(
                table=DolibarrTable.PRODUCT,
                dolibarr_id=self.id,
                extrafield="main_supplier_codename",
                value=str(self.codename.value),
            )
        else:
            logger.warning("Codename is None")

    def __insert_sku__(self):
        if self.sku:
            self.create.insert_extrafield(
                table=DolibarrTable.PRODUCT,
                dolibarr_id=self.id,
                extrafield="external_ref",
                value=self.sku,
            )
        else:
            logger.warning("sku is None")

    def __insert_list_price__(self):
        if self.external_list_price:
            self.create.insert_extrafield(
                table=DolibarrTable.PRODUCT,
                dolibarr_id=self.id,
                extrafield="list_price",
                value=self.external_list_price,
            )
        else:
            logger.warning("list price is None")

    def __insert_url__(self):
        # todo migrate to built in url?
        if self.external_url:
            self.create.insert_extrafield(
                table=DolibarrTable.PRODUCT,
                dolibarr_id=self.id,
                extrafield="product_url",
                value=self.external_url,
            )
        else:
            logger.warning("No URL found for this product")

    def __insert_image_url__(self):
        if self.external_image_url:
            self.create.insert_extrafield(
                table=DolibarrTable.PRODUCT,
                dolibarr_id=self.id,
                extrafield="picture_url",
                value=self.external_image_url,
            )
        else:
            logger.warning("No image URL provided for this product")

    def __insert_latest_update__(self):

        # Update no matter what
        self.create.insert_extrafield_date_now(
            DolibarrTable.PRODUCT, dolibarr_id=self.id, extrafield="last_update"
        )

    def __insert_expired__(self):
        if self.expired:
            self.create.insert_extrafield(
                table=DolibarrTable.PRODUCT,
                dolibarr_id=self.id,
                extrafield="expired",
                value=str(self.expired.value),
            )

    def __insert_restock_date__(self):
        if self.restock_date:
            self.create.insert_extrafield_date(
                table=DolibarrTable.PRODUCT,
                dolibarr_id=self.id,
                extrafield="restock_date",
                date=self.restock_date,
            )

    def __insert_ean__(self):
        if self.ean:
            self.create.insert_extrafield(
                table=DolibarrTable.PRODUCT,
                dolibarr_id=self.id,
                extrafield="ean",
                value=self.ean,
            )

    def __insert_extrafields__(self):
        """Helper method to insert all extrafields we need"""
        self.__insert_english_and_german_labels__()
        self.__insert_codename__()
        self.__insert_sku__()
        self.__insert_list_price__()
        self.__insert_url__()
        self.__insert_image_url__()
        self.__insert_latest_update__()
        self.__insert_expired__()
        self.__insert_restock_date__()
        self.__insert_ean__()

        # Deprecated
        # if not self.work_minutes:
        #     raise ValueError("self.workminutes was None")
        # else:
        #     self.create.insert_extrafield(
        #         table=DolibarrTable.PRODUCT,
        #         dolibarr_id=self.id,
        #         extrafield="workminutes",
        #         value=self.work_minutes,
        #     )
        # Supplier data
        # if self.external_stock:
        #     self.create.insert_extrafield(
        #         table=DolibarrTable.PRODUCT,
        #         dolibarr_id=self.id,
        #         extrafield="external_stock",
        #         value=self.external_stock,
        #     )
        # Date
        # Carriers
        # if self.postnord:
        #     self.create.insert_extrafield(
        #         table=DolibarrTable.PRODUCT,
        #         dolibarr_id=self.id,
        #         extrafield="postnord",
        #         value=str(self.postnord.value),
        #     )
        # if self.schenker:
        #     self.create.insert_extrafield(
        #         table=DolibarrTable.PRODUCT,
        #         dolibarr_id=self.id,
        #         extrafield="schenker",
        #         value=str(self.schenker.value),
        #     )
        # # Integration
        # if self.sello_status:
        #     self.create.insert_extrafield(
        #         table=DolibarrTable.PRODUCT,
        #         dolibarr_id=self.id,
        #         extrafield="sello_tosell",
        #         value=str(self.sello_status.value),
        #     )
        # Legacy
        # self.create.insert_extrafield(
        #     DolibarrTable.PRODUCT, dolibarr_id=self.id, extrafield="script_created", 1,
        # )
        logger.info("Extrafields inserted/updated")

    def __insert_multiprices__(self):
        """Insert mulitprices
        This has to be enabled in Dolibarr to work"""
        logger.debug("__insert_multiprices__: Running")
        # Convert None
        if self.multiprice1 is None:
            # self.multiprice1 = 0
            raise MissingInformationError("self.multiprice1 was None")
        else:
            if self.multiprice2 is None:
                self.multiprice2 = 0
            self.create.insert_multiprice(self)

    def __check_before_inserting_purchase_price__(self):
        if not self.ref:
            raise ValueError(
                "Cannot update purchase price because "
                + f"external ref is missing. Please fix. {self.url}"
            )
        if not self.cost_price:
            raise ValueError(
                f"Cannot update purchase price because cost_price is missing, see {self.url}"
            )
        if not self.multicurrency_cost_price:
            if self.codename in EUR_suppliers:
                raise ValueError(
                    f"Cannot update purchase price because multicurrency_cost_price "
                    f"was None and it is an EUR supplier, see {self.url}"
                )
            else:
                self.multicurrency_cost_price = self.cost_price
        elif self.cost_price == 0:
            raise ValueError("Cost price was 0, please fix")
        elif self.multicurrency_cost_price == float(0):
            raise ValueError("multicurrency cost price was 0, please fix")
        if not self.currency:
            raise MissingInformationError("self.currency was None")
        if not self.purchase_vat_rate:
            raise MissingInformationError("self.purchase_vat_rate was None")

    def __insert_purchase_price__(self):
        """Insert purchase price into Dolibarr"""
        logger.debug("__insert_purchase_price__: running")
        self.__check_before_inserting_purchase_price__()
        from src.models.dolibarr.supplier import DolibarrSupplier

        supplier = DolibarrSupplier(codename=self.codename)
        supplier.update_attributes_from_dolibarr()
        if not supplier.id:
            raise ValueError("got no supplier id from dolibarr")
        # TODO write test for this once we have a test database
        if self.codename in EUR_suppliers:
            # Dolibarr wants 0.1 if the eur-sek rate is 10.
            multicurrency_rate = config.eur_sek_exchange_rate / 100
        else:
            # Else we use 1 for SEK
            multicurrency_rate = 1
        data = {
            "buyprice": self.cost_price,
            "price_base_type": PriceBaseType.NET_PRICE.value,
            "multicurrency_buyprice": self.multicurrency_cost_price,
            "multicurrency_price_base_type": PriceBaseType.NET_PRICE.value,
            "multicurrency_tx": multicurrency_rate,
            "multicurrency_code": self.currency.value,
            "tva_tx": self.purchase_vat_rate.value,
            "fourn_id": supplier.id,
            "ref_fourn": self.ref,
            "delivery_time_days": supplier.delivery_delay,
            # Dolibarr did not handle minimum_quantity correctly in V12 so we set it to
            # always 1 for now.
            "qty": 1,  # minimum_quantity
            "availability": 0,
            "import_key": "Import from script"
            # multicurrency is not supported yet
            # "multicurrency_buyprice": self.multicurrency_cost_price,
            # "multicurrency_price_base_type": "ttc",
            # "multicurrency_tx": self.currency_conversion_rate,
            # "multicurrency_code": self.currency.value
        }
        logger.debug(f"purchase_price_data:{data}")
        r = self.api.call_action_api(
            endpoint=DolibarrEndpoint.PRODUCTS,
            object_id=self.id,
            action=DolibarrEndpointAction.PURCHASE_PRICES,
            params=data,
        )
        if r.status_code == 200:
            logger.info(f"Purchase price inserted. {self.purchase_price_url}")
        else:
            raise ValueError(f"Got {r.status_code}:{r.text}")

    def __update_weight__(self):
        if not self.weight:
            raise ValueError("Weight was None")
        data = {
            "weight": self.weight,
            # gram
            "weight_units": "-3",
        }
        r = self.api.call_update_api(DolibarrEndpoint.PRODUCTS, self.id, data)
        utilities.print_result(r, "Weight added", "adding self.weight")

    def __update_purchase_price__(self):
        """The Dolibarr API does not support updating the price,
        so we remove and insert"""
        if not self.codename:
            raise MissingInformationError(f"self.codename was None, see {self.url}")
        self.delete.delete_purchase_prices(product=self)
        self.__insert_purchase_price__()

    def create_from_supplier_product(self):
        """Create a new product or product in Dolibarr
        The call_create_api returns a response object"""
        # why is this disabled?
        # if self.supplier_product.codename in EUR_suppliers:
        #     raise ValueError("EU supplier not supported yet.")
        # Setup defaults
        logger.debug("create_from_supplier_product: Running")
        from src.models.supplier.entity import SupplierEntity

        if not isinstance(self.supplier_product, SupplierEntity):
            raise ValueError("self.supplier_product not a SupplierEntity")
        if not isinstance(self.supplier_product.codename, SupportedSupplier):
            raise ValueError(
                f"self.codename '{self.codename}' " f"not a SupportedSupplier"
            )
        self.__prepare_before_creating_new_product__()
        self.__create_product_and_add_prices_and_extrafields__()
        self.__insert_extrafields__()
        if self.status_sell == Status.ENABLED:
            self.__insert_multiprices__()
        self.__insert_purchase_price__()
        print(f"Product created successfully, see {self.dolibarr_product_url}")

    # def enrich_product(self):
    #     """Update """
    #     logger = logging.getLogger(__name__)
    #     if data.get("search_url"):
    #         # Product has expired
    #         logger.info(f"Did not find the product. See {data['search_url']}")
    #         self.expired = Expired.TRUE
    #         self.status_buy = Status.DISABLED
    #     else:
    #         cost_price = data["cost_price"]
    #         if not self.cost_price:
    #             print("Cost price was None in Dolibarr")
    #         elif not cost_price:
    #             raise ValueError("cost_price from supplier was None")
    #         else:
    #             if self.cost_price > cost_price:
    #                 print(f"Cost price in Dolibarr was {self.cost_price} but " +
    #                       f"{self.codename} has lowered it to {cost_price}")
    #             if self.cost_price < data["cost_price"]:
    #                 print(f"Cost price in Dolibarr was {self.cost_price} but " +
    #                       f"{self.codename} has raised it to {cost_price}")
    #         self.cost_price = cost_price
    #         self.external_image_url = data["external_image_url"]
    #         self.external_stock = data["external_stock"]
    #         self.external_url = data["external_url"]
    #         self.restock_date = data["restock_date"]
    #         description = data["description"]
    #         if description:
    #             if (self.description is not None and self.description != "" and
    #                     self.description != description and description is not None):
    #                 answer = self.ask_yes_no_question(f"Description already exists: "
    #                                                        f"{self.description}, replace with "
    #                                                        f"{description}?")
    #                 if answer:
    #                     if self.codename.value == "JO":
    #                         self.description = description.replace("¤ ", "\n")
    #             elif not self.description or self.description == "":
    #                 if self.codename.value == "JO":
    #                     self.description = description.replace("¤ ", "\n")
    #                 else:
    #                     self.description = description
    #         self.external_list_price = data["list_price"]
    #         self.last_update = datetime.today()
    #         self.expired = Expired.FALSE
    #         self.status_buy = Status.ENABLED
    #         # self.update()

    def mark_expired_and_update(self):
        print("Marking expired now.")
        self.expired = Expired.TRUE
        self.status_buy = Status.DISABLED
        self.external_stock = 0
        self.update()

    def update(self):
        """Update product in Dolibarr from object"""
        # todo test this
        logger.debug("update: Running")
        if self.ref is None:
            raise MissingInformationError("self.ref was None")
        data = dict(
            ref=self.ref,
            cost_price=self.cost_price,
            label=self.label,
            description=self.description,
            status_buy=self.status_buy.value,
            status_sell=self.status_sell.value,
            accountancy_code_sell=self.accountancy_code_sell,
            accountancy_code_buy=self.accountancy_code_buy,
            accountancy_code_buy_export=self.accountancy_code_buy_export,
            vat_tx=self.sales_vat_rate.value,
        )
        if config.loglevel == logging.DEBUG:
            logger.debug("Sending this data to Dolibarr")
            print(data)
        r = self.api.call_update_api(DolibarrEndpoint.PRODUCTS, self.id, params=data)
        if r.status_code == 200:
            self.__insert_extrafields__()
            if self.expired == Expired.FALSE:
                logger.debug(f"expired:{self.expired}")
                self.__insert_multiprices__()
                self.__update_purchase_price__()
                print(f"Succesfully updated the entity {self.label}")
            else:
                logger.info(
                    "Not updating purchase price because the product has expired"
                )
        else:
            raise ValueError(f"Got {r.status_code} from Dolibarr")

    def update_extrafields(self):
        self.__insert_extrafields__()

    def update_multiprices(self):
        self.__insert_multiprices__()
