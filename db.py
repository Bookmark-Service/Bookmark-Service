# # db.py

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# # 실제 데이터베이스 URL로 교체하세요.
# DATABASE_URL = "mysql+pymysql://user:password@localhost/mydatabase?charset=utf8mb4"

# engine = create_engine(DATABASE_URL, pool_pre_ping=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve database credentials from environment variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_CHARSET = os.getenv("DB_CHARSET", "utf8mb4")  # Default to utf8mb4 if not specified

# Construct the database URL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset={DB_CHARSET}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
