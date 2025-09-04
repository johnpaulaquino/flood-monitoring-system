from datetime import date

from sqlmodel import SQLModel, Field,Column,ForeignKey


class BasePersonalInformation(SQLModel):
     firstname : str = Field(nullable=False)
     middle_name : str = Field(nullable=True)
     last_name : str = Field(nullable=True)
     age : int = Field(nullable=False)
     birthdate : date = Field(nullable=False)


class PersonalInformation(SQLModel, table = True):
     __table_name = 'personal_info'
     id : int = Field(primary_key=True)
     user_id : int = Field(sa_column=Column(
             ForeignKey('users.id', ondelete="CASCADE"), nullable=True))


