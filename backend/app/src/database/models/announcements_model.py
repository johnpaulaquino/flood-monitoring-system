import uuid
from datetime import datetime

from fastapi import Body
from sqlalchemy import Column, DateTime, ForeignKey, func, Integer
from sqlmodel import Field, SQLModel


class BaseAnnouncements(SQLModel):
     content: str = Field(nullable=True)
     title: str = Field(nullable=True)


class Announcements(BaseAnnouncements, table=True):
     __tablename__ = 'announcements'
     id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, index=True)
     user_id: str = Field(sa_column=Column(
             ForeignKey('users.id', ondelete="CASCADE"), nullable=True))
     image_url_id: int = Field(sa_column=Column(Integer,
                                                ForeignKey('profile_img.id', ondelete="CASCADE")))
     created_at: datetime = Field(sa_column=Column(type_=DateTime(timezone=True),
                                                   server_default=func.now()))


class CreateAnnouncements(BaseAnnouncements):
     pass

     @staticmethod
     def create_announcements_as_body_form(content: str = Body(), title: str = Body()):
          return BaseAnnouncements(content=content, title=title)


class UpdateAnnouncements(BaseAnnouncements):


     @staticmethod
     def update_announcements_as_body_form(content: str = Body(), title: str = Body()):
          return BaseAnnouncements(content=content, title=title)
