from datetime import date

from sqlmodel import Column, Field, ForeignKey, SQLModel


class BasePersonalInformation(SQLModel):
     firstname: str = Field(nullable=False)
     middle_name: str = Field(nullable=True)
     last_name: str = Field(nullable=True)
     birthdate: date = Field(nullable=False)
     gender : str = Field(nullable=False)


class PersonalInformation(BasePersonalInformation, table=True):
     __table_name = 'personal_info'
     id: int = Field(default=None, primary_key=True, index=True)
     user_id: str = Field(sa_column=Column(
             ForeignKey('users.id', ondelete="CASCADE"), nullable=True))
     age: int = Field(nullable=False)
