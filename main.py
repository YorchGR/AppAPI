from fastapi import FastAPI
from services import user_services

app = FastAPI()

app.include_router(user_services.router)