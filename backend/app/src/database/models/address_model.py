from typing import Optional

from fastapi import Body
from sqlmodel import Field, SQLModel


class BaseAddress(SQLModel):
     barangay: Optional[str] = Field(nullable=True)
     city: Optional[str] = Field(nullable=True)
     province: Optional[str] = Field(nullable=True)
     regions: Optional[str] = Field(nullable=True)


class Address(BaseAddress, table=True):
     __tablename__ = 'address'
     id: int = Field(default=None, primary_key=True, index=True)
     user_id: str = Field(foreign_key='users.id', ondelete="CASCADE")


class UpdateAddress(BaseAddress):

     @staticmethod
     def update_schema(barangay: Optional[str] = Body(None),
                       city: Optional[str] = Body(None),
                       province: Optional[str] = Body(None),
                       regions: Optional[str] = Body(None)
                       ):
          return BaseAddress(barangay=barangay,
                             city=city,
                             province=province,
                             regions=regions)
