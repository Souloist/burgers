import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqlalchemy_url = os.environ.get("SQLALCHEMY_DATABASE_URI")
engine = create_engine(sqlalchemy_url, convert_unicode=True)

Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
session = scoped_session(Session)

Base = declarative_base()
Base.query = session.query_property()
