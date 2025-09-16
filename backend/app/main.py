import uvicorn
from fastapi import FastAPI
import socket

from app.config.settings import Settings
from app.src.routes.auth_route import auth_router

settings = Settings()


app = FastAPI()


app.include_router(auth_router)


if __name__ == '__main__':
     import subprocess

     host = '0.0.0.0'
     # if settings.HOST =='local':
     #      #for localhost to access the api in mobile
     #      host = subprocess.check_output(["hostname", "-I"]).decode().strip().split()[0]
     uvicorn.run('app.main:app',reload=True,host=host,port=9090)