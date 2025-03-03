from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Schémas pour l'utilisateur
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str  # en clair, qui sera haché

class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Schéma pour la mise à jour du mot de passe
class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str

# Schémas pour l'authentification (existant)
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Schémas pour les articles (existant)
class BlogPostBase(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None

class BlogPostCreate(BlogPostBase):
    user_id: int

class BlogPostUpdate(BlogPostBase):
    pass

class BlogPostRead(BlogPostBase):
    id: int
    created_at: datetime
    author: Optional[UserRead] = None

    class Config:
        orm_mode = True
