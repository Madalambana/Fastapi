from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from app import oauth2
from .. import models, schemas
from ..database import engine,get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

#we are retrieving all posts
@router.get("/", response_model=List[schemas.ResponseVote])
def root(db: Session = Depends(get_db), current_user: int = Depends(oauth2.current_user), limit: int = 10, skip: int = 0,
search:Optional[str] = ""): 
    #posts = db.query(models.Post).filter(models.Post.destination.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.destination.contains(search)).limit(limit).offset(skip).all()
    return results
    
#we are inserting new posts
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Response)
def post(postman: schemas.Create_post,db: Session = Depends(get_db), current_user: int = Depends(oauth2.current_user) ):
    created_post = models.Post(owner_id = current_user.id, **postman.dict())
    db.add(created_post)
    db.commit()
    db.refresh(created_post)
    return created_post

#getting an idividual post
@router.get("/{id}",response_model=schemas.ResponseVote)
def get_post(id: int,db: Session = Depends(get_db), current_user: int = Depends(oauth2.current_user)):
    test_post =  db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if test_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail= f"post is {id} not available")
    return test_post

#deleting posts
@router.delete("/{id}")
def delete(id: int,db: Session = Depends(get_db), current_user: int = Depends(oauth2.current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "post with id does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot perform action requested")
    post_query.delete(synchronize_session=False)
    db.commit() 
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#updating post
@router.put("/{id}", response_model=schemas.Response)
def update(id: int, postman: schemas.Create_post,db: Session = Depends(get_db), current_user: int = Depends(oauth2.current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot perform action requested")
    post_query.update(postman.dict(),synchronize_session=False)
    db.commit()
    return post
