import uuid

from sqlmodel import Column, Field, SQLModel, String


class BaseUsers(SQLModel):
     username: str = Field(sa_column=Column(
             type_=String,
             index=True))
     email: str = Field(sa_column=Column(
             type_=String,
             index=True,
             unique=True))


class Users(BaseUsers, table=True):
     __tablename__ = 'users'
     id: str = Field(default=str(uuid.uuid4()), primary_key=True, index=True)
     role: str = Field(default='user')
     hash_password: str = Field()
     status: str = Field(default='pending', index=True)


class CreateUser(BaseUsers):
     password: str
