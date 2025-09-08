from sqlalchemy.testing.pickleable import User
from sqlmodel import delete, select, update

from app.src.database.engine_creator import create_session
from app.src.database.models import Address, PersonalInformation, ProfileImage, Users
from app.src.utils.auth_utils import AuthUtils


class UserRepository:
     @staticmethod
     async def create_user(user: Users):
          async with create_session() as db:
               try:
                    db.add(user)
                    await db.commit()
                    await db.refresh(user)
               except Exception as e:
                    await db.rollback()
                    raise e

     @staticmethod
     async def find_user_by_email(email: str):
          async with create_session() as db:
               try:
                    stmt = select(Users).where(Users.email == email)
                    result = await db.execute(stmt)
                    data = result.scalar()
                    return data
               except Exception as e:
                    raise e

     @staticmethod
     async def find_user_by_id(user_id: str):
          async with create_session() as db:
               try:
                    stmt = (select(Users, PersonalInformation, Address, ProfileImage)
                    .outerjoin(PersonalInformation, Users.id == PersonalInformation.user_id)
                    .outerjoin(Address, Users.id == Address.user_id)
                    .outerjoin(ProfileImage, Users.id == ProfileImage.user_id)
                    .where(
                            Users.id == user_id))
                    result = await db.execute(stmt)
                    data = result.mappings().unique().all()
                    return data
               except Exception as e:
                    raise e

     @staticmethod
     async def update_user(user_id: str, user: Users):
          async with create_session() as db:
               try:
                    pass
               except Exception as e:
                    raise e

     @staticmethod
     async def active_user_account(email: str):
          """
          To mark the user as activated.
          :param email: is a unique from user to activate his/her account.
          :return: nothing.
          """
          async with create_session() as db:
               try:
                    stmt = update(Users).values(status='activated').where(Users.email == email)
                    await db.execute(stmt)
                    await db.commit()
               except Exception as e:
                    await db.rollback()
                    raise e

     @staticmethod
     async def delete_user(user_id: str):
          async with create_session() as db:
               try:
                    stmt = delete(Users).where(Users.id == user_id)
                    await db.execute(stmt)
                    await db.commit()
               except Exception as e:
                    await db.rollback()
                    raise e

     @classmethod
     async def update_password(cls, email: str, new_password: str):
          async with create_session() as db:
               try:
                    hashed_new_password = AuthUtils.hash_password(new_password)
                    stmt = update(Users).values(
                            hash_password=hashed_new_password,
                    ).where(Users.email == email)

                    await db.execute(stmt)
                    await db.commit()
               except Exception as e:
                    await db.rollback()
                    raise e

     @staticmethod
     async def update_address(user_id: str, address: Address):
          async with create_session() as db:
               try:
                    stmt = update(Address).values(
                            barangay=address.barangay,
                            city=address.city,
                            municipality=address.municipality,
                            province=address.province,
                    ).where(address.user_id == user_id)
                    await db.execute(stmt)
                    await db.commit()
               except Exception as e:
                    await db.rollback()
                    raise e

     @staticmethod
     async def update_personal_information(user_id: str, personal_info: PersonalInformation):
          async with create_session() as db:
               try:
                    stmt = update(PersonalInformation).values(
                            age=personal_info.age,
                            gender=personal_info.gender,
                            birthdate=personal_info.birthdate,
                            firstname=personal_info.firstname,
                            middle_name=personal_info.middle_name,
                            last_name=personal_info.last_name,
                    ).where(PersonalInformation.user_id == user_id)
                    await db.execute(stmt)
                    await db.commit()
               except Exception as e:
                    await db.rollback()
                    raise e

     @staticmethod
     async def update_profile_image(user_id: str, prof_image: ProfileImage):
          async with create_session() as db:
               try:
                    stmt = update(ProfileImage).values(
                            img_url=prof_image.img_url,
                            public_key=prof_image.public_key,
                    ).where(ProfileImage.user_id == user_id)
                    await db.execute(stmt)
                    await db.commit()
               except Exception as e:
                    await db.rollback()
                    raise e
