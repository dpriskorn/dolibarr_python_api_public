from typing import List

from src.models.dolibarr import DolibarrEndpoint
from src.models.dolibarr.product import DolibarrProduct
from src.views.my_base_view import MyBaseView


class DolibarrEntitiesView(MyBaseView):
    """Get products or services from the Dolibarr API"""

    def check_all_products(self):
        raise NotImplementedError("finish this if needed")
        # self.get_stockable_products()
        # p.fetch_purchase_data_and_finish_parsing()
        # if p.status_sell == Status.ENABLED and p.multiprice1 is None:
        #     print(product)
        #     raise DebugExit()

    def get_out_of_stock_but_for_sale_and_in_stock_at_supplier(
        self,
    ) -> List[DolibarrProduct]:
        """Returns a list of product objects"""
        if not self.api:
            self.__setup_api__()
        if self.api:
            r = self.api.call_list_api(
                DolibarrEndpoint.PRODUCTS,
                {
                    "sortfield": "t.label",
                    "limit": "500",
                    "sqlfilters": "(t.fk_product_type: = :'0') and (t.tosell: = :'1') and (t.reel: = :'0')",
                },
            )
            if r.status_code == 200:
                products = self.convert_dolibarr_product_list_to_objects(r.json())
                product_list = [
                    p
                    for p in products
                    if (p.stock_quantity is not None and p.stock_quantity > 0)
                ]
                if len(product_list) == 0:
                    print(
                        "No out of stock products for sale are "
                        + "currently in stock at the supplier",
                    )
                return product_list
            else:
                raise ValueError(f"Got {r.status_code} from Dolibarr")
        else:
            raise ValueError("self.api was None")

    def get_bike_services(self) -> List[DolibarrProduct]:
        """Returns a list of product objects"""
        if not self.api:
            self.__setup_api__()
        if self.api:
            r = self.api.call_list_api(
                DolibarrEndpoint.PRODUCTS,
                {
                    "sortfield": "t.label",
                    "limit": "700",
                    "sqlfilters": "(t.fk_product_type: = :'1')",
                },
            )
            if r.status_code == 200:
                return [
                    service
                    for service in self.convert_dolibarr_product_list_to_objects(
                        r.json()
                    )
                    if service.is_bike_entity
                ]
            else:
                raise ValueError(f"Got {r.status_code} from Dolibarr")
        else:
            raise ValueError("self.api was None")

    def get_services(self) -> List[DolibarrProduct]:
        """Returns a list of product objects"""
        if not self.api:
            self.__setup_api__()
        if self.api:
            r = self.api.call_list_api(
                DolibarrEndpoint.PRODUCTS,
                {
                    "sortfield": "t.label",
                    "limit": "700",
                    "sqlfilters": "(t.fk_product_type: = :'1')",
                },
            )
            if r.status_code == 200:
                return self.convert_dolibarr_product_list_to_objects(r.json())
            else:
                raise ValueError(f"Got {r.status_code} from Dolibarr")
        else:
            raise ValueError("self.api was None")

    def get_stockable_products(self) -> List[DolibarrProduct]:
        """Returns a list of product objects"""
        if not self.api:
            self.__setup_api__()
        if self.api:
            r = self.api.call_list_api(
                DolibarrEndpoint.PRODUCTS,
                {
                    "sortfield": "t.label",
                    "limit": "500",
                    "sqlfilters": "(t.fk_product_type: = :'0')",
                },
            )
            if r.status_code == 200:
                return self.convert_dolibarr_product_list_to_objects(r.json())
            else:
                raise ValueError(f"Got {r.status_code} from Dolibarr: {r.text}")
        else:
            raise ValueError("self.api was None")

    def get_stocked_and_for_sale_with_missing_external_ref(
        self,
    ) -> List[DolibarrProduct]:
        """Returns a list of product objects"""
        if not self.api:
            self.__setup_api__()
        if self.api:
            r = self.api.call_list_api(
                DolibarrEndpoint.PRODUCTS,
                {
                    "sortfield": "t.label",
                    "limit": "500",
                    "sqlfilters": "(t.fk_product_type: = :'0') and (t.tosell: = :'1')",
                },
            )
            if r.status_code == 200:
                products = self.convert_dolibarr_product_list_to_objects(r.json())
                product_list = [p for p in products if not p.external_ref]
                if len(product_list) == 0:
                    print(
                        "No stocked products for sale are "
                        + "currently missing an external external_ref",
                    )
                else:
                    print(f"found {len(product_list)} products without external_ref")
                    for p in product_list:
                        print(p.url)
                return product_list
            else:
                raise ValueError(f"Got {r.status_code} from Dolibarr: {r.text}")
        else:
            raise ValueError("self.api was None")

    def get_stocked_and_for_sale_and_out_of_stock_at_supplier(
        self,
    ) -> List[DolibarrProduct]:
        """Returns a list of product objects which are in stock
        and for sale but out of stock at the supplier"""
        if not self.api:
            self.__setup_api__()
        if self.api:
            r = self.api.call_list_api(
                # We get all products which are for sale
                DolibarrEndpoint.PRODUCTS,
                {
                    "sortfield": "t.label",
                    "limit": "500",
                    "sqlfilters": "(t.fk_product_type: = :'0') and (t.tosell: = :'1')",
                },
            )
            if r.status_code == 200:
                products = self.convert_dolibarr_product_list_to_objects(r.json())
                product_list = [
                    p
                    for p in products
                    if (
                        p.stock_quantity is not None
                        and p.stock_quantity > 0
                        and p.external_stock is not None
                        and p.external_stock == 0
                    )
                ]
                if len(product_list) == 0:
                    print(
                        "No stocked products for sale are "
                        + "currently out of stock at the supplier",
                    )
                return product_list
            else:
                raise ValueError(f"Got {r.status_code} from Dolibarr")
        else:
            raise ValueError("self.api was None")

    def search_stocked_and_for_sale(self, label: str) -> List[DolibarrProduct]:
        """Returns a list of product objects matching LABEL"""
        if not self.api:
            self.__setup_api__()
        if self.api:
            r = self.api.call_list_api(
                DolibarrEndpoint.PRODUCTS,
                {
                    "sortfield": "t.label",
                    "limit": "500",
                    "sqlfilters": f"(t.fk_product_type: = :'0') and (t.tosell: = :'1') and (t.label: ilike :'{label}')",
                },
            )
            if r.status_code == 200:
                return self.convert_dolibarr_product_list_to_objects(r.json())
            else:
                raise ValueError(f"Got {r.status_code} from Dolibarr")
        else:
            raise ValueError("self.api was None")

    def delete_latest_added_entity(self, endpoint: DolibarrEndpoint) -> None:
        if not self.api:
            self.__setup_api__()
        if self.api:
            r = self.api.call_list_api(
                endpoint, {"sortfield": "t.rowid", "limit": "1", "sortorder": "DESC"}
            )
            if r.status_code == 200:
                print(r.json()[0]["id"])
                if endpoint in (
                    DolibarrEndpoint.SUPPLIER_ORDER,
                    DolibarrEndpoint.SUPPLIER_INVOICE,
                ):
                    question = (
                        f'Delete {r.json()[0]["ref"]}'
                        + f'{r.json()[0]["id"]}:'
                        + f' {r.json()[0]["ref_supplier"]}'
                    )
                elif endpoint in [
                    DolibarrEndpoint.CUSTOMER_ORDER,
                    DolibarrEndpoint.INVOICES,
                ]:
                    question = (
                        f'Delete {r.json()[0]["ref"]}'
                        + f'{r.json()[0]["id"]}:'
                        + f' {r.json()[0]["ref_client"]}'
                    )
                elif endpoint == DolibarrEndpoint.PRODUCTS:
                    question = f'Delete {r.json()[0]["ref"]}: {r.json()[0]["label"]} with id: {r.json()[0]["id"]}:'
                elif endpoint == DolibarrEndpoint.THIRDPARTIES:
                    question = (
                        f'Delete {r.json()[0]["ref"]}' + f' {r.json()[0]["name"]}'
                    )
                else:
                    raise ValueError("unsupported entity")
                if self.ask_yes_no_question(question):
                    r = self.api.call_delete_api(endpoint, r.json()[0]["id"])
                    print(r)
                    print("Entity deleted")
        else:
            raise ValueError("self.api was None")
