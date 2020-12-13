from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

basedir = os.path.abspath(os.path.dirname(__file__))

# SQLALCHEMY_DATABASE_URL = 'sqlite:///' + os.path.join(basedir, 'sql_app.db')
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = "postgres://osgcfjjqxheapy:e74118db45e5c3a4098c9b761ed75e68187c7228907f9dd3fcf2b230a1bafd3d@ec2-50-17-218-108.compute-1.amazonaws.com:5432/d6o4j4vds51re5"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL#, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()