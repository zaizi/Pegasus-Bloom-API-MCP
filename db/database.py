from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()

db_username = os.getenv("POSTGRES_USER")
db_password = os.getenv("DB_PASSWORD")
database_name= os.getenv("POSTGRES_DB")
db_host = os.getenv("DB_HOST", "db")
DBPASS = os.getenv("DBPASS", None)

if DBPASS is None:
    DATABASE_URL = os.getenv("DATABASE_URL")
    if DATABASE_URL is None:
        raise ValueError("DATABASE_URL environment variable is not set")
else:
    DATABASE_URL = f"postgresql+psycopg2://{db_username}:{DBPASS}@{db_host}:5432/{database_name}"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a SessionLocal class to generate new Session objects
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for database models
Base = declarative_base()