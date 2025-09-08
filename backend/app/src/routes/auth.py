from fastapi import APIRouter, BackgroundTasks

from app.src.database.models.users_model import CreateUser
from app.src.services.user_services import UserServices

auth_router = APIRouter(
        prefix='/api/v1/auth', )


@auth_router.post('/create-account')
async def create_account(user_: CreateUser, background_task: BackgroundTasks):
     try:
          return await UserServices.create_user_account(user_,background_task)
     except Exception as e:
          raise e
