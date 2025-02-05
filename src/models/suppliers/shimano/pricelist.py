# import logging
# import os
# from typing import List
#
# import pandas as pd  # type: ignore
# import requests
# from fuzzywuzzy import fuzz  # type: ignore
# from openpyxl import load_workbook  # type: ignore
# from pandas import DataFrame  # type: ignore
# from pydantic import BaseModel
#
# import config
# # from src.helpers.utilities import ask_yes_no_question
# from src.models.exceptions import FuzzyMatchError, MissingInformationError
# from src.models.suppliers.shimano import ShimanoLogin
# from src.models.suppliers.shimano.product import ShimanoProduct
#
# logger = logging.getLogger(__name__)

# DISABLED because we really don't need it
# class ShimanoPricelist(MyBaseModel):
#     products: List[ShimanoProduct] = []
#     pricelist_url: str = ""
#     refs_dataframe: DataFrame = None
#     data_dir: str = "/home/egil/src/python/dolibarr_python_api/data"
#     excluded_product_groups = ["Clothing", "Shoes"]
#
#     class Config:
#         arbitrary_types_allowed = True
#
#
#     def __download_file__(self, url: str):
#         """Snipped from https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests#16696317"""
#         local_filename = f"{self.data_dir}/{self.__extract_filename__()}"
#         # NOTE the stream=True parameter below
#         with requests.get(url, stream=True) as r:
#             r.raise_for_status()
#             with open(local_filename, "wb") as f:
#                 for chunk in r.iter_content(chunk_size=8192):
#                     # If you have chunk encoded response uncomment if
#                     # and set chunk_size parameter to None.
#                     # if chunk:
#                     f.write(chunk)
#         return local_filename
#
#     def __download_if_new__(self):
#         # extract the filename from the url
#         filename = self.__extract_filename__()
#         # check if we already downloaded it
#         file_list: List = os.listdir(self.data_dir)
#         if filename not in file_list:
#             with console.status("Downloading new pricelist"):
#                 self.__download_the_pricelist__()
#                 print("New pricelist downloaded succesfully")
#         else:
#             print(f"The pricelist {filename} on disk is the newest available")
#
#     def __download_the_pricelist__(self):
#         self.__download_file__(url=self.pricelist_url)
#
#     def __update_to_the_latest_pricelist__(self):
#         """Log in and get the latest url for the pricelist and download
#         it if it is we don't have it already on disk
#
#         The pricelist is ~3 MB and takes a few seconds to download"""
#         self.__get_url_to_latest_pricelist__()
#         self.__download_if_new__()
#
#     def __get_url_to_latest_pricelist__(self):
#         # Get from the pricelist_api
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0',
#             'Accept': 'application/json, text/plain, */*',
#             'Accept-Language': 'en-US,en;q=0.5',
#             # 'Accept-Encoding': 'gzip, deflate, br',
#             'Content-Type': 'application/json',
#             'Authorization': 'bearer M24gDqXIh5rLGaHAmhHyY6DHXCA',
#             'Origin': 'https://b2b.shimano.com',
#             'DNT': '1',
#             'Connection': 'keep-alive',
#             'Referer': 'https://b2b.shimano.com/',
#             'Sec-Fetch-Dest': 'empty',
#             'Sec-Fetch-Mode': 'cors',
#             'Sec-Fetch-Site': 'cross-site',
#         }
#
#         params = {
#             'currentPage': '0',
#             'fields': 'DEFAULT',
#             'pageSize': '9',
#             'type': 'ALL',
#             'lang': 'sv',
#             'curr': 'SEK',
#         }
#         response = requests.get(
#             'https://api.c5vp9gk-shimanoin2-p1-public.model-t.cc.commerce.ondemand.com/shimanob2bcommercewebservices/v2/shimanoBike-se/downloads/search',
#             params=params, headers=headers)
#         if config.debug_responses:
#             print(response.json())
#         # The first one is the latest
#         self.pricelist_url = "https://api.c5vp9gk-shimanoin2-p1-public.model-t.cc.commerce.ondemand.com" + response.json()["medias"][0]["media"]
#
#
#     def __get_pricelist_file_path__(self) -> str:
#         return f"{self.data_dir}/{self.__extract_filename__()}"
#
#     def __extract_filename__(self) -> str:
#         """Return the filename based on the URL
#         We remove spaces to avoid problems"""
#         if not self.pricelist_url:
#             raise MissingInformationError("self.pricelist_url was None")
#         # Split out the query stuff which makes for an awful long filename
#         return self.pricelist_url.split("?")[0].split("/")[-1]  # .replace(' ', '_')
#
#     def __get_all_product_item_numbers__(self) -> None:
#         """Load the latest pricelist from disk and save all the item numbers in a set"""
#         with console.status("Loading the pricelist refs into memory"):
#             # TODO switch to pandas and save to pickle to speed it up?
#             # We only care about the Item Number column for now
#             self.refs_dataframe = pd.read_excel(
#                 io=self.__get_pricelist_file_path__(), sheet_name="Data", usecols="G"
#             )  # type: ignore
#             # print(self.refs_dataframe.head())
#             # wb = load_workbook(filename=self.__get_pricelist_file_path__())
#             # # print(wb.get_sheet_names())
#             # sheet = wb.active
#             # # Skip header by starting at 2
#             # for x in range(2, 14000):
#             #     ref = sheet.cell(row=x, column=7).value
#             #     if ref:
#             #         self.refs.add(ref)
#         print(
#             f"Finished loading {len(self.refs_dataframe)} refs from the pricelist"
#         )
#
#     # def __load_and_parse_the_whole_pricelist__(self):
#     #     """Load the latest pricelist from disk and parse it into objects"""
#     #     # load it using a library
#     #     with console.status("Loading the pricelist data into memory"):
#     #         wb = load_workbook(filename=self.__get_pricelist_file_path__())
#     #         # print(wb.get_sheet_names())
#     #         sheet = wb.active
#     #         # Skip header by starting at 2
#     #         for x in range(2, 14000):
#     #             product_group = sheet.cell(row=x, column=4).value
#     #             if product_group not in self.excluded_product_groups:
#     #                 # parse it into ShimanoProducts
#     #                 # for column in range(1,35):
#     #                 #     print(f"{column}: {sheet.cell(row=x, column=column).value}")
#     #                 try:
#     #                     cost_price = float(sheet.cell(row=x, column=26).value)
#     #                 except TypeError:
#     #                     cost_price = 0.
#     #                 try:
#     #                     ean = int(sheet.cell(row=x, column=16).value)
#     #                 except ValueError:
#     #                     ean = 0
#     #                 image_filename = sheet.cell(row=x, column=13).value
#     #                 if image_filename:
#     #                     image_url = f"http://www.shimanoshop-eu.com/SHOP/Artikel_KENMERKOPTIE/{image_filename}"
#     #                 else:
#     #                     image_url = ""
#     #                 try:
#     #                     list_price = float(sheet.cell(row=x, column=31).value)
#     #                 except TypeError:
#     #                     list_price = 0.
#     #                 sp = ShimanoProduct(
#     #                     brand=sheet.cell(row=x, column=3).value,
#     #                     cost_price=cost_price,
#     #                     description=sheet.cell(row=x, column=11).value or "",
#     #                     ean=ean,
#     #                     image_url=image_url,
#     #                     label=f"{sheet.cell(row=x, column=8).value}: {sheet.cell(row=x, column=9).value}",
#     #                     list_price=list_price,
#     #                     model_name=sheet.cell(row=x, column=5).value,
#     #                     product_group=product_group,
#     #                     ref=sheet.cell(row=x, column=7).value,
#     #                 )
#     #                 sp.url = sp.generated_url()
#     #                 if config.loglevel == logging.DEBUG:
#     #                     print(sp.dict())
#     #                 self.products.append(sp)
#     #                 # raise DebugExit()
#     #     print("The latest pricelist has now been loaded into memory")
#
#     def load_and_parse_the_latest_pricelist(self) -> None:
#         self.__update_to_the_latest_pricelist__()
#         self.__get_all_product_item_numbers__()
#
#     def get_valid_product_ref_from_pricelist(self, ref: str) -> str:
#         """Lookup the product by ref from the pricelist. If it fails do fuzzy matching"""
#         if hasattr(self, "refs_dataframe") and (
#             not self.refs_dataframe or self.refs_dataframe.empty
#         ):
#             self.load_and_parse_the_latest_pricelist()
#         result = self.refs_dataframe.loc[self.refs_dataframe["Item Number"] == ref]
#         if result.empty:
#             logger.info(
#                 f"Could not find the ref {ref} in the pricelist, trying to fuzzy match"
#             )
#             self.refs_dataframe["item_number_score"] = self.refs_dataframe[
#                 "Item Number"
#             ].apply(lambda x: fuzz.ratio(x, ref))
#             sorted_df: DataFrame = self.refs_dataframe.sort_values(
#                 by="item_number_score", ascending=False, inplace=False
#             )
#             print(sorted_df.head(1))
#             best_match_score = int(sorted_df.iloc[0]["item_number_score"])
#             best_match_ref = str(sorted_df.iloc[0]["Item Number"])
#             # best_match_score = int(self.refs_dataframe["item_number_score"][0])
#             logger.info(f"Best match score: {best_match_score}")
#             logger.info(f"Best match ref: {best_match_ref}")
#             print(sorted_df.head())
#             # We auto-approve matches over 95
#             if 95 >= best_match_score >= 90:
#                 result = ask_yes_no_question(message=f"Does the first one match {ref}?")
#                 if result:
#                     logger.info("Picking the best match as ref after user approval")
#                     return best_match_ref
#                 else:
#                     raise FuzzyMatchError("No valid match found :/")
#             elif best_match_score < 90:
#                 raise FuzzyMatchError(
#                     f"The best score {best_match_score} was below 90 "
#                     f"- No valid match found :/"
#                 )
#             else:
#                 logger.info("Picking the best match as ref")
#                 return best_match_ref
#         print(result)
#         logger.info("Returning exact match :)")
#         return str(self.refs_dataframe["Item Number"][0])
