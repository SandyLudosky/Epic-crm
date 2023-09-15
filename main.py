
import click
import os
import bcrypt
import hashlib
import base64


from app.models import Contract, Event, Client, Collaborator
from crud import create_collaborators, create_clients, create_events, create_contracts
from app.config import session

import sentry_sdk


def hash_password():
    psw = os.environ['PSW']

    try:
        encode = psw.encode("utf-8")
        hashed = bcrypt.hashpw(encode, bcrypt.gensalt())
        return [encode, hashed]

    except Exception as e:
        print(e)


@click.command()
@click.option('--user', prompt='username', help='Type your username')
@click.option('--password', prompt='password', help='Type a strong password')
def login(user, password):
    os.environ["USER"] = user
    os.environ["PSW"] = password
    main()


def main():
    try:
        [encode, hashed] = hash_password()
        user_connected = bcrypt.checkpw(encode, hashed)
        if user_connected:
            print("connected")
            app()
        else:
            print("not connected")
            login()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print("\n======= LOGIN =======\n")
        login()


def app():
    create_collaborators()
    create_clients()
    create_events()
    create_contracts()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        # Alternatively the argument can be omitted
        print(e)
        sentry_sdk.capture_exception(e)
        sentry_sdk.capture_message('Something went wrong')
