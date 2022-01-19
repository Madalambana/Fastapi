from os import access
from jose import JWTError, jwt 
from datetime import datetime,timedelta
from . import schemas, models
from .config import settings
from .database import get_db
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#secret_key
#algorithm
#expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id = payload.get("id")

        if id == None:
            raise credentials_exception
        token_data = schemas.Token_data(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

def current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED ,detail= 
            "Cannot authenticate", headers={"WWW-Authenticate": "Bearer"})
    token = verify_token(token,credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
