from authlib.jose import jwt
from fastapi import BackgroundTasks, status
from fastapi.params import Depends
from starlette.responses import JSONResponse

from app.config.settings import Settings
from app.src.database.models.users_model import CreateUser
from app.src.database.repositories.user_repository import UserRepository
from app.src.security.auth_security import AuthSecurity
from app.src.services.auth_services import UserServices
from app.src.services.email_services import EmailServices
import socket


settings = Settings()

class AuthController:

     @staticmethod
     async def create_user_account(user_: CreateUser, background_task: BackgroundTasks):
          try:
               ip_address = socket.gethostbyaddr(socket.gethostname())[2]

               # already inserted in database,
               new_user = await UserServices.create_user_account(user_)

               generated_token = AuthSecurity.generate_access_token({"user_email": new_user.email})

               url_link_for_activation = f"http://192.168.7.52:9090/api/v1/auth/activate/account?token={generated_token}"

               background_task.add_task(EmailServices.send_message_via_clicking, user_.email, url_link_for_activation)
               # return JSONResponse
               return JSONResponse(
                       status_code=status.HTTP_201_CREATED,
                       content={'status': 'ok', 'message': 'Successfully account created. Please go to your email to verify your account.'},
               )
          except Exception as e:
               raise e

     @staticmethod
     async def google_callback(code: str):
          try:
               pass
          except Exception as e:
               raise e

     @staticmethod
     async def activate_user_account(token: str):
          try:
               email = await UserServices.activate_user_account(token)
               await UserRepository.activate_user_account(email)
          except Exception as e:
               raise e
