import uvicorn
from fastapi import FastAPI
import socket

from app.config.settings import Settings
from app.src.routes.auth_route import auth_router
from app.src.routes.user_route import user_router

settings = Settings()


app = FastAPI()


app.include_router(auth_router)
app.include_router(user_router)


if __name__ == '__main__':
     import subprocess

     host = '0.0.0.0'
     # if settings.HOST =='local':
     #      #for localhost to access the api in mobile
     #      host = subprocess.check_output(["hostname", "-I"]).decode().strip().split()[0]
     uvicorn.run('app.main:app',reload=True,host=host,port=settings.SERVER_PORT)
