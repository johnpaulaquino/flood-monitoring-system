from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile

from app.src.database.models.address_model import UpdateAddress
from app.src.database.models.personal_information_models import UpdatePersonalInformation
from app.src.dependencies.auth_dependencies import AuthDependency
from app.src.services.user_services import UserServices

user_router = APIRouter(
        prefix='/api/v1/user',
        tags=['User'])


@user_router.put('/address')
async def update_user_address(address=Depends(UpdateAddress.update_schema),
                              current_user: str = Depends(AuthDependency.get_current_user)):
     try:

          return await UserServices.update_user_address(address, current_user)

     except Exception as e:
          raise e


@user_router.put('/profile-image')
async def update_profile_image(background_task: BackgroundTasks,
                               current_user=Depends(AuthDependency.get_current_user),
                               image_file: UploadFile = File(None)):
     try:
          return await UserServices.update_user_profile_image(background_task, current_user, image_file)
     except Exception as e:
          raise e


@user_router.put('/personal-info')
async def update_personal_information(current_user=Depends(AuthDependency.get_current_user),
                                      personal_information=Depends(
                                              UpdatePersonalInformation.update_personal_info_schema)):
     try:
          return await UserServices.update_user_personal_information(current_user, personal_information)
     except Exception as e:
          raise e
