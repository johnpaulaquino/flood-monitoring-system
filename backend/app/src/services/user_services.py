from fastapi import BackgroundTasks, File, HTTPException, status, UploadFile
from starlette.responses import JSONResponse

from app.src.database.models import PersonalInformation
from app.src.database.models.address_model import UpdateAddress
from app.src.database.models.personal_information_models import UpdatePersonalInformation
from app.src.database.repositories.user_repository import UserRepository
from app.src.services.cloudinary_services import CloudinaryServices
from app.src.utils.global_utils import GlobalUtils

class UserServices:

     @staticmethod
     async def update_user_address(address: UpdateAddress, current_user):
          try:
               data = await UserRepository.find_user_by_id(current_user)
               if not data:
                    raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail={'status': 'ok', 'message': 'User not found'})

               # This is an object who contains the old address
               old_address: UpdateAddress = data["Address"]

               # Update the Object by updating through mapping
               updated_address = old_address.model_copy(
                       update=address.model_dump(exclude_unset=True, exclude_none=True))

               # then update the data in database
               await UserRepository.update_address(current_user, updated_address.model_dump())
               return JSONResponse(
                       status_code=status.HTTP_200_OK,
                       content={'status': 'ok', 'message': 'Successfully updated'})
          except Exception as e:
               raise e

     @staticmethod
     async def update_user_profile_image(background_task: BackgroundTasks,
                                         current_user,
                                         image_file: UploadFile = File(None),
                                         ):
          try:
               data = await UserRepository.find_user_by_id(current_user)
               if not data:
                    raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail={'status': 'ok', 'message': 'User not found'})

               profile_old_profile_picture = data['ProfileImage'].public_key
               if not GlobalUtils.is_file_uploaded(img_file=image_file):
                    return JSONResponse(
                            status_code=status.HTTP_200_OK,
                            content={'status': 'ok', 'message': 'No changes made'})
               filename = image_file.filename
               background_task.add_task(CloudinaryServices.update_image_file,
                                        current_user,
                                        filename,
                                        profile_old_profile_picture,
                                        image_file.file.read())
               return JSONResponse(
                       status_code=status.HTTP_200_OK,
                       content={'status': 'ok', 'message': 'Successfully updated profile picture'})

          except Exception as e:
               raise e

     @staticmethod
     async def update_user_personal_information(current_user,
                                                personal_information: UpdatePersonalInformation):
          try:
               # get the data
               data = await UserRepository.find_user_by_id(current_user)
               # check if not exist
               if not data:
                    # then raise an error
                    raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail={"status": 'fail', 'message': 'User not found'},
                    )
               # check if all fields in schema is null or not set
               to_inserted = personal_information.model_dump(exclude_none=True, exclude_unset=True)
               if not to_inserted:
                    # then return JSONResponse
                    return JSONResponse(
                            status_code=status.HTTP_200_OK,
                            content={'status': 'ok', 'message': 'No changes made'},
                    )
               # set age
               new_age = 0
               # check if birthdate is set on schema
               if personal_information.birthdate:
                    # then calculate age
                    new_age = GlobalUtils.calculate_age(personal_information.birthdate)

               # then get the old personal info
               old_personal_info: PersonalInformation = data['PersonalInformation']
               # then copy it and update the value based on the schema
               new_data = old_personal_info.model_copy(
                       update=personal_information.model_dump(exclude_unset=True,
                                                              exclude_none=True))
               # check if the age is not less than to 0
               if new_age > 0:
                    # then set new age
                    new_data.age = new_age

               # update the personal information in database
               await UserRepository.update_personal_information(current_user, new_data.model_dump())
               # then return Response
               return JSONResponse(
                       status_code=status.HTTP_200_OK,
                       content={'status': 'ok', 'message': 'Successfully updated personal information'},
               )
          except Exception as e:
               raise e
