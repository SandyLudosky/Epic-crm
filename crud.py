from app.models import Contract, Event, Client, User, ROLE, STATUS
from sqlalchemy import ForeignKey
from app.config import session

import datetime

users = [
    {"name": 'sandra',
     "email": 'sandra@gmail.com',
     "phone": '444-340-211',
     "role": ROLE["SALES"]},
    {"name": 'mike',
     "email": 'mike@hotmal.com',
     "phone": '407-000-211',
     "role":  ROLE["SALES"]},
    {"name": 'Daisy X',
     "email": 'daisy@hotmal.com',
     "phone": '416-340-211',
     "role":  ROLE["SALES"]},
    {"name": 'claire',
     "email": 'claire@gmail.com',
     "phone": '416-222-333',
     "role":  ROLE["SUPPORT"]},
    {"name": 'Support Rep 2',
     "email": 'support2@gmail.com',
     "phone": '406-777-111',
     "role": ROLE["SUPPORT"]},
    {"name": 'adele',
     "email": 'adele@gmail.com',
     "phone": '234-456-123',
     "role": ROLE["MANAGER"]},
]

clients = [
    {"support": 3,
     "name": 'Melany B',
     "email": "melb@gmail.com",
     "phone": '444-340-211',
     'company_name': 'company ABC'
     },
    {"support": None,
     "name": 'Melany C',
     "email": 'melc@gmail.com',
     "phone": '416-706-2001',
     'company_name': 'company XYZ'
     },
    {
        "support": 1,
        "name": 'Stephany MacFarland',
        "email": 'sfarland@farland.com',
        "phone": '706-200-111',
        'company_name': 'Farland Inc'
    }
]

events = [
    {"client_id": 1,
     "support": 2,
     "name": 'Event 1',
     "start_date": datetime.datetime(2003, 11, 8),
     "end_date": datetime.datetime(2003, 10, 8),
     "location": 'Montreal',
     "attendees": 100,
     "notes": "This is a note"},
    {"client_id": 2,
     "support": None,
     "name": 'Event 2',
     "start_date": datetime.datetime(1995, 2, 3),
     "end_date": datetime.datetime(1995, 2, 10),
     "location": 'Toronto',
     "attendees": 200,
     "notes": "This is a note"},
    {"client_id": 3,
     "support": 3,
     "name": 'Event 3',
     "start_date": datetime.datetime(2015, 7, 1),
     "end_date": datetime.datetime(2015, 7, 3),
     "location": 'Vancouver',
     "attendees": 300,
     "notes": None},
]

contracts = [
    {"client": 1,
     "support": 2,
     "event": 1,
     "created_at": datetime.datetime(2003, 9, 8),
     "cost": 1000.20,
     "status": STATUS["CREATED"]},
    {"client": 2,
     "support": 2,
     "event": 2,
     "created_at": datetime.datetime(1995, 2, 3),
     "cost": 999.00,
     "status": STATUS["CREATED"]},
    {"client": 3,
     "support": 3,
     "event": 3,
     "created_at": datetime.datetime(2015, 7, 1),
     "cost": 199.00,
     "status": STATUS["CREATED"]}
]


def create_users():
    for user in users:
        user = User(name=user["name"],
                    email=user["email"],
                    phone=user["phone"],
                    role=user["role"])
        user.set_password("test123")
        session.add(user)
        session.commit()


def create_clients():
    for client in clients:
        client = Client(support_id=client["support"],
                        name=client["name"],
                        email=client["email"],
                        phone=client["phone"],
                        company_name=client["company_name"])

        session.add(client)
        session.commit()


def create_contracts():
    for contract in contracts:
        contract = Contract(client_id=contract["client"],
                            event_id=contract["event"],
                            created_at=contract["created_at"],
                            status=contract["status"])

        session.add(contract)
        session.commit()


def create_events():
    for event in events:
        event = Event(support_contact_id=event["support"],
                      client_id=event["client_id"],
                      name=event["name"],
                      start_date=event["start_date"],
                      end_date=event["end_date"],
                      location=event["location"],
                      attendees=event["attendees"],
                      notes=event["notes"])
        session.add(event)
        session.commit()
        print(event.name + "new record added")
