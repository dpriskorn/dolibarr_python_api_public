from requests import Session

from src.models.basemodels.my_base_model import MyBaseModel


class ShimanoBaseModel(MyBaseModel):
    """This model is for all Shimano classes which only work
    when logged in so we require a session"""

    session: Session

    class Config:  # dead:disable
        arbitrary_types_allowed = True
