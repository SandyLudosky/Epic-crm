import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sentry_sdk


SENTRY = os.environ.get("SENTRY")
sentry_sdk.init(
    dsn=SENTRY,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

# engine SQLITE
# engine = create_engine("sqlite:///database.db", echo=True)


# engine POSTGRESQL
engine = create_engine(
    "postgresql+psycopg2://postgres:test123@localhost:5432/sandyludosky", echo=False)


# 2- session
Session = sessionmaker(bind=engine)
session = Session()
