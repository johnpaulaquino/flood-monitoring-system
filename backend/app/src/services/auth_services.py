from fastapi import HTTPException, status
from starlette.responses import JSONResponse

from app.src.database.models import Users
from app.src.database.models.users_model import CreateUser
from app.src.database.repositories.user_repository import UserRepository
from app.src.security.auth_security import AuthSecurity


class UserServices:

     @staticmethod
     async def create_user_account(user_: CreateUser):
          """
          To create a user account. Create first, before create its personal information.
          :param user_: that contains the credentials of a user to be insert in database.
          :return: New User
          """
          try:
               # retrieved data
               data = await UserRepository.find_user_by_email(user_.email)
               # check if data exists.
               if data:
                    if data.status:
                         raise HTTPException(
                                 status_code=status.HTTP_200_OK,
                                 detail={'status' : 'ok',
                                         'message': 'User is already exist but not verified yet!'})
                    # return JSONResponse
                    raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail={'status' : 'failed',
                                     'message': 'User is already exist'})
               # hash password
               hashed_password = AuthSecurity.hash_password(user_.password)
               # Set the arguments for User object
               new_user = Users(email=user_.email, username=user_.username, hash_password=hashed_password)

               await UserRepository.create_user(new_user)
               # return new User
               return new_user
          except Exception as e:
               # if encountered error, then raise it
               raise e

     @staticmethod
     async def activate_user_account(token: str):
          """
          To activate user account based on his/her email.
          :param token:
          :return: email
          """
          try:

               payload = AuthSecurity.decode_jwt_token(token)
               original_data = AuthSecurity.decrypt_data(payload)
               data = await UserRepository.find_user_by_email(original_data['user_email'])
               if not data:
                    raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail={'status': 'failed', 'message': 'Email is not found'},
                    )
               return data.email
          except Exception as e:
               raise e
