# db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 실제 데이터베이스 URL로 교체하세요.
DATABASE_URL = "mysql+pymysql://user:password@localhost/mydatabase?charset=utf8mb4"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
