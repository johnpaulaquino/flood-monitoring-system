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
     id: str = Field(default_factory=lambda : str(uuid.uuid4()), primary_key=True, index=True)
     role: str = Field(default='user')
     password: str = Field(default=None, nullable=True)
     status: str = Field(default='pending', index=True)
     is_profile_completed: bool = Field(default=False)
     # 1 Email Verification
     # 2 Setup password
     # 3 Personal Information
     # 4 Address
     profile_setup_steps: int = Field(default=1)


class CreateUser(BaseUsers):
     password: str
