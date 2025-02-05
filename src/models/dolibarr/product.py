import logging
from datetime import datetime, timezone
from pprint import pprint
from typing import Any, Dict, Optional

from requests import Response
from rich import print

import config
from src.models.dolibarr.entity import DolibarrEntity
from src.models.dolibarr.enums import (
    Currency,
    DolibarrEndpoint,
    Expired,
    Status,
    StockType,
)
from src.models.exceptions import MissingInformationError
from src.models.supplier.enums import EntityType
from src.models.suppliers.enums import (
    EUR_suppliers,
    SupportedSupplier,
)
from src.models.vat_rate import VatRate

logger = logging.getLogger(__name__)


class DolibarrProduct(DolibarrEntity):
    """This models the Dolibarr product object data"""

    # These are strings because in some countries they
    # might include other things than numbers
    # # 4535 within EU and 4545 outside EU
    array_options: Any = None  # does the API always output this?
    multiprices: Dict[Any, Any] = {}
    accountancy_code_buy_export: str = ""
    accountancy_code_buy: str = ""  # 4xxx
    accountancy_code_sell: str = ""  # 3xxx
    # bought_quantity: Optional[int]
    codename: Optional[Any] = None  # typing: SupportedSupplier
    cost_price: Optional[float] = 0.0
    currency: Optional[Currency] = None
    # default to 1
    currency_conversion_rate: float = 1
    description: str | None = None
    desiredstock: Optional[float] = 2.0
    entity_type: EntityType = EntityType.PRODUCT
    expired: Optional[Expired] = None
    # ref is a human readable join of the codename and the SKU
    ref: str = ""
    id: int = 0
    label: str = ""

    last_update: Optional[datetime] = None
    last_update_purchase_price: Optional[datetime] = None
    mean_calculated_cost: float = 0.0
    # minimum_quantity=1, # disabled because it is not used by me
    multicurrency_cost_price: float = 0.0
    multicurrency_sales_price: float = 0.0
    multiprice1: float = 0.0
    multiprice2: float = 0.0
    # Carriers with Enums
    price: float = 0.0
    purchase_price_found: bool = False
    restock_date: datetime | int | None = None
    seuil_stock_alerte: Optional[float] = 2.0
    status_buy: Status | None = Status.DISABLED
    status: Status | None = Status.DISABLED  # == status_sell
    stock_reel: Optional[
        float
    ] = None  # quantity currently in stock. See property methods below
    stock_theorique: Optional[float] = None
    type: StockType | None = StockType.SERVICE
    tva_tx: float = 0.0
    sales_vat_rate: Optional[VatRate] = None
    purchase_vat_rate: Optional[VatRate] = None
    # vat_amount = 0
    weight: Optional[float] = 0.0  # in grams
    supplier_product: Optional[Any] = None  # typing: SupplierEntity

    # Extra
    other: Any = None
    price_ttc: Any = None
    price_min: Any = None
    price_min_ttc: Any = None
    price_base_type: Any = None
    multiprices_ttc: Any = None
    multiprices_base_type: Any = None
    multiprices_min: Any = None
    multiprices_min_ttc: Any = None
    multiprices_tva_tx: Any = None
    prices_by_qty: Any = None
    prices_by_qty_list: Any = None
    default_vat_code: Any = None
    localtax1_tx: Any = None
    localtax2_tx: Any = None
    localtax1_type: Any = None
    localtax2_type: Any = None
    lifetime: Any = None
    qc_frequency: Any = None
    pmp: Any = None
    duration_value: Any = None
    duration_unit: Any = None
    finished: Any = None
    status_batch: Any = None
    batch_mask: Any = None
    customcode: Any = None
    url: Any = None
    weight_units: Any = None
    length: Any = None
    length_units: Any = None
    width: Any = None
    width_units: Any = None
    height: Any = None
    height_units: Any = None
    surface: Any = None
    surface_units: Any = None
    volume: Any = None
    volume_units: Any = None
    net_measure: Any = None
    net_measure_units: Any = None
    accountancy_code_sell_intra: Any = None
    accountancy_code_sell_export: Any = None
    accountancy_code_buy_intra: Any = None
    barcode: Any = None
    barcode_type: Any = None
    multilangs: Any = None
    date_creation: Any = None
    date_modification: Any = None
    stock_warehouse: Any = None
    fk_default_warehouse: Any = None
    fk_price_expression: Any = None
    fk_unit: Any = None
    price_autogen: Any = None
    is_object_used: Any = None
    entity: Any = None
    import_key: Any = None
    array_languages: Any = None
    linkedObjectsIds: Any = None
    canvas: Any = None
    ref_ext: Any = None
    country_id: Any = None
    country_code: Any = None
    state_id: Any = None
    region_id: Any = None
    barcode_type_coder: Any = None
    last_main_doc: Any = None
    note_public: Any = None
    note_private: Any = None
    total_ht: Any = None
    total_tva: Any = None
    total_localtax1: Any = None
    total_localtax2: Any = None
    total_ttc: Any = None
    date_validation: Any = None
    specimen: Any = None
    duration: Any = None
    stats_expedition: Any = None

    # Deprecate these
    # Integration
    sello_status: Optional[Status] = None
    sello_desc_sv: str = ""
    sello_id: Optional[int] = None
    sello_label_sv: str = ""
    external_image_url: str = ""
    external_list_price: float = 0.0
    external_url: str = ""
    external_stock: int = 0

    # Commented out because of test failure
    # @property
    # def label_de(self) -> str:
    #     option = "options_label_de"
    #     if self.array_options:
    #         if self.array_options.get(option, "") is not None:
    #             return str(self.array_options.get(option, ""))
    #     return ""
    #
    # @label_de.setter
    # def label_de(self, value) -> None:
    #     self.array_options = {"options_label_de": value}

    @property
    def label_en(self) -> str:
        option = "options_label_en"
        if self.array_options and self.array_options.get(option, "") is not None:
            return str(self.array_options.get(option, ""))
        return ""

    @label_en.setter
    def label_en(self, value) -> None:
        self.array_options = {"options_label_en": value}

    @property
    def desired_stock_quantity(self) -> int:
        return int(self.desiredstock)

    @desired_stock_quantity.setter
    def desired_stock_quantity(self, value):
        self.desiredstock = float(value)

    @property
    def external_ref(self) -> str:
        if self.array_options:
            return str(self.array_options["options_external_ref"])
        else:
            return ""

    @external_ref.setter
    def external_ref(self, value):
        """Extrafield method"""
        if not self.array_options:
            self.array_options = {}
        self.array_options["options_external_ref"] = value

    @property
    def is_bike_entity(self) -> bool:
        """This determines if the product is a bike product
        according to the accountancy_code_sell"""
        if self.accountancy_code_sell:
            if int(self.accountancy_code_sell) == 3001:
                return True
            else:
                return False
        else:
            raise MissingInformationError("self.accountancy_code_sell was missing")

    @property
    def local_price(self):
        return self.multiprice1

    @property
    def internet_price(self):
        return self.multiprice2

    @property
    def purchase_price_url(self) -> str:
        # moved from util where it was called product_url
        return f"{self._base_url}product/fournisseurs.php?id={self.id}"

    @property
    def selling_price_url(self) -> str:
        return f"{self._base_url}product/price.php?id={self.id}"

    @property
    def status_sell(self):
        return self.status

    @property
    def stock_warning_quantity(self) -> int:
        return int(self.seuil_stock_alerte)

    @stock_warning_quantity.setter
    def stock_warning_quantity(self, value):
        self.seuil_stock_alerte = float(value)

    @property
    def stock_quantity(self):
        return self.stock_reel

    @property
    def dolibarr_product_url(self):
        return f"{self._base_url}product/card.php?id={self.id}"

    # @property
    # def work_minutes(self) -> Optional[int]:
    #     if self.array_options and self.array_options.get("options_workminutes"):
    #         return int(self.array_options.get("options_workminutes"))
    #     else:
    #         return None

    def __calculate_sek_prices_from_eur__(self):
        """Calculate SEK prices for TUI and Dolibarr UI convenience"""
        logger.debug("__calculate_sek_prices_from_eur__: Running")
        self.cost_price = round(
            self.multicurrency_cost_price * config.eur_sek_exchange_rate, 2
        )
        # self.external_list_price = self.supplier_product.eur_list_price * config.eur_sek_exchange_rate

    def extract_from_list_api_or_fail(
        self,
        response: Response,
        target_key: str,
        key_title: str,
        found_text: str,
        error_text: str,
        is_extrafield: bool = False,
    ):
        """Check response looking for TARGET_KEY while displaying a message to
        users with the human title of the found object and some text"""
        # is this the best way to handle errors?
        if config.debug_responses:
            pprint(response)
        if isinstance(response, list):
            if is_extrafield is True:
                value = self.extrafield(response[0], target_key)
            else:
                value = response[0][target_key]
            if not self.empty_or_false(value):
                print(
                    f"{found_text}: " + f"{response[0][key_title]}",
                )
                return value
            else:
                raise ValueError(f"{error_text} not found in Dolibarr")
        else:
            raise ValueError(
                f"Error extracting {error_text}, got no list from Dolibarr"
            )

    # def __find_root_category__(
    #     self,
    #     assume_yes=False,
    # ):
    #     # Get root suppliers category ID
    #     r = self.api.call_list_api(
    #         DolibarrEndpoint.CATEGORIES,
    #         params={
    #             "sqlfilters": "(t.label:like:'%"
    #             + config.supplier_category
    #             + "%') "
    #             # root category
    #             "and (t.fk_parent:=:0)",
    #         },
    #     )
    #     if r.status_code == 200:
    #         json = r.json()
    #         if config.debug_responses:
    #             pprint(json)
    #         suppliers_category_id = self.extract_from_list_api_or_fail(
    #             json,
    #             "id",
    #             "label",
    #             "Supplier category id found for",
    #             "Supplier category id",
    #             is_extrafield=False,
    #         )
    #         # Find this suppliers category ID
    #         r = self.api.call_list_api(
    #             endpoint=DolibarrEndpoint.CATEGORIES,
    #             params={
    #                 "sqlfilters": "(t.label:like:'%"
    #                 + str(self.codename.value)
    #                 + "%') "
    #                 + "and (t.fk_parent:=:"
    #                 + suppliers_category_id
    #                 + ")"
    #             },
    #         )
    #         not_found = (
    #             "Failed to find the correct supplier category. "
    #             + "Please fix. See "
    #             + f"{self._base_url}categories/viewcat.php"
    #             + "?type=product&id=8"
    #         )
    #         if r.status_code == 404:
    #             raise ValueError(not_found)
    #         elif r.status_code == 200:
    #             json = r.json()
    #             if config.debug_responses:
    #                 pprint(json)
    #             category_id = self.extract_from_list_api_or_fail(
    #                 json,
    #                 "id",
    #                 "label",
    #                 "Category id found for",
    #                 "Category id",
    #                 is_extrafield=False,
    #             )
    #             if assume_yes:
    #                 print("Assuming this is the correct category.")
    #             else:
    #                 answer = self.ask_yes_no_question("Is that the correct category?")
    #                 if answer:
    #                     return category_id
    #                 else:
    #                     raise ValueError(not_found)
    #         else:
    #             raise ValueError(f"Got {r.status_code}")
    #     else:
    #         raise ValueError(f"Got {r.status_code}")

    def __get_purchase_data__(self):
        """Fetch the purchase data including currency and multicurrency buy prices"""
        # TODO create new class that supports multiple prices?
        if not self.id:
            raise ValueError("self.id was None")
        r = self.api.get_purchase_prices_by_id(self.id)
        if r.status_code == 200:
            # It returns a list so pick the first one
            data = r.json()
            if len(data) == 1:
                if config.loglevel == logging.DEBUG and config.debug_responses:
                    print(data)
                self.purchase_price_found = True
                self.purchase_vat_rate = VatRate(value=float(data[0]["fourn_tva_tx"]))
                # DISABLED because we don't want to use this data ever for anything
                # when importing an order from MS we always use the price on the invoice
                # multicurrency_cost_price = data[0]["fourn_multicurrency_price"]
                # if not self.empty_or_false(multicurrency_cost_price):
                #     self.multicurrency_cost_price = float(multicurrency_cost_price
                #     )
                # else:
                #     if multicurrency_cost_price:
                #         logger.debug(multicurrency_cost_price)
                #         raise ValueError(f"Could not parse multicurrency_cost_price: '{multicurrency_cost_price}'")
                self.currency = None
                currency_value = data[0]["fourn_multicurrency_code"]
                if not self.empty_or_false(currency_value):
                    self.currency = Currency(currency_value)
                    logger.debug(f"Got currency {self.currency.name}")
                else:
                    logger.warning(f"Got no currency for product {self.url}")
                    # print(data)
                    # raise DebugExit()
                # input("press enter to continue")
                self.last_update_purchase_price = datetime.fromtimestamp(
                    data[0]["fourn_date_modification"], tz=timezone.utc
                )
            elif len(data) == 0:
                logger.info(
                    "No purchase price found in Dolibarr, setting default currency"
                )
                self.__set_default_currency__()
            else:
                raise ValueError(
                    f"more than "
                    f"one purchase price is not supported, see {self.purchase_price_url}"
                )
                # logger.warning(
                #     f"Skipping {self.id} because more than "
                #     f"one purchase price is not supported, see {self.purchase_price_url}"
                # )
        else:
            raise ValueError(f"Got {r.status_code} from Dolibarr")

    # def __make_internal_ref__(self):
    #     if not self.codename:
    #         raise ValueError("codename is None")
    #     elif not self.ref:
    #         raise ValueError("ref is None")
    #     else:
    #         self.internal_ref = str(self.codename.value) + "-" + self.ref

    # def __make_internal_ref_from_supplier_product__(self):
    #     logger.debug("making internal ref from supplier product")
    #     if not self.supplier_product:
    #         raise ValueError("self.supplier_product is None")
    #     if not self.supplier_product.codename:
    #         raise ValueError("codename is None")
    #     elif not self.supplier_product.sku:
    #         raise ValueError("ref was None")
    #     else:
    #         self.internal_ref = (
    #             self.supplier_product.codename.value
    #             + "-"
    #             + str(self.supplier_product.sku)
    #         )
    #         logger.debug(f"generated internal ref:{self.internal_ref}")

    def __parse_codename__(self):
        # disabled because of pydantic 2.7 error
        # logger.debug(f"trying to parse codename from {self.label}, see {self.url}")
        if self.array_options and self.array_options.get(
            "options_main_supplier_codename"
        ):
            self.codename = SupportedSupplier(
                self.array_options.get("options_main_supplier_codename")
            )

    def __parse_multiprices__(self):
        """We only support 2 multiprices for now"""
        logger.debug("__parse_multiprices__: Running")
        for entry in self.multiprices:
            if entry == "1":
                self.multiprice1 = self.multiprices[entry]
            elif entry == "2":
                self.multiprice2 = self.multiprices[entry]
        if self.multiprice1 is None and self.price:
            logger.debug("Migrating old price to multiprice1")
            self.multiprice1 = self.price

    def __parse_vat__(self):
        logger.info("Parsing the selling VAT rate from Dolibarr")
        if self.status_sell == Status.ENABLED and not self.tva_tx:
            if self.id in config.entities_with_no_vat:
                self.sales_vat_rate = VatRate.ZERO
            else:
                raise ValueError(
                    f"self.tva_tx was None for product with id {self.id}"
                    f", please fix in "
                    f"Dolibarr at {self.selling_price_url}"
                )
        self.sales_vat_rate = VatRate(int(float(self.tva_tx)))
        if not self.sales_vat_rate:
            raise ValueError("self.selling_vat_rate was None")

    def __set_default_currency__(self):
        """Set the default currency automatically"""
        if self.codename == SupportedSupplier.MESSINGSCHLAGER:
            logger.debug("Setting EUR as currency")
            self.currency = Currency.EUR
        else:
            logger.debug("Defaulting to SEK as currency")
            self.currency = Currency.SEK

    def fetch_purchase_data_and_finish_parsing(self):
        """This finishes the parsing of product data from Dolibarr"""
        logger.debug("fetch_purchase_data_and_finish_parsing: Running")
        if self.type == StockType.STOCKED:
            # We only parse the codename from products that are stocked
            self.__parse_codename__()
        self.__parse_multiprices__()
        self.__get_purchase_data__()
        self.__parse_vat__()
        # We only check for currency if there is a purchase price
        if self.purchase_price_found and not self.currency:
            logger.debug("Found purchase price bug no currency")
            self.__set_default_currency__()
        if not self.label:
            raise ValueError("self.label was None")
        if not self.type:
            # type is needed when adding products to orders in dolibarr
            raise ValueError("self.type was None")

    def set_status_sell(self, status: Status):
        self.status = status

    def set_stock_warning_quantity(self, quantity: int):
        self.seuil_stock_alerte = float(quantity)

    # def set_work_minutes(self, minutes: int):
    #     if self.array_options:
    #         self.array_options["options_workminutes"] = str(minutes)

    @property
    def virtual_stock(self):
        return self.stock_theorique

    def lookup_from_supplier_product(self) -> Optional[Any]:
        """This method looks up the product in Dolibarr and returns it if found"""
        logger.debug("lookup_from_supplier_product: Running")
        if self.supplier_product is None:
            raise MissingInformationError("self.supplier_product was None")
        # This does not work for some reason. We get a
        # if isinstance(self.supplier_product, SupplierService):
        # Workaround:
        if "SupplierService" in str(self.supplier_product.__class__):
            logger.debug("Got service")
            if not self.supplier_product.dolibarr_product_id:
                raise MissingInformationError("dolibarr_product_id was None")
            self.id = self.supplier_product.dolibarr_product_id
            product = self.get_by_id()
            # Set the eur cost price
            product.multicurrency_cost_price = self.supplier_product.eur_cost_price
            return product
        else:
            logger.debug("Got product")
            if self.supplier_product is not None and not self.supplier_product.codename:
                raise MissingInformationError("Codename was None")
            if self.supplier_product is not None and self.supplier_product.sku:
                # Get the dolibarr supplier object
                from src.models.dolibarr.supplier import DolibarrSupplier

                current_supplier: DolibarrSupplier = DolibarrSupplier(
                    codename=self.supplier_product.codename
                )
            else:
                raise MissingInformationError("self.supplier_product.ref was empty")
            if not current_supplier.codename:
                raise MissingInformationError("current_supplier.codename was None")
            r = self.api.call_list_api(
                DolibarrEndpoint.PRODUCTS,
                {
                    "thirdparty_ids": current_supplier.id,
                    "sqlfilters": f"(t.ref:=:'{self.supplier_product.generated_dolibarr_ref}')",
                },
            )
            if r.status_code == 200:
                logger.debug("Got product from Dolibarr")
                dolibarr_json = r.json()
                if len(dolibarr_json) == 1:
                    if config.debug_responses:
                        pprint(dolibarr_json[0])
                    from src.views.dolibarr.product import DolibarrProductView

                    dolibarr_product = DolibarrProductView(**dolibarr_json[0])
                    # This is needed to get the currency
                    dolibarr_product.fetch_purchase_data_and_finish_parsing()
                    if dolibarr_product.currency is None:
                        raise ValueError("currency was None")
                    if self.supplier_product.codename not in EUR_suppliers:
                        # We override the cost price in Dolibarr with the one on the
                        # order to make sure it is right
                        if (
                            dolibarr_product.cost_price
                            and self.supplier_product.cost_price
                        ):
                            # self.__print_price_difference__(
                            #     dolibarr_product=dolibarr_product
                            # )
                            dolibarr_product.cost_price = (
                                self.supplier_product.cost_price
                            )
                        elif not self.supplier_product.cost_price:
                            raise MissingInformationError(
                                "self.supplier_product.cost_price was None or 0. "
                                f"see {self.purchase_price_url}"
                            )
                    else:
                        logger.debug("Setting multicurrency_cost_price")
                        dolibarr_product.multicurrency_cost_price = float(
                            self.supplier_product.eur_cost_price
                        )
                    return dolibarr_product
                else:
                    raise ValueError(f"Got multiple or no results: {dolibarr_json}")
            elif r.status_code == 404:
                logger.error(
                    f"Did not find product with external_ref "
                    f"{self.supplier_product.sku} and codename "
                    f"{self.supplier_product.codename}"
                )
                # raise DebugExit()
                return None
            else:
                raise ValueError(r.text)

    def get_by_id(self) -> Any:
        """This does not update the current product,
        but instead returns a new instance"""
        if not self.id:
            raise ValueError("self.id was None")

        r = self.api.get_product_by_id(self.id)
        if r.status_code == 200:
            data = r.json()
            if config.debug_responses:
                print(data)
            from src.views.dolibarr.product import DolibarrProductView

            if isinstance(data, list):
                logger.debug("got list from Dolibarr")
                dolibarr_product = DolibarrProductView(**data[0])
                dolibarr_product.api = self.api
                dolibarr_product.fetch_purchase_data_and_finish_parsing()
                return dolibarr_product
            else:
                logger.debug("got dict from Dolibarr")
                dolibarr_product = DolibarrProductView(**data)
                dolibarr_product.api = self.api
                dolibarr_product.fetch_purchase_data_and_finish_parsing()
                return dolibarr_product
        else:
            raise ValueError(f"Got {r.status_code} from Dolibarr")

    def get_by_external_ref(
        self, codename: SupportedSupplier, external_ref: str
    ) -> Optional[Any]:  # type here is DolibarrProduct but setting it gives an error
        """Get product by internal external_ref if it exist and return DolibarrProduct"""
        product_id = self.read.get_dolibarr_product_id_by_external_ref(
            external_ref=external_ref, codename=codename
        )
        if product_id:
            from src.views.dolibarr.product import DolibarrProductView

            p = DolibarrProductView(api=self.api, id=product_id)
            return p.get_by_id()
        else:
            logger.info(
                f"No product found in Dolibarr with codename: {codename.name} and ref '{external_ref}'"
            )
            return None
