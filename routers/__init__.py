from .auth import router as auth_router
from .posts import router as posts_router

routes = [
    auth_router,
    posts_router
]