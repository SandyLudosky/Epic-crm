from app.model import Contract, Event, Client, Collaborator
from crud import create_collaborators, create_clients, create_events, create_contracts
from app.config import session
import click


def main():
    create_collaborators()
    create_clients()
    create_events()
    create_contracts()


if __name__ == '__main__':
    main()
