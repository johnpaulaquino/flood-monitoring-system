from datetime import date

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import ExpiredSignatureError
from starlette.responses import JSONResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from app.config.settings import Settings
from app.src.database.models.users_model import CreateUser
from app.src.database.repositories.user_repository import UserRepository
from app.src.security.auth_security import AuthSecurity
from app.src.services.auth_services import AuthServices

auth_router = APIRouter(
        prefix='/api/v1/auth',
        tags=['Authentication'])

settings = Settings()

templates = Jinja2Templates(directory=settings.TEMPLATE_PATH)


@auth_router.post('/create-account')
async def create_account(background_task: BackgroundTasks, user_: CreateUser):
     try:
          return await AuthServices.create_user_account(user_, background_task)
     except Exception as e:
          raise e


@auth_router.get("/google")
async def login_via_google():
     """

     :return:
     """
     google_auth_url = (
             "https://accounts.google.com/o/oauth2/v2/auth"
             f"?client_id={settings.GOOGLE_CLIENT_ID}"
             f"&redirect_uri={settings.REDIRECT_URI}"
             "&response_type=code"
             "&scope=openid%20email%20profile"
     )
     return RedirectResponse(url=google_auth_url)


@auth_router.get('/google/callback')
async def oauth_callback(code: str):
     """
     A function that retrieve the data after successful linked account in google.
     :param code: a unique code that response from Google auth
     :return: JSON Response
     """
     try:
          return await AuthServices.oauth_callback(code)
     except Exception as e:
          raise e


@auth_router.post('/login')
async def manual_login(data_form: OAuth2PasswordRequestForm = Depends()):
     """
     Allow users to login manually by inputting their email and password, then once
     the credentials is verified it will return a response including the access token
     and refresh token.

     :param data_form: is a form that allow the users to input username and password for
     authenticating.
     :return: JSONResponse
     """
     try:
          # retrieve user data first
          user_ = await UserRepository.find_user_by_email(data_form.username)
          # check if user exists
          if not user_:
               raise HTTPException(
                       status_code=status.HTTP_404_NOT_FOUND,
                       detail={'status': 'failed', 'message': "User not found"},
                       headers={'WWW-Authenticate': "Bearer"},
               )
          # check if user is verified
          if user_.status == "pending":
               raise HTTPException(
                       status_code=status.HTTP_400_BAD_REQUEST,
                       detail={'status': 'failed', 'message': "Please verify your email first "},
                       headers={'WWW-Authenticate': "Bearer"},
               )
          # check if user password is none
          if user_.hash_password is None:
               return JSONResponse(
                       status_code=status.HTTP_400_BAD_REQUEST,
                       content={'status': 'failed', 'message': "Please change your password"},
                       headers={'WWW-Authenticate': "Bearer"},
               )
          # check if provided password is match to the hash password is db
          if not AuthSecurity.verify_hashed_password(data_form.password, user_.hash_password):
               raise HTTPException(
                       status_code=status.HTTP_400_BAD_REQUEST,
                       detail={'status': 'failed', 'message': "Incorrect password"},
                       headers={'WWW-Authenticate': "Bearer"})

          # if passed to all condition, then generate an access and refresh token
          to_encode = {"user_id": user_.id}
          to_encode_refresh_token = {"user_id": user_.id, 'user_email': user_.email}
          generated_access_token = AuthSecurity.generate_access_token(to_encode)
          generated_refresh_access_token = AuthSecurity.generate_refresh_token(to_encode_refresh_token)

          # return response
          return JSONResponse(
                  status_code=status.HTTP_200_OK,
                  content={"access_token"        : generated_access_token,
                           "access_type"         : "bearer",
                           "refresh_access_token": generated_refresh_access_token})

     except Exception as e:
          # if encountered error, then raise it
          raise e


@auth_router.get('/activate/account')
async def activate_user_account(request: Request, token: str):
     try:
          # activate account then return the html website
          email_address = await AuthServices.activate_user_account(token)

          contex = {'email_address':email_address,
                    'date_today':date.today()}
          return templates.TemplateResponse(request=request,context=contex, name="verified-account.html")
     except ExpiredSignatureError as ex:
          return templates.TemplateResponse(request=request, name="failed-account-verification.html")
     except Exception as e:
          return templates.TemplateResponse(request=request, name="failed-account-verification.html")
