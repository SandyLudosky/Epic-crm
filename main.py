from app.model import Contract, Event, Client, Collaborator
from crud import create_collaborators, create_clients, create_events, create_contracts
from app.config import session
import click


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


def main():
    create_collaborators()
    create_clients()
    create_events()
    create_contracts()

if __name__ == '__main__':
    main()
