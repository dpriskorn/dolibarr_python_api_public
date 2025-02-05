from abc import ABC, abstractmethod

from requests import Session

from src.controllers.my_base_contr import MyBaseContr


class SupplierLoginContr(MyBaseContr, ABC):
    """Abstract controller class for supplier cart"""

    success: bool = False

    @abstractmethod
    def login(self) -> Session:
        """Logs in and return session"""
        raise NotImplementedError()
