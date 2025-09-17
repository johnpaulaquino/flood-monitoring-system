from datetime import date
from typing import Optional

from fastapi import Body
from sqlmodel import Column, Field, ForeignKey, SQLModel


class BasePersonalInformation(SQLModel):
     firstname: Optional[str] = Field(nullable=True)
     middle_name: Optional[str] = Field(nullable=True)
     last_name: Optional[str] = Field(nullable=True)
     birthdate: Optional[date] = Field(nullable=True)
     gender : Optional[str] = Field(nullable=True)


class PersonalInformation(BasePersonalInformation, table=True):
     __tablename__ = 'personal_info'
     id: int = Field(default=None, primary_key=True, index=True)
     user_id: str = Field(sa_column=Column(
             ForeignKey('users.id', ondelete="CASCADE"), nullable=True))
     age: int = Field(nullable=True)


class UpdatePersonalInformation(BasePersonalInformation):

     @staticmethod
     def update_personal_info_schema( firstname: Optional[str] = Body(None),
                                      middle_name: Optional[str] = Body(None),
                                      last_name: Optional[str] = Body(None),
                                      birthdate: Optional[date] = Body(None),
                                      gender: Optional[str] = Body(None)):
          return BasePersonalInformation(
                  firstname=firstname,
                  middle_name=middle_name,
                  last_name=last_name,
                  birthdate=birthdate,
                  gender=gender)