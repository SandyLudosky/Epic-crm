import click
import datetime
from sqlalchemy import literal_column
from app.model import Contract, Event, Client, Collaborator
from app.config import session
from utils import display_contract_status, display_role_status


def get_current_user():
    current_user = session.query(literal_column("current_user"))
    for usr in current_user:
        return usr[0]


def get_role(current_user):
    collaborators = session.query(Collaborator).all()
    for collaborator in collaborators:
        if collaborator.name == current_user:
            return collaborator.role


def get_permission(current_user):
    pass


def menu():
    print("======== MENU =========")
    print("[1] - create new event")
    print("[2] - edit event")
    print("[3] - display all events")
    print("=========================")
    print("[4] - create new contract")
    print("[5] - edit contract")
    print("[6] - display all contracts")
    print("=========================")
    print("[7] - create new collaborator")
    print("[8] - edit collaborator")
    print("[9] - display all collaborators")
    print("=========================")
    print("[10] - create new client")
    print("[11] - edit client")
    print("[12] - display all clients")

# CRUD


@click.command()
@click.option('--option', prompt='Your choice',
              help='Select option')
def selections(option):
    if int(option) == 1:
        create_event()
    elif int(option) == 2:
        get_all_events()
        edit_event()
    elif int(option) == 3:
        get_all_events()
    elif int(option) == 4:
        display_clients_events()
        create_contract()
    elif int(option) == 5:
        get_all_contracts()
        edit_contract()
    elif int(option) == 6:
        get_all_contracts()
    elif int(option) == 7:
        create_collaborator()
    elif int(option) == 8:
        edit_collaborator()
    elif int(option) == 9:
        get_all_collaborators
    elif int(option) == 10:
        create_client()
    elif int(option) == 11:
        edit_client()
    elif int(option) == 12:
        get_all_clients()
    else:
        print("Invalid option")


def sub_menu():
    print("======== MENU =========")
    print("[1] - make another query")
    print("[2] - quit")
    print("=========================")


@click.command()
@click.option('--option', prompt='Your choice',
              help='Select option')
def select(option):
    if int(option) == 1:
        menu()
        selections()
    elif int(option) == 2:
        exit()


def get_all_contracts():
    contracts = session.query(Contract).all()
    for contract in contracts:
        client = session.query(Client).filter(Client.id ==
                                              contract.client_id).first()
        event = session.query(Event).filter(Event.id ==
                                            contract.event_id).first()

        support = session.query(Collaborator).filter(Collaborator.id
                                                     == event.support_contact_id).first()

        print("id:", contract.id, "\n", "Created on:", contract.created_at,
              "\n", "client:", client.name, "\n",
              "support: ", support.name, "\n",
              "event:", event.name, "\n", "status:",
              display_contract_status(contract.status))
    sub_menu()
    select()
    return contracts


def get_all_events():
    events = session.query(Event).all()
    for event in events:
        print("id:", event.id, ",", "name:", event.name, "start:",
              event.start_date, "end:", event.end_date, "location:",
              event.location, "attendees:", event.attendees,
              "notes:", event.notes)
    sub_menu()
    select()
    return events


print("\n\n\n\n")


def get_all_collaborators():
    collaborators = session.query(Collaborator).all()
    for collaborator in collaborators:
        print("id:", collaborator.id, ",", "name:", collaborator.name, "email:",
              collaborator.email, "phone:", collaborator.phone, "role:",
              display_role_status(collaborator.role))
    sub_menu()
    select()
    return collaborators


def get_all_clients():
    clients = session.query(Client).all()
    for client in clients:
        support = session.query(Collaborator).filter(Collaborator.id
                                                     == client.support_id).first()
        print("id:", client.id, ",", "name:", client.name, "email:",
              client.email, "phone:", client.phone, "company name:",
              client.company_name, "support: ", support.name)

    sub_menu()
    select()
    return clients


def display_clients_events():
    events = session.query(Event).all()
    clients = session.query(Client).all()

    print("======Events: ======")
    for event in events:
        print("id:", event.id, ",", "name:", event.name, "start:",
              event.start_date, "end:", event.end_date, "location:",
              event.location, "attendees:", event.attendees,
              "notes:", event.notes)

    print("======Clients: ======")
    for client in clients:
        print("id:", client.id, ",", "name:", client.name, "email:",
              client.email, "phone:", client.phone, "company name:",
              client.company_name, "created at:", client.created_at)
    sub_menu()
    select()


@click.command()
@click.option('--name', prompt='name')
@click.option('--start', prompt='start date')
@click.option('--end', prompt='end date')
@click.option('--location', prompt='location')
@click.option('--attendees', prompt='number of attendees')
@click.option('--notes', prompt='notes or description')
def create_event(name, start, end, location, attendees, notes):

    start_date = datetime.datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end, '%Y-%m-%d')
    event = Event(name=name, start_date=start_date,
                  end_date=end_date,
                  location=location, attendees=int(attendees),
                  notes=notes)
    session.add(event)
    session.commit()
    sub_menu()
    select()


@click.command()
@click.option('--name', prompt='name')
@click.option('--email', prompt='email')
@click.option('--phone', prompt='phone')
def create_collaborator(name, email, phone, role):
    collaborator = Collaborator(name=name, email=email, phone=phone, role=role)
    session.add(collaborator)
    session.commit()
    sub_menu()
    select()


@click.command()
@click.option('--name', prompt='name')
@click.option('--email', prompt='email')
@click.option('--phone', prompt='phone')
def edit_collaborator(id, name, email, phone, role):
    collaborator = session.query(Collaborator).filter(
        Collaborator.id == int(id)).first()
    collaborator.name = name
    collaborator.email = email
    collaborator.phone = phone
    collaborator.role = role
    session.commit()
    sub_menu()
    select()


@click.command()
@click.option('--name', prompt='name')
@click.option('--email', prompt='email')
@click.option('--phone', prompt='phone')
def create_client(name, email, phone, company_name):

    client = Client(name=name, email=email, phone=phone,
                    company_name=company_name)
    session.add(client)
    session.commit()
    sub_menu()
    select()


@click.command()
@click.option('--name', prompt='name')
@click.option('--email', prompt='email')
@click.option('--phone', prompt='phone')
def edit_client(id, name, email, phone, role):
    client = session.query(Client).filter(
        Client.id == int(id)).first()
    client.name = name
    client.email = email
    client.phone = phone
    session.commit()
    sub_menu()
    select()


@click.command()
@click.option('--id', prompt='select event to edit')
@click.option('--name', prompt='name')
@click.option('--start', prompt='start date')
@click.option('--end', prompt='end date')
@click.option('--location', prompt='location')
@click.option('--attendees', prompt='number of attendees')
@click.option('--notes', prompt='notes or description')
@click.option('--status', prompt='notes or description')
def edit_event(id, name, start, end, location, attendees, notes, status):
    event = session.query(Event).filter(Event.id == int(id)).first()
    event.name = name
    event.start = datetime.datetime.strptime(start, '%Y-%m-%d')
    event.end = datetime.datetime.strptime(end, '%Y-%m-%d')
    event.location = location
    event.attendees = int(attendees)
    event.notes = notes
    event.status = status
    session.commit()
    sub_menu()
    select()


@click.command()
@click.option('--event_id', prompt='select event')
@click.option('--client_id', prompt='select client')
@click.option('--response', prompt='create contract ? [y/n]]')
def create_contract(client_id, event_id, response):
    contract = Contract(client_id=int(client_id), event_id=int(event_id),
                        created_at=datetime.datetime.now())
    if response == "y":
        session.add(contract)
        session.commit()
    sub_menu()
    select()


@click.command()
@click.option('--id', prompt='select contract to edit')
@click.option('--event_id', prompt='select event')
@click.option('--client_id', prompt='select client')
def edit_contract(id, client_id, event_id):
    contract = session.query(Contract).filter(Contract.id == int(id)).first()
    contract.client_id = int(client_id)
    contract.event_id = int(event_id)
    session.commit()
    sub_menu()
    select()


if __name__ == '__main__':
    menu()
    selections()
