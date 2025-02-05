from src.helpers.crud.create import Create
from src.helpers.crud.delete import Delete
from src.helpers.crud.update import Update
from src.models.dolibarr.my_dolibarr_api import MyDolibarrApi
from src.my_base_class import MyBaseClass


class MyBaseContr(MyBaseClass):
    """Inherits from MyBaseClass because we need the
    __get_json_auth_data__ method in the supplier login controllers"""

    api: MyDolibarrApi = MyDolibarrApi()  # default to production
    create: Create = Create()
    delete: Delete = Delete()
    update: Update = Update()
