from sqlalchemy.sql.sqltypes import TIMESTAMP, Boolean
from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, column
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, nullable=False)
    destination = Column(String,nullable=False)
    heading = Column(String,nullable=False)
    published = Column(Boolean,server_default='True')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('Now()'))
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False )
    owner = relationship("User")
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, nullable=False,primary_key=True)
    Email = Column(String,nullable=False, unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('Now()'))
    phone = Column(String, nullable= True)
    
class Vote(Base):
    __tablename__ = "votes"
    post_id = Column(Integer,ForeignKey("post.id",ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), primary_key=True)