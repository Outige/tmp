from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

basedir = os.path.abspath(os.path.dirname(__file__))

# SQLALCHEMY_DATABASE_URL = 'sqlite:///' + os.path.join(basedir, 'sql_app.db')
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = "postgres://ipehjzgtutjrdd:151db6d7c8c5ca0aeab88ec46166e159aef003ec004a4e6cf8e0075533bed1da@ec2-35-169-184-61.compute-1.amazonaws.com:5432/d1k2i8r28nki96"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL#, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()