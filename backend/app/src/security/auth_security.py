from datetime import datetime, timedelta, timezone
from typing import Any
from fastapi import status
import msgpack
from cryptography.fernet import Fernet
from jose import ExpiredSignatureError, jwt, JWTError
from msgpack import unpackb
from passlib.context import CryptContext
from starlette.responses import JSONResponse

from app.config.settings import Settings

settings = Settings()


class AuthSecurity:
     __cipher = Fernet(settings.FERNET_KEY)

     __context = CryptContext(schemes=['argon2'], deprecated='auto')

     @classmethod
     def hash_password(cls, plain_password: str):
          """
          To hash password using Argon2.
          :param plain_password: is provided by user.
          :return: hashed password.
          """
          return cls.__context.hash(plain_password)

     @classmethod
     def verify_hashed_password(cls, plain_password: str, hashed_password: str):
          """
          To verify if the inputted password is match to the hashed password.
          :param plain_password: is provided by user.
          :param hashed_password: is a hashed password that will retrieve to db.
          :return: True, if plain and hashed password is matched, otherwise False.
          """
          return cls.__context.verify(plain_password, hashed_password)

     @classmethod
     def generate_access_token(cls, data_: dict, expiration: int = 0):
          to_encode = data_.copy()
          expires = datetime.now(timezone.utc) + timedelta(minutes=5)
          if expiration > 0:
               expires = datetime.now(timezone.utc) + timedelta(days=expiration)

          # decrypt the data before it encode
          encrypted_data = {"data": cls.encrypt_data(to_encode), "exp":expires}

          encoded = jwt.encode(encrypted_data, key=settings.JWT_KEY, algorithm=settings.JWT_ALGORITHM)
          return encoded

     @staticmethod
     def decode_jwt_token(token : str):
          try:
               err_message = JSONResponse(
                       status_code=status.HTTP_401_UNAUTHORIZED,
                       content={'status':'failed', 'message':'Could not validate credentials'},
                       headers={"WWW-Authenticate":'Bearer'}
               )
               if not token:
                    return err_message

               payload= jwt.decode(token,key=settings.JWT_KEY,algorithms=[settings.JWT_ALGORITHM])
               if not payload.get('data'):
                    return err_message

               return payload.get('data')

          except ExpiredSignatureError as e:
               raise e

     @classmethod
     def generate_refresh_token(cls, to_encode):
          pass

     @classmethod
     def encrypt_data(cls, to_encode: Any):
          packed = msgpack.packb(to_encode)
          # encrypt the packed data before sending the data
          encrypted_data = cls.__cipher.encrypt(packed).decode()

          return encrypted_data

     @classmethod
     def decrypt_data(cls, encrypted_data: Any):
          decrypted_data = cls.__cipher.decrypt(encrypted_data)
          unpacked_data = unpackb(decrypted_data)

          return unpacked_data
