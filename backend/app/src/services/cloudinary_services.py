import asyncio
import os.path

import cloudinary
import cloudinary.uploader
from fastapi import File, UploadFile

from app.config.settings import Settings
from app.src.database.models.profile_img_model import UpdateProfileImage
from app.src.database.repositories.user_repository import UserRepository

settings = Settings()

# configure the credentials needed to connect in cloudinary
cloudinary.config(
        cloud_name=settings.C_NAME,
        api_key=settings.C_KEY,
        api_secret=settings.C_SECRET,
        secure=settings.C_SECURE,
)


class CloudinaryServices:

     @staticmethod
     async def upload_image(url_img, public_id: str, is_profile_picture) -> str:

          # upload the image in cloudinary
          asset_folder = 'fms/display-photo'
          if not is_profile_picture:
               asset_folder = 'fms/announcements-photos'
          result = await asyncio.to_thread(cloudinary.uploader.upload,
                                           url_img,
                                           public_id=public_id,
                                           overwrite=True,
                                           secure=True,
                                           asset_folder=asset_folder,
                                           resource_type="image",
                                           )
          # get the url of the uploaded image
          url = result.get("secure_url")
          # then return it
          return url

     @staticmethod
     async def update_image_file(current_user: str,
                                 filename,
                                 old_public_id,
                                 image_bytes: UploadFile = File(), is_profile_picture=True):
          public_id = None

          try:
               # generate public id
               public_id = CloudinaryServices.generate_public_id(filename, current_user,is_profile_picture)

               # check if user have a profile picture
               if old_public_id is not None:
                    cloudinary.uploader.destroy(old_public_id)
               # upload in cloudinary and return the secure url
               image_url = await CloudinaryServices.upload_image(image_bytes, public_id, )
               # then update the profile picture
               new_profile_picture = UpdateProfileImage(public_key=public_id, img_url=image_url)
               # update picture
               await UserRepository.update_profile_image(current_user, new_profile_picture.model_dump())

          except Exception as e:
               # delete the image if error occurred
               if public_id is not None:
                    cloudinary.uploader.destroy(public_id)
               raise e

     @staticmethod
     def generate_public_id(filename, user_id):
          public_id = f"{user_id}-{os.path.splitext(filename)[0]}"
          return public_id
