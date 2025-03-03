import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL","postgresql://postgres:postgres@localhost/blo")
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
