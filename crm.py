from sqlalchemy import ForeignKey
from app.model import Contract, Event, Client, Collaborator
from app.config import session
import click

import datetime


def menu():
    print("======== MENU =========")
    print("[1] - create new event")
    print("[2] - edit event")
    print("[3] - display all events")
    print("=========================")
    print("[4] - create new contract")
    print("[5] - edit contract")
    print("[6] - display all contracts")

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
        create_contract()
    elif int(option) == 5:
        get_all_contracts()
        edit_contract()
    elif int(option) == 6:
        get_all_contracts()
    else:
        print("Invalid option")


def get_all_contracts():
    contracts = session.query(Contract).all()
    for contract in contracts:
        client = session.query(Client).filter(Client.id ==
                                              int('contract.client_id')).first()
        event = session.query(Event).filter(Event.id ==
                                            int('contract.event_id')).first()
        print("id:", contract.id, ",", contract.created_at,
              "client:", client.name, "event:",
              event.name, "role:", contract.role)
    return contracts


def get_all_events():
    events = session.query(Event).all()
    for event in events:
        print("id:", event.id, ",", "name:", event.name, "start:",
              event.start_date, "end:", event.end_date, "location:",
              event.location, "attendees:", event.attendees,
              "notes:", event.notes)
    return events


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
@click.option('--name', prompt='name')
@click.option('--start', prompt='start date')
@click.option('--end', prompt='end date')
@click.option('--location', prompt='location')
@click.option('--attendees', prompt='number of attendees')
@click.option('--notes', prompt='notes or description')
@click.option('--status', prompt='notes or description')
def edit_event(name, start, end, location, attendees, notes, status):
    pass

@click.command()
@click.option('--id', prompt='select student to delete')
def create_contract(id):
    pass

@click.command()
@click.option('--id', prompt='select student to delete')
def edit_contract(id):
    pass


if __name__ == '__main__':
    menu()
    selections()