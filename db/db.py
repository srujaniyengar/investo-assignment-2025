from sqlmodel import create_engine, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:yourpassword@localhost:5432/investo_db")
engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session