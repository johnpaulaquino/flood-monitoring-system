from typing import Optional

from sqlmodel import SQLModel, Column, Field



class BaseAddress(SQLModel):
     barangay : Optional[str] = Field()
     city : Optional[str] = Field()
     municipality : Optional[str] = Field()
     province : Optional[str] = Field()


class Address(SQLModel, table= True):
     id : int = Field(primary_key=True, index=True)
     user_id : int = Field(foreign_key='users.id', ondelete="CASCADE")




