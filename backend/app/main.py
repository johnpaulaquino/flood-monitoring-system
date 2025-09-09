import uvicorn
from fastapi import FastAPI

from app.src.routes.auth_route import auth_router

app = FastAPI()


app.include_router(auth_router)





if __name__ == '__main__':
    uvicorn.run('app.main:app',reload=True,host='0.0.0.0',port=9090)