# import logging
# from unittest import TestCase
#
# import config
#
# logging.basicConfig(level=config.loglevel)
#
#
# class DolibarrUpload(TestCase):
#     @staticmethod
#     def test_upload():
#         from src.models.dolibarr.my_dolibarr_api import MyDolibarrApi
#
#         api = MyDolibarrApi()
#         # Read the contents of the file
#         file_path = (
#             "/home/dpriskorn/src/python/dolibarr_python_api/test_data/test.base64"
#         )
#         with open(file_path) as f:
#             base64_data = f.read()
#         response = api.upload_file(object_id=2184, filecontent=base64_data)
#         print(response.status_code)
#         print(response.text)
#         assert response.status_code == 200
