# import logging
#
# from flatten_json import flatten  # type: ignore
#
# import config
# # from src.models.basemodels.shimano import ShimanoBaseModel
# from src.models.exceptions import MissingInformationError, ScrapeError
# from src.models.suppliers.shimano.product.endpoint import ShimanoProductEndpoint
# from src.models.suppliers.shimano.product.options import ShimanoProductOptions
#
# logger = logging.getLogger(__name__)
#
#
# class ShimanoProductOptionsEndpoint(ShimanoBaseModel):
#     """This endpoint has lots of information about products"""
#
#     product_code: str
#
#     def get(self) -> ShimanoProductOptions:
#         if not self.session:
#             raise MissingInformationError()
#         if not self.product_code:
#             raise MissingInformationError("no product code")
#         url = (
#             f"https://api.c5vp9gk-shimanoin2-p1-public.model-t.cc.commerce.ondemand.com/"
#             f"shimanob2bcommercewebservices/v2/shimanoBike-se/products/{self.product_code}/options"
#         )
#         # headers: Dict[str, str] = {
#         #     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0",
#         #     "Accept": "application/json, text/plain, */*",
#         #     "Accept-Language": "en-US,en;q=0.5",
#         #     # 'Accept-Encoding': 'gzip, deflate, br',
#         #     "Content-Type": "application/json",
#         #     # "Authorization": "bearer M24gDqXIh5rLGaHAmhHyY6DHXCA",
#         #     "Origin": "https://b2b.shimano.com",
#         #     "DNT": "1",
#         #     "Connection": "keep-alive",
#         #     "Referer": "https://b2b.shimano.com/",
#         #     "Sec-Fetch-Dest": "empty",
#         #     "Sec-Fetch-Mode": "cors",
#         #     "Sec-Fetch-Site": "cross-site",
#         # }
#         params = {
#             "fields": "FULL",
#             "productOptions": "CLASSIFICATION",
#             "lang": "sv",
#             "curr": "SEK",
#         }
#         logger.debug(url)
#         # logger.debug(self.session.headers)
#         response = self.session.get(
#             url=url,
#             params=params,
#             # headers=headers
#         )
#         if response.status_code == 200:
#             data = flatten(response.json())
#             if config.debug_responses:
#                 print(data)
#             if not data:
#                 raise MissingInformationError(f"no data, see {url}")
#             return ShimanoProductOptions(**data)
#         elif response.status_code == 401:
#             raise ScrapeError(
#                 f"got {response.status_code} from Shimano, "
#                 f"which means logging in did not work because "
#                 f"we are not authorized."
#             )
#         elif response.status_code == 400:
#             # Fallback to product endpoint
#             product_endpoint = ShimanoProductEndpoint(
#                 product_code=self.product_code, session=self.session
#             )
#             return product_endpoint.get()
#         else:
#             # We get 400 when product not found
#             # print(response.text)
#             raise ScrapeError(
#                 f"got {response.status_code} from Shimano, "
#                 f"which means the product with the code: "
#                 f"'{self.product_code}' was not found, see {url}"
#             )
