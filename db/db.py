from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
#SQLALCHEMY_DATABASE_URL = "sqlite:///./hngStage2.db"
#SQLALCHEMY_DATABASE_URL = "postgresql://default:HePa1sdgW7vM@ep-young-smoke-a4l644r7.us-east-1.aws.neon.tech:5432/hngstage2?sslmode=require"
print(SQLALCHEMY_DATABASE_URL)

engine = create_engine("postgresql://default:HePa1sdgW7vM@ep-young-smoke-a4l644r7.us-east-1.aws.neon.tech:5432/hngstage2?sslmode=require", pool_pre_ping=True)
 
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()
