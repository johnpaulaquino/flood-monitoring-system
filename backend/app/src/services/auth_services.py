import socket
import subprocess

import requests
from fastapi import BackgroundTasks, HTTPException, status
from jose import jwt
from starlette.responses import JSONResponse

from app.config.settings import Settings
from app.src.database.models import Users
from app.src.database.models.users_model import CreateUser
from app.src.database.repositories.user_repository import UserRepository
from app.src.security.auth_security import AuthSecurity
from app.src.services.email_services import EmailServices

settings = Settings()


class AuthServices:

     @staticmethod
     async def create_user_account(user_: CreateUser, background_task: BackgroundTasks):
          """
          To create a user account. Create first, before create its personal information.
          :param user_: that contains the credentials of a user to be insert in database.
          :param background_task: to send email without delaying the process of sending email.
          :return: JSONResponse
          """
          try:
               # retrieved data
               data = await UserRepository.find_user_by_email(user_.email)
               # check if data exists.
               if data:
                    if data.status =='pending':
                         return JSONResponse(
                                 status_code=status.HTTP_200_OK,
                                 content={'status' : 'ok',
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

               # Insert in database
               await UserRepository.create_user(new_user)

               # generate token that will send to param
               generated_token = AuthSecurity.generate_access_token({"user_email": new_user.email})

               # For localhost only when try to access in phone
               ip_localhost_for_mobile = AuthSecurity.get_local_ip()

               # API Endpoint where to activate the user account
               url_link_for_activation = f"http://{ip_localhost_for_mobile}:{settings.SERVER_PORT}/api/v1/auth/activate/account?token={generated_token}"

               # send the activation link in email
               background_task.add_task(EmailServices.send_message_via_clicking, user_.email, url_link_for_activation)
               # return JSONResponse
               return JSONResponse(
                       status_code=status.HTTP_201_CREATED,
                       content={'status' : 'ok',
                                'message': 'Successfully account created. Please go to your email to verify your account.'},
               )
          except Exception as e:
               # if encountered error, then raise it
               raise e

     @staticmethod
     async def oauth_callback(code: str):
          try:
               token_url = "https://oauth2.googleapis.com/token"
               token_data = {
                       "code"         : code,
                       "client_id"    : settings.GOOGLE_CLIENT_ID,
                       "client_secret": settings.GOOGLE_CLIENT_SECRET,
                       "redirect_uri" : settings.REDIRECT_URI,
                       "grant_type"   : "authorization_code",
               }

               token_response = requests.post(token_url, data=token_data).json()
               if "id_token" not in token_response:
                    raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail={'status': 'failed', 'message': 'Failed to retrieve id token'})

               user_info = jwt.get_unverified_claims(token_response["id_token"])

               user_email = user_info['email']
               username = user_info['name']

               # get user
               data = await UserRepository.find_user_by_email(user_email)

               # initialize User to be inserted in database if data is null or empty
               new_user = Users(username=username, email=user_email)
               # if not exist which is signup
               if not data:
                    # Insert User in database
                    await UserRepository.create_user(new_user)
                    return JSONResponse(
                            status_code=status.HTTP_201_CREATED,
                            content={'status': 'ok', 'message': 'Successfully created account',
                                     'action': 'signup'})
               # otherwise login
               to_encode = {'user_id'            : data.id,
                            'profile_setup_steps': data.profile_setup_steps,
                            'user_status'        : data.status}

               # generate access and refresh token
               data_refresh_token = {'user_id': data.id, 'user_email': data.email}
               generated_access_token = AuthSecurity.generate_access_token(to_encode)
               generated_refresh_access_token = AuthSecurity.generate_refresh_token(data_refresh_token)

               # return response
               return JSONResponse(
                       status_code=status.HTTP_200_OK,
                       content={'status'              : 'ok',
                                'action'              : 'login',
                                'access_token'        : generated_access_token,
                                'refresh_access_token': generated_refresh_access_token,
                                'access_type'         : 'bearer'}, )
          except Exception as e:
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
               # then update user
               await UserRepository.activate_user_account(data.email)
               #return email address
               return data.email
          except Exception as e:
               raise e
