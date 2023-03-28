from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import cloudinary
import os

cloudinary.config(
    cloud_name = os.environ.get('cloudinary_cloud_name'),
    api_key = os.environ.get('cloudinary_api_key'),
    api_secret = os.environ.get('cloudinary_api_secret'),
    secure=True
)

SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URI')
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
