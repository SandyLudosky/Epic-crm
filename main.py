from faker_sqlalchemy import SqlAlchemyProvider, Faker

from app.model import Contract, Event, Client, Collaborator
from crud import create_collaborators, create_clients, create_events, create_contracts
from app.config import session
import click


def main():
    create_collaborators()
    create_clients()
    create_events()
    create_contracts()


def _main():
    fake = Faker()
    fake.add_provider(SqlAlchemyProvider)
    for i in range(10):
        client = fake.sqlalchemy_model(Client)
        collaborator = fake.sqlalchemy_model(Collaborator)
        event = fake.sqlalchemy_model(Event)
        contract = fake.sqlalchemy_model(Contract)
        session.add(client)
        session.add(collaborator)
        session.add(event)
        session.add(contract)
        session.commit()


if __name__ == '__main__':
    main()
