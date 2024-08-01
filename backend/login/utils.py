from passlib.context import CryptContext
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
