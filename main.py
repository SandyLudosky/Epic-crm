
from app.models import Contract, Event, Client, Collaborator
from crud import create_collaborators, create_clients, create_events, create_contracts
from app.config import session

import sentry_sdk


def main():
    create_collaborators()
    create_clients()
    create_events()
    create_contracts()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        # Alternatively the argument can be omitted
        sentry_sdk.capture_exception(e)
        sentry_sdk.capture_message('Something went wrong')
