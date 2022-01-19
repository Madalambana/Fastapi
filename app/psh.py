from fastapi import FastAPI
from sqlalchemy import engine
from . import models
from .database import engine
from .routers import post, user, auth, vote

try:
    models.Base.metadata.create_all(bind=engine)
    print("successfully connected")
except Exception as error:
    print('error', error)

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "less go jpxfrd"}
