from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from .database import engine
from .routers import routes
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)

for route in routes:
    app.include_router(route)

# Ajout du middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En développement, on peut autoriser toutes les origines. En prod, limitez aux domaines autorisés.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Blog API",
        version="1.0",
        description="API de blog avec authentification",
        routes=app.routes,
    )

    # Définition du schéma de sécurité pour JWT
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    # Appliquer la sécurité par défaut aux endpoints (sauf login et register)
    for path in openapi_schema["paths"]:
        if "api/auth/login" not in path and "api/auth/register" not in path:
            for method in openapi_schema["paths"][path]:
                openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi