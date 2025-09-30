from typing import Optional

from fastapi import BackgroundTasks, File, HTTPException, status, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.src.database.models import Announcements
from app.src.database.models.announcements_model import CreateAnnouncements, UpdateAnnouncements
from app.src.database.repositories.announcements_repository import AnnouncementsRepository
from app.src.schema import Paginated
from app.src.services.cloudinary_services import CloudinaryServices
from app.src.utils.global_utils import GlobalUtils


class AnnouncementsServices:

     @staticmethod
     async def create_announcement(announcement: CreateAnnouncements,
                                   curr_user,
                                   background_task: BackgroundTasks,
                                   img_file: Optional[UploadFile] = File(None)):
          try:
               new_announcement = Announcements(**announcement.model_dump(exclude_unset=True))
               user_id = curr_user['id']
               profile_old_profile_picture = curr_user['ProfileImage'].model_dump().get('public_key') if curr_user[
                    'ProfileImage'] else None
               new_announcement.user_id = user_id
               await AnnouncementsRepository.create_announcement(new_announcement, user_id)

               # update announcement picture if picture is provided
               if GlobalUtils.is_file_uploaded(img_file=img_file):
                    filename = img_file.filename
                    background_task.add_task(CloudinaryServices.update_image_file, user_id,
                                             filename,
                                             profile_old_profile_picture,
                                             img_file,
                                             False)
               return JSONResponse(
                       status_code=status.HTTP_201_CREATED,
                       content={'status': 'ok', 'message': 'Successfully created announcement'},
               )

          except Exception as e:
               raise e

     @staticmethod
     async def get_ten_announcements(current_user):
          try:
               user_id = current_user['id']
               data = await AnnouncementsRepository.get_ten_announcements(user_id)

               validated_data = jsonable_encoder(data)
               return JSONResponse(
                       status_code=status.HTTP_200_OK,
                       content={'status' : 'ok',
                                'message': 'Successfully retrieve',
                                'data'   : validated_data})
          except Exception as e:
               raise e

     @staticmethod
     async def paginated_announcements(paginated: Paginated, current_user):
          try:
               user_id = current_user['id']
               offset = GlobalUtils.get_offset(paginated.skip, paginated.limit)
               data = await AnnouncementsRepository.get_paginated_announcements(user_id, offset, paginated.limit)
               validated_data = jsonable_encoder(data)
               return JSONResponse(
                       status_code=status.HTTP_200_OK,
                       content={'status': 'ok', 'message': 'Successfully retrieved',
                                'data'  : validated_data})
          except Exception as e:
               raise e

     @staticmethod
     async def update_announcements(announcement: UpdateAnnouncements, announcement_id, current_user):
          try:
               user_id = current_user['id']
               data = await AnnouncementsRepository.get_specific_announcement(user_id, announcement_id)
               if not data:
                    raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail={'status': 'fail', 'message': 'Announcement not found'},
                    )

               await AnnouncementsRepository.update_announcements(user_id, announcement_id, announcement)
               return JSONResponse(
                       status_code=status.HTTP_200_OK,
                       content={'status': 'ok', 'message': 'Successfully updated'})
          except Exception as e:
               raise e

     @staticmethod
     async def delete_announcement(announcement_id, curr_user):
          try:
               user_id = curr_user['id']
               data = await AnnouncementsRepository.get_specific_announcement(user_id, announcement_id)
               if not data:
                    raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail={'status': 'fail', 'message': 'Announcement not found'},
                    )
               await AnnouncementsRepository.delete_announcement(user_id, announcement_id)
               return JSONResponse(
                       status_code=status.HTTP_200_OK,
                       content={'status': 'ok', 'message': 'Successfully deleted'})
          except Exception as e:
               raise e
