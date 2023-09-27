import enum
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from .config import engine

from sqlalchemy.dialects.postgresql import ENUM as PythonEnum

import datetime

Base = declarative_base()

ROLE = {
    "SALES": 'sales',
    "SUPPORT": 'support',
    "MANAGER": 'manager'
}

STATUS = {
    "CREATED": "created",
    "SIGNED": "signed",
    "PAID ": "paid",
}

class Client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True)
    support_id = Column(Integer)
    name = Column(String(50))
    email = Column(String(50))
    phone = Column(String(20))
    company_name = Column(String(50))


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50))
    phone = Column(String(20))
    role = Column(String(20))
    # role = Column(Enum(RoleEnum, name="role"), default="sales")

# Roles:
# sales representative = peut créer des events, changer les contrats de leurs clients
# account manager = peut changer les client support et les events
# client support = peut changer les events de leur clients


class Contract(Base):
    __tablename__ = 'contract'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    # client_id = ForeignKey('client.id', onupdate="CASCADE", ondelete="CASCADE")
    # event_id = ForeignKey('event.id', onupdate="CASCADE", ondelete="CASCADE")
    client_id = Column(Integer)
    event_id = Column(Integer)
    created_at = Column(Date, default=datetime.datetime.now)
    status = Column(String(20))
    # status = Column(Enum(StatusEnum, name="status"),
    #                 default="created")


class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # support_contact_id = ForeignKey('User.id', onupdate="CASCADE",
    #                                 ondelete="CASCADE")
    client_id = Column(Integer)
    support_contact_id = Column(Integer, nullable=True)
    name = Column(String(50))
    start_date = Column(Date)
    end_date = Column(Date)
    location = Column(String(50))
    attendees = Column(Integer)
    notes = Column(String(50), nullable=True, default="")


# 4- migrate
Base.metadata.create_all(engine)
