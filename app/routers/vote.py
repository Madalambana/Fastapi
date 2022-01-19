from fastapi import FastAPI, status, HTTPException, Response, Depends,APIRouter
from .. import schemas, oauth2, models
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(postman: schemas.Vote,db: Session = Depends(get_db),current_user: int = Depends(oauth2.current_user)):
    query = db.query(models.Post).filter(models.Post.id == postman.post_id).first()
    if query == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    post_query = db.query(models.Vote).filter(models.Vote.post_id == postman.post_id, models.Vote.user_id == current_user.id)
    post = post_query.first()
    if (postman.dir == 1):
        if (post):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User has already voted")
        new_vote = models.Vote(post_id = postman.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully created vote"}
    else:
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
    post_query.delete(synchronize_session=False)
    db.commit
    return {"message": "successfully deleted vote"}