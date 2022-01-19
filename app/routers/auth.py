from fastapi import Response, HTTPException, Depends, status, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.utils import encrypt
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2

router = APIRouter(
    tags=['Authentication']
)

@router.post("/login")
def login(postman:OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.Email == postman.username).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Incorrect Email entry")
    if not utils.compare(postman.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=" Invalid password entry")
    access_token = oauth2.create_access_token(data={"id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}