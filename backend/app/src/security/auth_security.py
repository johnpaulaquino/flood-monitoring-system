from datetime import datetime, timedelta, timezone
from typing import Any

import msgpack
from cryptography.fernet import Fernet
from jose import jwt
from msgpack import unpackb
from passlib.context import CryptContext

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
     def generate_access_token(cls, data: dict):
          to_encode = data.copy()
          expires = datetime.now(timezone.utc) + timedelta(days=3)
          to_encode.update({'exp': expires})
          encoded = jwt.encode(to_encode, key=settings.JWT_KEY, algorithm=settings.JWT_ALGORITHM)
          return encoded

     @classmethod
     def generate_refresh_token(cls):
          pass

     @classmethod
     def encrypt_data(cls, data : Any):
          packed = msgpack.packb(data)
          # encrypt the packed data before sending the data
          encrypted_data = cls.__cipher.encrypt(packed)

          return encrypted_data

     @classmethod
     def decrypt_data(cls,encrypted_data : Any):
          decrypted_data = cls.__cipher.decrypt(encrypted_data)
          unpacked_data = unpackb(decrypted_data)

          return unpacked_data
