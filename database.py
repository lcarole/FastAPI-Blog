import os
from sqlmodel import create_engine, Session


DATABASE_URL = os.getenv("DATABASE_URL","postgresql://postgres:postgres@localhost/blog_db")
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
