from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Standard template generally used for defining database URL for MySQL, PostGreSQL, Orcale DB
"<dialect>+<driver>://<username>:<password>@<host>:<port>/<database>"

# For SQL Lite
"sqlite://:memory:" # Add to system memory and will be lost when the application is closed/reloaded.
"sqlite://<path>" # start with '///' for relative path or '////' for absolute path

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'

engine = create_engine(url=SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

