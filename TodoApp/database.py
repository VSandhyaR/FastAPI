from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:test1234@localhost/TodoApplicationDatabase"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)  # creates db engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # creates instance of db session
Base = declarative_base()  # creates db model
