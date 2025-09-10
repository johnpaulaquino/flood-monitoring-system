from fastapi import BackgroundTasks, status
from starlette.responses import JSONResponse

from app.src.database.models.users_model import CreateUser
from app.src.database.repositories.user_repository import UserRepository
from app.src.security.auth_security import AuthSecurity
from app.src.services.auth_services import UserServices
from app.src.services.email_services import EmailServices


class AuthController:

     @staticmethod
     async def create_user_account(user_: CreateUser, background_task: BackgroundTasks):
          try:
               # already inserted in database,
               new_user = await UserServices.create_user_account(user_)

               generated_token = AuthSecurity.generate_access_token({"user_email":new_user.email})

               url_link_for_activation = f"http://127.0.0.1:9090/api/v1/auth/activate/account?token={generated_token}"

               background_task.add_task(EmailServices.send_message_via_clicking, user_.email, url_link_for_activation)
               # return JSONResponse
               return JSONResponse(
                       status_code=status.HTTP_201_CREATED,
                       content={'status': 'ok', 'message': 'Successfully Created!'},
               )
          except Exception as e:
               raise e

     @staticmethod
     async def activate_user_account(email: str):
          try:
               await UserRepository.activate_user_account(email)
               return JSONResponse(
                       status_code=status.HTTP_200_OK,
                       content={'status': 'ok', 'message': 'Successfully updated user account'},
               )
          except Exception as e:
               raise e
