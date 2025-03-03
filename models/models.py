from typing import Optional, List
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str
    
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    posts: List["BlogPost"] = Relationship(back_populates="author")

class BlogPost(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    image_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

    author: Optional[User] = Relationship(back_populates="posts")
