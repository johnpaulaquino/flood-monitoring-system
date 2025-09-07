from sqlmodel import SQLModel

from app.src.database.models.address_model import Address
from app.src.database.models.personal_information_models import PersonalInformation
from app.src.database.models.profile_img_model import ProfileImage
from app.src.database.models.users_model import Users

Base = SQLModel()
__all__ = [
        "Users",
        "Address",
        "PersonalInformation",
        "ProfileImage",
        "Base"
]
