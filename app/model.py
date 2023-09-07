from sqlalchemy import create_engine, Column, Integer, String, Date, Enum, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from .config import engine


Base = declarative_base()


class Client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True)
    support_id = Column(Integer)
    name = Column(String(50))
    email = Column(String(50))
    phone = Column(String(10))
    company_name = Column(String(50))
    created_at = Column(Date)


class Collaborator(Base):
    __tablename__ = 'collaborator'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50))
    phone = Column(String(10))
    role = Column(Enum("sales representative", "client support",
                       "account manager"))

# Roles:
# sales representative = peut créer des events, changer les contrats de leurs clients
# account manager = peut changer les client support et les events
# client support = peut changer les events de leur clients


class Contract(Base):
    __tablename__ = 'contract'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    client_id = ForeignKey('client.id', onupdate="CASCADE", ondelete="CASCADE")
    event_id = ForeignKey('event.id', onupdate="CASCADE", ondelete="CASCADE")
    created_at = Column(Date)

    role = Column(Enum("created", "signed", "paid"))


class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    sales_contact_id = ForeignKey('collaborator.id', onupdate="CASCADE",
                                  ondelete="CASCADE")
    support_contact_id = ForeignKey('collaborator.id', onupdate="CASCADE",
                                    ondelete="CASCADE")
    name = Column(String(50))
    start_date = Column(Date)
    end_date = Column(Date)
    location = Column(String(50))
    attendees = Column(Integer)
    notes = Column(String(50), nullable=True)


# 4- migrate
Base.metadata.create_all(engine)
