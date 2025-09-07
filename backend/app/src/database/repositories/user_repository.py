from sqlalchemy.testing.pickleable import User
from sqlmodel import delete, select

from app.src.database.engine_creator import create_session
from app.src.database.models import Address, PersonalInformation, ProfileImage, Users


class UserRepository:
     @staticmethod
     async def create_user(user: Users):
          async with create_session() as db:
               try:
                    db.add(user)
                    await db.commit()
                    await db.refresh()
               except Exception as e:
                    await db.rollback()
                    raise e

     @staticmethod
     async def find_user_by_email(email: str):
          async with create_session() as db:
               try:
                    stmt = select(User).where(Users.email == email)
                    result = await db.execute(stmt)
                    data = result.scalar()
                    return data
               except Exception as e:
                    raise e

     @staticmethod
     async def find_user_by_display_id(display_id: str):
          async with create_session() as db:
               try:
                    stmt = (select(Users, PersonalInformation, Address, ProfileImage)
                    .outerjoin(PersonalInformation, Users.id == PersonalInformation.user_id)
                    .outerjoin(Address, Users.id == Address.user_id)
                    .outerjoin(ProfileImage, Users.id == ProfileImage.user_id)
                    .where(
                            Users.display_id == display_id))
                    result = await db.execute(stmt)
                    data = result.mappings().unique().all()
                    return data
               except Exception as e:
                    raise e

     @staticmethod
     async def update_user(display_id: str, user: Users):
          async with create_session() as db:
               try:
                    pass
               except Exception as e:
                    raise e

     @staticmethod
     async def delete_user(display_id: str):
          async with create_session() as db:
               try:
                    stmt = delete(Users).where(Users.display_id == display_id)
                    await db.execute(stmt)
                    await db.commit()
               except Exception as e:
                    await db.rollback()
                    raise e
