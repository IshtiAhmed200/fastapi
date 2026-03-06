
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

DATABASE_URL= "sqlite:///./app.db"
Base = declarative_base()

def get_engine():
    return create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
    )

SessionLocal = sessionmaker(bind=get_engine(),autoflush=False,autocommit=False)

def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()

def init_db():
    Base.metadata.create_all(bind=get_engine())