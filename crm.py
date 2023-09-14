import click
import datetime

from app.model import Contract, Event, Client, Collaborator
from app.config import session
from utils import display_contract_status


def menu():
    print("======== MENU =========")
    print("[1] - create new event")
    print("[2] - edit event")
    print("[3] - display all events")
    print("=========================")
    print("[4] - create new contract")
    print("[5] - edit contract")
    print("[6] - display all contracts")
    print("[7] - display all clients")

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
        get_all_clients()
    else:
        print("Invalid option")


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
    return contracts


def get_all_events():
    events = session.query(Event).all()
    for event in events:
        print("id:", event.id, ",", "name:", event.name, "start:",
              event.start_date, "end:", event.end_date, "location:",
              event.location, "attendees:", event.attendees,
              "notes:", event.notes)
    return events


def get_all_clients():
    clients = session.query(Client).all()
    for client in clients:
        print("id:", client.id, ",", "name:", client.name, "email:",
              client.email, "phone:", client.phone, "company name:",
              client.company_name, "created at:", client.created_at)
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


@click.command()
@click.option('--id', prompt='select contract to edit')
@click.option('--event_id', prompt='select event')
@click.option('--client_id', prompt='select client')
def edit_contract(id, client_id, event_id):
    contract = session.query(Contract).filter(Contract.id == int(id)).first()
    contract.client_id = int(client_id)
    contract.event_id = int(event_id)
    session.commit()


if __name__ == '__main__':
    menu()
    selections()
