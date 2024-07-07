from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import models, db

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins = ["*"],
  allow_credentials = True,
  allow_methods = ["*"],
  allow_headers = ['*']
)

from routes import auth, user

app.include_router(auth.router)
app.include_router(user.router)

models.Base.metadata.create_all(db.engine)
print("db created")
