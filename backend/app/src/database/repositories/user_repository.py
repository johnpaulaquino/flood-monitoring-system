import asyncio

from sqlmodel import delete, select, update

from app.src.database.engine_creator import create_session
from app.src.database.models import Address, PersonalInformation, ProfileImage, Users
from app.src.database.models.address_model import UpdateAddress
from app.src.database.models.profile_img_model import UpdateProfileImage
from app.src.security.auth_security import AuthSecurity


class UserRepository:
     @staticmethod
     async def create_user(user: Users):
          async with create_session() as db:
               try:
                    db.add(user)
                    await db.flush()

                    # add the user_id in address and profile pic for the mean time.
                    address = Address(user_id=user.id)
                    profile_pic = ProfileImage(user_id=user.id)
                    personal_info = PersonalInformation(user_id=user.id)
                    # add in database
                    db.add_all([address, profile_pic, personal_info])
                    # commit the transaction
                    await db.commit()
                    # refresh the user
                    await db.refresh(user)
               except Exception as e:
                    # rollback the transaction if error occurred
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
                    stmt = (select(Users.email,Users.id,Users.username,Users.status,
                                   PersonalInformation, Address, ProfileImage)
                    .outerjoin(PersonalInformation, Users.id == PersonalInformation.user_id)
                    .outerjoin(Address, Users.id == Address.user_id)
                    .outerjoin(ProfileImage, Users.id == ProfileImage.user_id)
                    .where(
                            Users.id == user_id))
                    result = await db.execute(stmt)
                    data = result.mappings().unique().all()
                    return data[0]
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
     async def activate_user_account(email: str):
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
          """
          To delete user
          :param user_id: a unique id for every user.
          :return:  Nothing
          """
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
          """
          To update password
          :param email: is the unique credentials to update the password
          :param new_password: To be hashed and store in db.
          :return:
          """
          async with create_session() as db:
               try:
                    hashed_new_password = AuthSecurity.hash_password(new_password)
                    stmt = update(Users).values(
                            hash_password=hashed_new_password,
                    ).where(Users.email == email)

                    await db.execute(stmt)
                    await db.commit()
               except Exception as e:
                    await db.rollback()
                    raise e

     # Address
     @staticmethod
     async def update_address(user_id: str, address: UpdateAddress):
          async with create_session() as db:
               try:
                    # update statement
                    stmt = update(Address).values(address).where(Address.user_id == user_id)
                    # execute the stmt
                    await db.execute(stmt)
                    # commit the transaction
                    await db.commit()
               except Exception as e:
                    # rollback the transaction if error occurred
                    await db.rollback()
                    raise e

     @staticmethod
     async def update_personal_information(user_id: str, personal_info: PersonalInformation):
          async with create_session() as db:
               try:
                    stmt = update(PersonalInformation).values(
                         personal_info
                    ).where(PersonalInformation.user_id == user_id)
                    await db.execute(stmt)
                    await db.commit()
               except Exception as e:
                    await db.rollback()
                    raise e

     @staticmethod
     async def update_profile_image(user_id: str, prof_image: UpdateProfileImage):
          async with create_session() as db:
               try:
                    stmt = update(ProfileImage).values(
                            prof_image
                    ).where(ProfileImage.user_id == user_id)
                    await db.execute(stmt)
                    await db.commit()
               except Exception as e:
                    await db.rollback()
                    raise e
