from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:test1234@127.0.0.1:3306/todoapp"  #mysql
# SQLALCHEMY_DATABASE_URL = "sqlite:///.todos.db"  #sqlite
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:test1234@localhost/TodoApplicationDatabase"  #postgresql


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)  # creates db engine for other db's

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )  # creates db engine for sqlite

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # creates instance of db session
Base = declarative_base()  # creates db model
