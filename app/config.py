from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import URL

import sentry_sdk


sentry_sdk.init(
    dsn="https://examplePublicKey@o0.ingest.sentry.io/0",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)


# engine SQLITE
# engine = create_engine("sqlite:///database.db", echo=True)


# engine POSTGRESQL
# engine = create_engine(
#     "postgresql+psycopg2://postgres:test123@localhost:5432/sandyludosky", echo=True)

engine = create_engine(
    "postgresql+psycopg2://mike:test123@localhost:5432/sandyludosky", echo=True)

# 2- session
Session = sessionmaker(bind=engine)
session = Session()
