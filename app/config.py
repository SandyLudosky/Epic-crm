from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# 1- engine
engine = create_engine("sqlite:///database.db", echo=True)

# 2- session
Session = sessionmaker(bind=engine)
session = Session()
