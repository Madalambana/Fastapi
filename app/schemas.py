from typing import Optional
from pydantic  import BaseModel, EmailStr, conint

#Validation from front end
class Verification(BaseModel):
    destination: str
    heading: str

class Create_post(Verification):
    pass

class Create_user(BaseModel):
        Email: EmailStr
        password: str

class Login(Create_user):
    pass

class Token_data(BaseModel):
    id : Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
#Response structure

class Users(BaseModel):
    id : int
    Email: EmailStr
    class Config:
        orm_mode = True

class Response(Verification):
    id: int
    published: bool
    owner_id : int
    pass
    owner: Users
    class Config:
        orm_mode = True

class ResponseVote(BaseModel): 
    Post : Response
    Votes: int
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token = str
    token_type = str
    