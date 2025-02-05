# see https://realpython.com/python-interface/#python-interface-overview
from abc import ABC

from pydantic import BaseModel


class ReferenceInterface(BaseModel, ABC):
    """Interface which mandates the implementer to have a reference attribute"""

    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, "reference") or NotImplemented
