import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config.settings import Settings
from app.src.exceptions.app_exception import BaseAppException
from app.src.exceptions.app_handle_exception import app_exception_handler
from app.src.routes.announcements_route import announcements_router
from app.src.routes.auth_route import auth_router
from app.src.routes.user_route import user_router
from app.src.utils.app_utils import AppUtils

settings = Settings()

lifespan = AppUtils()

app = FastAPI(
        lifespan=lifespan.life_span,
)
# set CORS
app.add_middleware(CORSMiddleware,
              allow_origins=['*'],
              allow_methods=['*'],
              allow_headers=['*'],
              allow_credentials=True)
# add exception middleware to handle custom exception
app.add_exception_handler(exc_class_or_status_code=BaseAppException, handler=app_exception_handler())
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(announcements_router)

if __name__ == '__main__':

     host = '0.0.0.0'
     # if settings.HOST =='local':
     #      #for localhost to access the api in mobile
     #      host = subprocess.check_output(["hostname", "-I"]).decode().strip().split()[0]
     uvicorn.run('app.main:app', reload=True, host=host, port=settings.SERVER_PORT)
