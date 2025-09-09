import asyncio
import time
from pathlib import Path
from threading import Lock

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr

from app.config.settings import Settings

settings = Settings()


class EmailServices:
     __instance = {}
     __lock = Lock()
     __template_path = Path(__file__).parent.parent.parent / 'templates' / 'email'

     def __new__(cls, *args, **kwargs):
          # we lock the thread and check if there is an instance of object
          with cls.__lock:
               if cls not in cls.__instance:
                    instance = super().__new__(*args, **kwargs)
                    time.sleep(1)
                    cls.__instance[cls] = instance
          return cls.__instance[cls]

     @classmethod
     def get_fastapi_mail(cls):
          configuration = ConnectionConfig(
                  MAIL_USERNAME=settings.MAIL_USERNAME,
                  MAIL_PASSWORD=settings.MAIL_PASSWORD,
                  MAIL_FROM=settings.MAIL_FROM,
                  MAIL_PORT=settings.MAIL_PORT,
                  MAIL_SERVER=settings.MAIL_SERVER,
                  MAIL_STARTTLS=settings.MAIL_STARTTLS,
                  MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
                  USE_CREDENTIALS=settings.MAIL_USE_CREDENTIALS,
                  VALIDATE_CERTS=settings.MAIL_VALIDATE_CERTS,
                  TEMPLATE_FOLDER=cls.__template_path,
          )
          fm = FastMail(configuration)
          return fm

     @classmethod
     async def send_message(cls, recipient: str):
          fm = cls.get_fastapi_mail()
          message = MessageSchema(
                  subject="Account Verification",
                  recipients=[recipient],
                  template_body={},
                  subtype=MessageType.html,
          )
          await fm.send_message(message, template_name="email-verification.html")


