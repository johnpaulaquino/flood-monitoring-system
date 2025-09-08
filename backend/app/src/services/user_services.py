from fastapi import BackgroundTasks, status
from starlette.responses import JSONResponse

from app.src.database.models import Users
from app.src.database.models.users_model import CreateUser
from app.src.database.repositories.user_repository import UserRepository
from app.src.services.email_services import EmailServices
from app.src.utils.auth_utils import AuthUtils


class UserServices:

     @staticmethod
     async def create_user_account(user_: CreateUser,background_task : BackgroundTasks):
          """
          To create a user account. Create first, before create its personal information.
          :param user_: that contains the credentials of a user to be insert in database.
          :return: JsonResponse
          """
          try:
               #retrieved data
               data = await UserRepository.find_user_by_email(user_.email)
               #check if data exists.
               if data:
                    #return JSONResponse
                    return JSONResponse(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            content={'status' : 'failed',
                                     'message': 'User is already exist'})
               #hash password
               hashed_password = AuthUtils.hash_password(user_.password)
               #Set the arguments for User object
               new_user = Users(email=user_.email, username=user_.username, hash_password=hashed_password)
               #insert in database
               await UserRepository.create_user(new_user)

               #send verification email and add in task to not interrupt the speed of response.
               await EmailServices.send_message(user_.email)
               #return JSONResponse
               return JSONResponse(
                       status_code=status.HTTP_201_CREATED,
                       content={'status': 'ok', 'message': 'Successfully Created!'},
               )
          except Exception as e:
               #if encountered error, then raise it
               raise e

     @staticmethod
     async def activate_user_account(email: str):
          """
          To activate user account based on his/her email.
          :param email: is a unique to user to activate her/his account.
          :return: JSONResponse
          """
          try:
               data = await UserRepository.find_user_by_email(email)
               if not data:
                    return JSONResponse(
                            status_code=status.HTTP_404_NOT_FOUND,
                            content={'status': 'failed', 'message': 'Email is not found'},
                    )
               await UserRepository.active_user_account(email)
               return JSONResponse(
                       status_code=status.HTTP_200_OK,
                       content={'status': 'ok', 'message': 'Successfully updated user account'},
               )
          except Exception as e:
               raise e
     