# disabled because the test fail
# import logging
# from pprint import pprint
#
# from requests import Response, Session
#
# import config
# from src.controllers.supplier.cart import SupplierCartContr
# from src.controllers.suppliers.ms.login import MsLoginContr
# from src.models.exceptions import CartError
# from src.models.supplier.cart_response import CartResponse
# from src.models.suppliers.messingschlager.product import MessingschlagerProduct
#
# logger = logging.getLogger(__name__)
#
#
# class MsCart(SupplierCartContr):
#     response: Response | None = None
#     session: Session | None = None
#
#     def __go_to_cart__(self):
#         """This is to test we are really logged in"""
#         logger.debug("go to cart: running")
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0',
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
#             'Accept-Language': 'en-US,en;q=0.5',
#             # 'Accept-Encoding': 'gzip, deflate, br, zstd',
#             'DNT': '1',
#             'Connection': 'keep-alive',
#             'Referer': 'https://www.messingschlager.com/en/account',
#             'Upgrade-Insecure-Requests': '1',
#             'Sec-Fetch-Dest': 'document',
#             'Sec-Fetch-Mode': 'navigate',
#             'Sec-Fetch-Site': 'same-origin',
#             'Sec-Fetch-User': '?1',
#             'Priority': 'u=1',
#             # Requests doesn't support trailers
#             # 'TE': 'trailers',
#         }
#
#         response = self.session.get(
#             "https://www.messingschlager.com/en/cart",
#             headers=headers,
#         )
#         if response.status_code != 200:
#             raise CartError(f"could not go to cart, got {response.status_code} from MS")
#         else:
#             if config.write_test_data:
#                 with open("/tmp/test.html", "w") as f:
#                     f.write(response.text)
#             if not MsLoginContr.cart_link_is_present(response=response):
#                 raise CartError("not logged in")
#             else:
#                 logger.info("got cart successfully")
#
#     # def __artres__(self, product: MessingschlagerProduct):
#     #     """It's unclear what this is needed for"""
#     #     logger.debug("artres: running")
#     #     headers = {
#     #         "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0",
#     #         "Accept": "application/json, text/javascript, */*; q=0.01",
#     #         "Accept-Language": "en-US,en;q=0.5",
#     #         # 'Accept-Encoding': 'gzip, deflate, br, zstd',
#     #         "X-Requested-With": "XMLHttpRequest",
#     #         "DNT": "1",
#     #         "Connection": "keep-alive",
#     #         "Referer": "https://www.messingschlager.com/en/cart",
#     #         "Sec-Fetch-Dest": "empty",
#     #         "Sec-Fetch-Mode": "cors",
#     #         "Sec-Fetch-Site": "same-origin",
#     #         "Priority": "u=1",
#     #         # Requests doesn't support trailers
#     #         # 'TE': 'trailers',
#     #     }
#     #
#     #     params = {
#     #         "artikel_id": f"{product.sku}",
#     #     }
#     #
#     #     response = self.session.get(
#     #         "https://www.messingschlager.com/m3/ajax/ArtResV_check",
#     #         params=params,
#     #         headers=headers,
#     #     )
#     #     """response looks like so:"""
#     #     """{
#     #         "return": 0,
#     #         "menge_abruf": 0,
#     #         "menge_res": 0
#     #     }"""
#     #     print(response.text)
#
#     def add(self, product: MessingschlagerProduct, quantity: int = 1) -> CartResponse:
#         if product is None:
#             raise ValueError("got no product")
#         self.session = MsLoginContr().login()
#         # we should be logged in now
#         self.__go_to_cart__()
#         # self.__artres__(product=product)
#         return self.__add_product__(product=product,quantity=quantity)
#
#     def __add_product__(self, product: MessingschlagerProduct, quantity: int = 1) -> CartResponse:
#         logger.debug("add product: running")
#         headers = {
#             "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0",
#             "Accept": "application/json, text/javascript, */*; q=0.01",
#             "Accept-Language": "en-US,en;q=0.5",
#             # 'Accept-Encoding': 'gzip, deflate, br, zstd',
#             "X-Requested-With": "XMLHttpRequest",
#             "DNT": "1",
#             "Connection": "keep-alive",
#             "Referer": "https://www.messingschlager.com/en/cart",
#             "Sec-Fetch-Dest": "empty",
#             "Sec-Fetch-Mode": "cors",
#             "Sec-Fetch-Site": "same-origin",
#             # Requests doesn't support trailers
#             # 'TE': 'trailers',
#         }
#
#         params = {
#             "artikel_id": f"{product.sku}",
#             # 'artikel_id': '12969',
#             "menge": str(quantity),
#             # 'menge': '1',
#         }
#
#         response = self.session.get(
#             "https://www.messingschlager.com/m3/ajax/Basket_quickadd",
#             params=params,
#             headers=headers,
#         )
#         if response.status_code == 200:
#             """success response looks like this
#             {
#               "return": 1,
#               "html": "    \n        <div class=\"row m-l-0 m-r-0 m-b-2 product-item list p-t-1 p-b-1\"
#               id=\"xbasket-item-1089224\">\n            <div class=\"col-sm-2 col-xs-12\">\n
#                <div class=\"product-item-img\">\n                        <a href=\"\\/en\\/products\\/tires
#                _t105\\/kujo-one-0-one-t-protect-clincher-28-x-1.75_a558052\"><img class=\"img-fluid\"
#                src=\"\\/content\\/Artikelfotos\\/600x600\\/558052_KU-2003_170223.jpg\" \\/><\\/a>\t\t\t\t\t\t\n
#                                    <\\/div>\n            <\\/div>\n        <div class=\"col-sm-10 col-xs-12\">
#               \n            <div class=\"row\">\n                <div clas
#               s=\"col-sm-4 col-xs-12\">\n                        <input t
#               ype=\"hidden\" name=\"xbasket[1089224][basketitem_id]\" value
#               =\"1089224\"\\/> \n                        <div class=\"prod
#               uct-title ms-font-medium ms-color-black m-b-0\"><a href=\"\\
#               /en\\/products\\/tires_t105\\/kujo-one-0-one-t-protect-clinche
#               r-28-x-1.75_a558052\">KUJO One 0 One T Protect Clincher 28 x
#               1.75\"<\\/a>                        \n
#                   <\\/div>\n                        <span class=\"ms-colo
#                   r-darkgrey ms-artikel\">Article No.: 558052<\\/span><
#                   br\\/>\n                            \n
#                            <div class=\"delivery-info m-t-1 m-b-1\">
#                 \n
#                 <div class=\"delivery-info text-uppercase  m-t-2\">\n
#               <span ><i id=\"ampel-1089224\" class=\"stock-green fa fa-circle\
#               " aria-hidden=\"true\"><\\/i>\n
#                <span id=\"message-1089224\">Available - on stock<\\/span><\\/span>\n
#              <\\/div>                                            \n
#              <\\/div>\n                <\\/div>     \n                <div class=\"col-sm-5 col-xs-12\">\n
#              <div class=\"row ms-bg-warning\" id=\"mmz-msg-1089224\">
#             \n\n                <div class=\"col-xs-12\">
#           \n                    <span class=\"qty-hint\"><i id=\"mmz-icon-1089224\" class=\"fa fa-warni
#       ng ms-color-red\" aria-hidden=\"true\"><\\/i>\n                    Minimum quantity surchage 5,00
#   % For quantities below 25 pcs                    <\\/span>    \n                <\\/div>
#                                       \n            <\\/div>\n           \n\n
#               \n        <div class=\"row ms-bg-skintone \">\n            <div class=\"col-xs-12\">
#               \n                <span class=\"ms-bg-skintone qty-hint\"><i class=\"fa fa-info-circle\
#               " aria-hidden=\"true\"><\\/i>
#          \n                        Packed in bale of 25 pcs. Shipment as multiples.
#         \n                <\\/span>    \n            <\\/div>
#        \n        <\\/div>\n\n                        \n                        \n\n
# <\\/div>\n                <div class=\"col-sm-3 col-xs-12\">\n                     <div class=\"visible-u
# p-xs\">\n                            <div class=\"col-sm-12 text-xs-right\">\n
#                 <button type=\"button\" class=\"btn-drop ms-btn-small-lightblue ms-w-100-xs btn btn-
#                 primary m-t-1\" data-dropurl='\\/m3\\/ajax\\/Basket_drop' data-id=\"1089224\"><i class=\
#                 "fa fa-trash\" aria-hidden=\"true\"><\\/i>Delete<\\/button>\n
#                  <\\/div>\n                    <\\/div>\n                <\\/div>\n
#                  <div class=\"col-md-12 col-sm-12 col-xs-12\">\n                    <div class=\
#                  "col-md-2 col-sm-12 col-xs-12\">\n                        <label class=\"m-a-0
#                  ms-color-darkgrey\">Your article number:<\\/label><br>\n
#                  <input data-id=\"1089224\" \n                               class=\"kartikel  text
#                  -xs-center form-control ms-bg-lightgrey ms-w-50 m-l-0 m-t-0 m-b-0\" \n
#                                     type=\"text\" name=\"xbasket[1089224][kartikel]\" \n
#               value=\"\"\n
#               data-toggle=\"popover\" data-placement=\"bottom\"
#                data-trigger=\"focus\" data-content=\"Do you want to find your own article number in
#                your invoice and use it in the product search in the future? Please indicate it here.\"\n
#                                             \\/>\n                    <\\/div>\n                \n                    <div class=\"col-md-1 col-sm-12 col-xs-12\">\n                        <label class=\"m-a-0 ms-color-darkgrey\">Amount:<\\/label><br>          \n                           <input id=\"qty-1089224\" data-id=\"1089224\" class=\"qty form-control ms-bg-lightgrey text-xs-right p-r-1   m-t-0 m-b-0\"  type=\"text\" value=\"1\"  data-toggle=\"popover\" data-placement=\"bottom\" data-trigger=\"focus\" data-html=\"true\"  \\/>\n                    <\\/div>                    \n                \n                                        <div class=\"col-md-3 col-sm-4 col-xs-12 text-xs-right\">\n                            <label class=\"m-a-0 ms-color-darkgrey text-sm-right\">Your price&nbsp;(EUR):<\\/label><p class=\"ms-color-red m-b-0\"  id=\"preis-box-1089224\"><span class=\"text-sm-right \" id=\"preis-icon-1089224\"><i class=\"fa fa-warning\" > <\\/i><\\/span> <span class=\"ms-price-size-big\"  id=\"preis-1089224\">7,57<\\/span><\\/p><span class=\"ms-color-darkgrey text-sm-right\">pro piece<\\/span>                        \n                        <\\/div>   \n                        <div class=\"col-md-2 col-sm-4 col-xs-12 text-xs-right\">\n                                <div id=\"preis-alt-box-1089224\" \n                                                                        >\n                                    <label class=\"m-a-0 ms-color-darkgrey text-sm-right\">\n                                        Price&nbsp;(EUR):                                    <\\/label><br\\/>\n                                    <span class=\"ms-price-size-big\" id=\"preis-alt-1089224\">7,21<\\/span><br\\/><span class=\"text-sm-right\" id=\"preis-alt-lbl-1089224\"><\\/span>                                <\\/div>\n                        <\\/div>   \n                                        <div class=\"col-md-2 col-sm-4 col-xs-12 text-xs-right text-nowrap\">\n                        <label class=\"m-a-0 ms-color-darkgrey\">Total (EUR):<\\/label> <br\\/>                              \n                        \t\t\t\t\t              \n                             <div class=\"ms-price-size-big ms-final-price\"><span class=\"m-t-1\" id=\"summe-1089224\">7,57<\\/span><\\/div>                        \n                    <\\/div>                \n                <\\/div>\n            <\\/div>    \n        <\\/div>              \n    <\\/div>",
#               "message": "Article added to cart.<br>Please order multiples of packing units in order to avoid markups.<br\\/><strong>We recommend to add 24 piece.<\\/strong>",
#               "id": "1089224",
#               "count": 1,
#               "counttxt": "Your cart contains one article(s) amounting to 7,57 EUR.",
#               "shippingfree": 1,
#               "total": "7,57",
#               "backlog": "0,00",
#               "deliverable": "7,57",
#               "goodvalue": "7,57",
#               "shipping": ""
#             }
#             """
#             # print(response.text)
#             self.response = response
#             return self.__parse_response__()
#         else:
#             raise Exception(f"Got {response.status_code} from MS")
#
#     def __parse_response__(self) -> CartResponse:
#         data = self.response.json()
#         pprint(data)
#         # sys.exit()
#         if data["message"] == "Order item not found.":
#             raise CartError("could not add to cart, did login succeed?")
#         on_stock = bool("On stock" in data["html"])
#         cr = CartResponse(total_amount=float(data["total"]), on_stock=on_stock)
#         pprint(cr.model_dump())
#         return cr
