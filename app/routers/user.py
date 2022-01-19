from fastapi import FastAPI, status, HTTPException, Response, Depends,APIRouter
from .. import models, schemas, utils
from ..database import engine,get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users"
)

@router.post("/", response_model=schemas.Users, status_code=status.HTTP_201_CREATED)
def users( postman: schemas.Create_user,db: Session = Depends(get_db)):
    encrypt = utils.encrypt(postman.password)
    postman.password = encrypt
    users = models.User(**postman.dict())
    db.add(users)
    db.commit()
    db.refresh(users) 
    return users

@router.get("/{id}", response_model=schemas.Users)
def get_user(id: int, db: Session = Depends(get_db)):
    get_user = db.query(models.User).filter(models.User.id == id)
    if get_user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} does not exist")
    return get_user.first()