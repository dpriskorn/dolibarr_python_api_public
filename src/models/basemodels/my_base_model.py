from src.helpers.crud.read import Read
from src.my_base_class import MyBaseClass


class MyBaseModel(MyBaseClass):
    """This class helps other classes that need to read from the database"""

    read: Read = Read()
    # model_config = {"arbitrary_types_allowed": "true"}
