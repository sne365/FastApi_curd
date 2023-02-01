from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost/Fastapi'
 
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, bind=engine,autocommit=False)

Base= declarative_base()

def get_db_connection():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()
        