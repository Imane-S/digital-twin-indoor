import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import redis

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/digitaltwin")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)