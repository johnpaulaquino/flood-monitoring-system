from typing import Optional

from sqlmodel import Field, SQLModel


class BaseAddress(SQLModel):
     barangay: Optional[str] = Field(nullable=True)
     city: Optional[str] = Field(nullable=True)
     municipality: Optional[str] = Field(nullable=True)
     province: Optional[str] = Field(nullable=True)


class Address(BaseAddress, table=True):
     __tablename__ = 'address'
     id: int = Field(default=None, primary_key=True, index=True)
     user_id: int = Field(foreign_key='users.id', ondelete="CASCADE")
