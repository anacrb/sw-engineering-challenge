import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# In production, use environment variables or a config file for the DB URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://bloqit:bloqit@localhost:5432/bloqitdb")

engine = create_engine(DATABASE_URL, echo=False)  # echo=True for SQL debug logs
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()