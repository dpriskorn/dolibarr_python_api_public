# from flatten_json import flatten  # type: ignore
#
# import config
# # from src.models.basemodels.shimano import ShimanoBaseModel
# from src.models.exceptions import MissingInformationError, ScrapeError
# from src.models.suppliers.shimano.product.options import ShimanoProductOptions
#
#
# class ShimanoProductEndpoint(ShimanoBaseModel):
#     """This endpoint has price and other product information"""
#
#     product_code: str
#
#     def get(self) -> ShimanoProductOptions:
#         if not self.session or not self.product_code:
#             raise MissingInformationError()
#         url = (
#             f"https://api.c5vp9gk-shimanoin2-p1-public.model-t.cc.commerce."
#             f"ondemand.com/shimanob2bcommercewebservices/"
#             f"v2/shimanoBike-se/products/{self.product_code}"
#         )
#         print(dict(self.session.headers))
#         headers = {
#             "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0",
#             "Accept": "application/json, text/plain, */*",
#             "Accept-Language": "en-US,en;q=0.5",
#             # 'Accept-Encoding': 'gzip, deflate, br',
#             # 'Authorization': 'bearer cHNINqaeSDBtDDa-gIqLxgEgaas',
#             "Origin": "https://b2b.shimano.com",
#             "DNT": "1",
#             "Connection": "keep-alive",
#             "Referer": "https://b2b.shimano.com/",
#             "Sec-Fetch-Dest": "empty",
#             "Sec-Fetch-Mode": "cors",
#             "Sec-Fetch-Site": "cross-site",
#         }
#         params = {
#             "fields": "FULL",
#             "lang": "sv",
#             "curr": "SEK",
#         }
#         response = self.session.get(
#             url,
#             params=params,
#             headers=headers,
#         )
#         # response = self.session.get(url=url)
#         if response.status_code == 200:
#             data = flatten(response.json())
#             if config.debug_responses:
#                 print(data)
#             if not data:
#                 raise MissingInformationError(f"no data, see {url}")
#             return ShimanoProductOptions(**data)
#         else:
#             # find cause of  get errors
#             # print(response.text)
#             raise ScrapeError(
#                 f"got {response.status_code} and {response.json()} from Shimano, see {url}"
#             )
