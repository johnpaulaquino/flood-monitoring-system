from dotenv import load_dotenv
from pydantic import EmailStr, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
     #database URL
     DB_URL: str

     #email configurations
     MAIL_FROM: EmailStr
     MAIL_PASSWORD: SecretStr
     MAIL_PORT: int
     MAIL_STARTTLS: bool
     MAIL_USERNAME: str
     MAIL_SSL_TLS: bool
     MAIL_SERVER: str
     MAIL_USE_CREDENTIALS: bool
     MAIL_VALIDATE_CERTS: bool