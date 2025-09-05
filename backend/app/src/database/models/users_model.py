from sqlmodel import Column, Field, SQLModel


class BaseUsers(SQLModel):
     username: str = Field(sa_column=Column(
             index=True))
     email: str = Field(sa_column=Column(
             index=True,
             unique=True))
     role = str = Field(default='user')


class Users(SQLModel, table=True):
     __tablename__ = 'users'
     id: int = Field(primary_key=True, index=True)
     hash_password: str = Field()
