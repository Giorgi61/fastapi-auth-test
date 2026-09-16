from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

import app.api as routes
import app.models  #noqa
from app.core.config import settings
from app.core.database import AsyncDB, db


class MainApp:
    def __init__(self, db: AsyncDB):
        self.db = db
        self.app = FastAPI(lifespan=self.db.create_database_lifespan)

app_fastapi = MainApp(db).app

app_fastapi.include_router(routes.routers)
app_fastapi.add_middleware(SessionMiddleware, secret_key=settings.OAUTH_SECRET_KEY.get_secret_value())



def main():
    import uvicorn


    uvicorn.run("app.main:app_fastapi", host="127.0.0.1", port=8000, reload=True)