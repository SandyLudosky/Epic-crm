from app.model import Contract, Event, Client, Collaborator
from app.config import session

import datetime

collaborators = [
    {"name": 'Sandra Queen',
     "email": 'sandra@gmail.com',
     "phone": '444-340-211',
     "role": "sales representative"},
    {"name": 'Dalton T',
     "email": 'dalton@hotmal.com',
     "phone": '407-000-211',
     "role": "sales representative"},
    {"name": 'Daisy X',
     "email": 'daisy@hotmal.com',
     "phone": '416-340-211',
     "role": "sales representative"},
    {"name": 'Support Rep 1',
     "email": 'support1@gmail.com',
     "phone": '416-222-333',
     "role": "client support"},
    {"name": 'Support Rep 2',
     "email": 'support2@gmail.com',
     "phone": '406-777-111',
     "role": "client support"},
    {"name": 'Manager 1',
     "email": 'support2@gmail.com',
     "phone": '234-456-123',
     "role": "account manager"},
]

clients = [
    {"support": 1,
     "name": 'Melany B',
     "email": "melb@gmail.com",
     "phone": '444-340-211',
     'company_name': 'company ABC',
     "created_at": datetime.datetime(2003, 11, 8)
     },
    {"support": 2,
     "name": 'Melany C',
     "email": 'melc@gmail.com',
     "phone": '416-706-2001',
     'company_name': 'company XYZ',
     "created_at": datetime.datetime(1995, 2, 3)
    },
    {
     "support": 1,
     "name": 'Stephany MacFarland',
     "email": 'sfarland@farland.com',
     "phone": '706-200-111',
     'company_name': 'Farland Inc',
     "created_at": datetime.datetime(2015, 7, 1)}
]

events = [
    {"contact_id": 1,
     "support_id": 2,
     "name": 'Event 1',
     "start_date": datetime.datetime(2003, 11, 8),
     "end_date": datetime.datetime(2003, 10, 8),
     "location": 'Montreal',
     "attendees": 100,
     "notes": "This is a note"},
    {"contact_id": 2,
     "support_id": 3,
     "name": 'Event 2',
     "start_date": datetime.datetime(1995, 2, 3),
     "end_date": datetime.datetime(1995, 2, 10),
     "location": 'Toronto',
     "attendees": 200,
     "notes": "This is a note"},
    {"contact_id": 3,
     "support_id": 3,
     "name": 'Event 3',
     "start_date": datetime.datetime(2015, 7, 1),
     "end_date": datetime.datetime(2015, 7, 3),
     "location": 'Vancouver',
     "attendees": 300,
     "notes": "This is a note"},
]

contracts = [
    {"client_id": 1,
     "support_id": 2,
     "event_id": 1,
     "created_at": datetime.datetime(2003, 9, 8),
     "role": "created"},
    {"client_id": 2,
     "support_id": 2,
     "event_id": 2,
     "created_at": datetime.datetime(1995, 2, 3),
     "role": "created"},
    {"client_id": 3,
     "support_id": 3,
     "event_id": 3,
     "created_at": datetime.datetime(2015, 7, 1),
     "role": "created"},
]


def create_collaborators():
    for collaborator in collaborators:
        collaborator = Collaborator(name=collaborator["name"],
                                    email=collaborator["email"],
                                    phone=collaborator["phone"],
                                    role=collaborator["role"])
        session.add(collaborator)
        session.commit()


def create_clients():
    for client in clients:
        client = Client(support_id=client["support"],
                        name=client["name"],
                        email=client["email"],
                        phone=client["phone"],
                        company_name=client["company_name"],
                        created_at=client["created_at"])

        session.add(client)
        session.commit()


def create_contracts():
    for contract in contracts:
        contract = Contract(
                              client_id=contract["client_id"],
                              event_id=contract["event_id"],
                              created_at=contract["created_at"],
                              role=contract["role"]
                                )

        session.add(contract)
        session.commit()


def create_events():
    for event in events:
        event = Event(sales_contact_id=event["contact_id"],
                      support_contact_id=event["support_id"],
                      start_date=event["start_date"],
                      end_date=event["end_date"],
                      location=event["location"],
                      attendees=event["attendees"],
                      notes=event["notes"])
        session.add(event)
        session.commit()