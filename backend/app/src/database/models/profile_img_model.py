from typing import Optional

from sqlmodel import SQLModel, Field, Column


class BaseProfileImage(SQLModel):
     # This is generated from cloudinary
     img_url : Optional[str] = Field(nullable=True)
     public_key : Optional[str] = Field(nullable=True,unique=True, index=True)


class ProfileImage(BaseProfileImage,table=True):
     __tablename__  = "profile_img"
     id : int = Field(default=None, primary_key=True, index=True)
     user_id : str = Field(foreign_key='users.id', ondelete="CASCADE")


class UpdateProfileImage(BaseProfileImage):
     pass