from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile

from app.src.constants import API_PREFIX
from app.src.database.models.announcements_model import CreateAnnouncements, UpdateAnnouncements
from app.src.dependencies.auth_dependencies import AuthDependency
from app.src.schema import Paginated
from app.src.services.announcements_services import AnnouncementsServices

announcements_router = APIRouter(
        prefix=f"{API_PREFIX}/announcements",
        tags=['Announcements'])


@announcements_router.post('/create')
async def create_announcements(
        background_task: BackgroundTasks,
        announcement: CreateAnnouncements = Depends(CreateAnnouncements.create_announcements_as_body_form),
        curr_user=Depends(AuthDependency.get_current_user),
        img_file: Optional[UploadFile] = File(None)):
     """
     TO Create announcement
     :param background_task: to send the process in background to not delay the other process
     :param announcement: this is the data to be inserted in database
     :param curr_user: to get the current user based on the token
     :param img_file: the file to be upload in server
     :return: JSONResponse
     """
     try:

          return await AnnouncementsServices.create_announcement(announcement, curr_user, background_task, img_file)
     except Exception as e:
          raise e


@announcements_router.get('/')
async def get_ten_announcements(current_user=Depends(AuthDependency.get_current_user)):
     try:

          return await AnnouncementsServices.get_ten_announcements(current_user)
     except Exception as e:
          raise e


@announcements_router.get('/paginated/')
async def get_ten_announcements(paginated: Paginated = Depends(),
                                current_user=Depends(AuthDependency.get_current_user)):
     try:
          return await AnnouncementsServices.paginated_announcements(paginated, current_user)
     except Exception as e:
          raise e


@announcements_router.put('/{announcement_id}')
async def create_announcements(announcement_id,
                               update_announcement: UpdateAnnouncements = Depends(
                                       UpdateAnnouncements.update_announcements_as_body_form),
                               img_file: Optional[UploadFile] = File(None),
                               current_user=Depends(AuthDependency.get_current_user)):
     try:
          print(update_announcement.model_dump())
          return await AnnouncementsServices.update_announcements(update_announcement, announcement_id, current_user)

     except Exception as e:
          raise e


@announcements_router.delete('/{announcement_id}')
async def delete_announcement(announcement_id: str, curr_user=Depends(AuthDependency.get_current_user)):
     try:
          return await AnnouncementsServices.delete_announcement(announcement_id, curr_user)
     except Exception as e:
          raise e
