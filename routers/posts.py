from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List
from ..models import BlogPost, User
from ..schemas import BlogPostCreate, BlogPostRead, BlogPostUpdate
from ..database import get_session
from ..routers.auth import get_current_user

router = APIRouter(
    prefix="/api/posts",
    tags=["posts"]
)

@router.get("/", response_model=List[BlogPostRead])
def read_posts(skip: int = 0, limit: int = 100, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Récupère tous les posts
    """
    posts = session.exec(select(BlogPost).offset(skip).limit(limit)).all()
    return posts

# Endpoint de recherche des posts par une requête (q)
@router.get("/search", response_model=List[BlogPostRead])
def search_posts(q: str, 
                 session: Session = Depends(get_session), 
                 current_user: User = Depends(get_current_user)):
    """
    Recherche des posts dont le titre ou le contenu contient la chaîne de caractères 'q'.
    La recherche est insensible à la casse (grâce à ilike).
    """
    # Utiliser ilike() pour une recherche insensible à la casse (PostgreSQL)
    query = select(BlogPost).where(
        (BlogPost.title.ilike(f"%{q}%")) | (BlogPost.content.ilike(f"%{q}%"))
    )
    posts = session.exec(query).all()
    if not posts:
        raise HTTPException(status_code=404, detail="Aucun post trouvé pour cette recherche")
    return posts

@router.get("/{post_id}", response_model=BlogPostRead)
def read_post(post_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Récupère un post par son id
    """
    post = session.get(BlogPost, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.get("/user/{user_id}", response_model=List[BlogPostRead])
def read_posts_by_user(user_id: int, session: Session = Depends(get_session)):
    """
    Récupère tout les postes d'un utilisateur spécifique
    """
    posts = session.exec(select(BlogPost).where(BlogPost.user_id == user_id)).all()
    if not posts:
        raise HTTPException(status_code=404, detail="No posts found for this user")
    return posts


@router.post("/", response_model=BlogPostRead)
def create_post(post: BlogPostCreate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Créer un nouveau post
    """
    db_post = BlogPost(**post.dict())
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post

@router.put("/{post_id}", response_model=BlogPostRead)
def update_post(post_id: int, post_update: BlogPostUpdate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Mettre à jour un post existant
    """
    post = session.get(BlogPost, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    update_data = post_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(post, key, value)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

@router.delete("/{post_id}")
def delete_post(post_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Supprimer un post
    """
    post = session.get(BlogPost, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    session.delete(post)
    session.commit()
    return {"detail": "Post deleted successfully"}