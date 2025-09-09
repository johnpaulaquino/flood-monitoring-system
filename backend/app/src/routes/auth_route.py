import requests
from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from starlette.responses import JSONResponse, RedirectResponse

from app.config.settings import Settings
from app.src.database.models import Users
from app.src.database.models.users_model import CreateUser
from app.src.database.repositories.user_repository import UserRepository
from app.src.security.auth_security import AuthSecurity
from app.src.services.user_services import UserServices

auth_router = APIRouter(
        prefix='/api/v1/auth', )

settings = Settings()


@auth_router.post('/create-account')
async def create_account(user_: CreateUser, background_task: BackgroundTasks):
     try:
          return await UserServices.create_user_account(user_, background_task)
     except Exception as e:
          raise e


@auth_router.get("/login/google")
async def login_via_google():
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
               return JSONResponse(
                       status_code=status.HTTP_400_BAD_REQUEST,
                       content={'status': 'failed', 'message': 'Failed to retrieve id token'})

          user_info = jwt.get_unverified_claims(token_response["id_token"])

          user_email = user_info['email']
          username = user_info['name']
          given_name = user_info['given_name']
          family_name = user_info['family_name']

          user_data = {'user_email': user_email}

          data = await UserRepository.find_user_by_email(user_email)

          new_user = Users(username=username, email=user_email)
          # if not exist which is signup

          if not data:
               await UserRepository.create_user(new_user)
               return JSONResponse(
                       status_code=status.HTTP_201_CREATED,
                       content={'status': 'ok', 'message': 'Successfully created account',
                                'action': 'signup'})

          # otherwise login
          to_encode = {'user_id'            : data.id,
                       'profile_setup_steps': data.profile_setup_steps,
                       'user_status'        : data.status}

          data_refresh_token = {'user_id': data.id, 'user_email': data.email}
          generated_access_token = AuthSecurity.generate_access_token(to_encode)

          return JSONResponse(
                  status_code=status.HTTP_200_OK,
                  content={'status'              : 'ok',
                           'action'              : 'login',
                           'access_token'        : generated_access_token,
                           'refresh_access_token': data_refresh_token,
                           'access_type'         : 'bearer'}, )

     except Exception as e:
          raise e


@auth_router.post('/login')
async def manual_login(data_form: OAuth2PasswordRequestForm = Depends()):
     try:
          user_ = await UserRepository.find_user_by_email(data_form.username)
          if not user_:
               return JSONResponse(
                       status_code = status.HTTP_404_NOT_FOUND,
                       content={'status':'failed','message': "User not found"},
               )
     except Exception as e:
          raise e
