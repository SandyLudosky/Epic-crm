import os
import click
import datetime
from app.config import session


from app.models import Contract, Event, Client, User, ROLE
from app.menu import menu, roles_options, restart, contract_filters
from app.permissions import UserPermissions

from utils import display_contract_status, display_role
import sentry_sdk

# MENU
USER = os.getenv('USER')

def get_current_user():
    return session.query(User).filter(User.name == USER).first()

@click.command()
@click.option('--option', prompt='Your choice',
              help='Select option')
def restart_selections(option):
    if int(option) == 1:
        menu()
        selections()
    elif int(option) == 2:
        exit()


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
        roles_options()
        create_user()
    elif int(option) == 8:
        edit_user()
    elif int(option) == 9:
        get_all_users()
    elif int(option) == 10:
        delete_user()
    elif int(option) == 11:
        create_client()
    elif int(option) == 12:
        edit_client()
    elif int(option) == 13:
        get_all_clients()
    else:
        print("Invalid option")
    restart()
    restart_selections()


@click.command()
@click.option('--option', prompt='Your choice',
              help='Select option')
def restart_selections(option):
    if int(option) == 1:
        menu()
        selections()
    elif int(option) == 2:
        exit()


def get_current_user():
    return session.query(User).filter(User.name == USER).first()

# READ


def get_all_contracts():
    if UserPermissions.can_read_contract():
        contracts = session.query(Contract).all()
        for contract in contracts:
            client = session.query(Client).filter(Client.id ==
                                                  contract.client_id).first()
            event = session.query(Event).filter(Event.id ==
                                                contract.event_id).first()

            support = session.query(User).filter(User.id
                                                         == event.support_contact_id).first()

            print("id:", contract.id, "\n",
                  "\n", "client:", client.name, "\n",
                  "support: ", support.name, "\n",
                  "event:", event.name, "\n", "status:",
                  display_contract_status(contract.status))
        contract_filters()
        filter_display_contracts()
        return contracts
    else:
        print("🛑 You don't have the permission to create a contract")


def get_all_events():
    current_user = get_current_user()
    events = session.query(Event).all()
    events_no_support = session.query(Event).filter(
        Event.support_contact_id is None).all()

    if UserPermissions.can_display_events_without_support(current_user):
        for event in events_no_support:
            print("id:", event.id, ",", "name:", event.name, "start:",
                  event.start_date, "end:", event.end_date, "location:",
                  event.location, "attendees:", event.attendees,
                  "notes:", event.notes)
    else:
        for event in events:
            print("id:", event.id, ",", "name:", event.name, "start:",
                  event.start_date, "end:", event.end_date, "location:",
                  event.location, "attendees:", event.attendees,
                  "notes:", event.notes)
    return events


def get_all_users():
    users = session.query(User).all()
    for user in users:
        print("id:", user.id, ",", "name:", user.name, "email:",
              user.email, "phone:", user.phone, "role:",
              display_role_status(user.role))
    return users


def get_all_clients():
    clients = session.query(Client).all()
    for client in clients:
        support = session.query(User).filter(User.id
                                                     == client.support_id).first()
        print("id:", client.id, ",", "name:", client.name, "email:",
              client.email, "phone:", client.phone, "company name:",
              client.company_name, "support: ", support.name)

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
              client.company_name)


@click.command()
@click.option('--filter', prompt='filter')
def filter_display_contracts(filter):
    contracts = []
    if filter == int(1):
        contracts = session.query(Contract).filter(
            Contract.status == "created").all()
    elif filter == int(2):
        contracts = session.query(Contract).filter(
            Contract.status == "signed").all()
    elif filter == int(3):
        contracts = session.query(Contract).filter(
            Contract.status == "paid").all()
    else:
        print("Invalid option")
    display(contracts)
    restart()
    restart_selections()


def display(contracts):
    if len(contracts) == 0:
        return print("No contracts to display")
    else:
        for contract in contracts:
            client = session.query(Client).filter(Client.id ==
                                                  contract.client_id).first()
            event = session.query(Event).filter(Event.id ==
                                                contract.event_id).first()

            support = session.query(User).filter(User.id
                                                         == event.support_contact_id).first()

            print("id:", contract.id, "\n",
                  "\n", "client:", client.name, "\n",
                  "support: ", support.name, "\n",
                  "event:", event.name, "\n", "status:",
                  display_contract_status(contract.status))


# CREATE


@click.command()
@click.option('--name', prompt='name')
@click.option('--email', prompt='email')
@click.option('--phone', prompt='phone')
@click.option('--role', prompt='role')
def create_user(name, email, phone, role):
    try:
        if UserPermissions.can_create_user():

            user = User(
                name=name, email=email, phone=phone,
                role=display_role(int(role)))
            session.add(user)
            session.commit()
            print("✅ user successfully created")
        else:
            print("🛑 You don't have the permission to create a user")
    except Exception as e:
        # Alternatively the argument can be omitted
        print("ERROR")
        print(str(e))
        sentry_sdk.capture_exception(e)
        sentry_sdk.capture_message('Something went wrong')


@click.command()
@click.option('--event_id', prompt='select event')
@click.option('--client_id', prompt='select client')
@click.option('--response', prompt='create contract ? [y/n]]')
def create_contract(client_id, event_id, response):
    if UserPermissions.can_create_contract():
        contract = Contract(client_id=int(client_id), event_id=int(event_id),
                            created_at=datetime.datetime.now())
        if response == "y":
            session.add(contract)
            session.commit()
            print("✅ user successfully created")
    else:
        print("🛑 You don't have the permission to create a user")


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
@click.option('--email', prompt='email')
@click.option('--phone', prompt='phone')
@click.option('--company_name', prompt='company')
def create_client(name, email, phone, company_name):
    current_user = get_current_user()
    if UserPermissions.can_create_client():
        client = Client(name=name, email=email, phone=phone,
                        company_name=company_name, support_id=current_user.id)
        session.add(client)
        session.commit()
        print("✅ client successfully created")
    else:
        print("🛑 You don't have the permission to create a client")


# UPDATE


@click.command()
@click.option('--name', prompt='name')
@click.option('--email', prompt='email')
@click.option('--phone', prompt='phone')
def edit_user(id, name, email, phone, role):
    if UserPermissions.can_update_user():
        user = session.query(User).filter(
            User.id == int(id)).first()
        user.name = name
        user.email = email
        user.phone = phone
        user.role = role
        session.commit()
        print("✅ user successfully edited")
    else:
        print("🛑 You don't have the permission to edit a user")


def edit_client():
    current_user = get_current_user()
    if UserPermissions.can_update_client():

        clients = session.query(Client).filter(
            Client.support_id == current_user.id).first()
        edit_one_client()
        for client in clients:
            print("id:", client.id, ",", "name:", client.name, "email:",
                  client.email, "phone:", client.phone, "company name:",
                  client.company_name)
        print("✅ client successfully edited")
    else:
        print("🛑 You don't have the permission to create a client")


@click.command()
@click.option('--name', prompt='name')
@click.option('--email', prompt='email')
@click.option('--phone', prompt='phone')
@click.option('--id', prompt='phone')
def edit_one_client(id, name, email, phone):
    if UserPermissions.can_update_user():
        client = session.query(Client).filter(
            Client.id == int(id)).first()

        client.name = name
        client.email = email
        client.phone = phone
        session.commit()
        print("✅ user successfully edited")
    else:
        print("🛑 You don't have the permission to create a client")


def edit_event():
    current_user = get_current_user
    if UserPermissions.can_display_events_without_support(current_user):
        edit_event_with_no_support()
    else:
        edit_any_event()


@click.command()
@click.option('--id', prompt='select event to edit')
@click.option('--name', prompt='name')
@click.option('--start', prompt='start date')
@click.option('--end', prompt='end date')
@click.option('--location', prompt='location')
@click.option('--attendees', prompt='number of attendees')
@click.option('--notes', prompt='notes or description')
@click.option('--status', prompt='notes or descript1ion')
def edit_any_event(id, name, start, end, location, attendees, notes, status):
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
@click.option('--id', prompt='select event to edit')
@click.option('--support', prompt='support')
def edit_event_with_no_support():
    event = session.query(Event).filter(Event.id == int(id)).first()
    support_contact_id = session.query(
        User).filter(User.id == int(id)).first()
    event.support_contact_id = support_contact_id
    session.commit()


@click.command()
@click.option('--id', prompt='select event to edit')
@click.option('--support', prompt='support contact')
def edit_event_support(id, support_contact_id):
    event = session.query(Event).filter(Event.id == int(id)).first()
    event.support_contact_id = support_contact_id
    session.commit()


def edit_contract():
    current_user = get_current_user()
    client = session.query(Client).filter(
        Client.support_id == current_user.id).first()
    contracts = session.query(Contract).filter(
        Contract.client_id == client.id).all()
    if UserPermissions.can_update_contract():
        for contract in contracts:

            event = session.query(Event).filter(Event.id ==
                                                contract.event_id).first()

            support = session.query(user).filter(user.id
                                                         == event.support_contact_id).first()

            print("id:", contract.id, "\n",
                  "\n", "client:", client.name, "\n",
                  "support: ", support.name, "\n",
                  "event:", event.name, "\n", "status:",
                  display_contract_status(contract.status))
        edit_contract_my_clients()
        print("✅ user successfully edited")
    else:
        print("🛑 You don't have the permission to create a client")


@click.command()
@click.option('--id', prompt='select contract to edit')
@click.option('--status', prompt='select status')
def edit_contract_my_clients(id, status):
    contract = session.query(Contract).filter(
        Contract.id == int(id)).first()
    contract.status = status
    session.commit()

# DELETE


@click.command()
@click.option('--name', prompt='name')
@click.option('--email', prompt='email')
@click.option('--phone', prompt='phone')
def delete_user(id):
    session.query(User).delete(
        User.id == int(id)).first()
    print("user successfully deleted")
    session.commit()


if __name__ == '__main__':
    menu()
    selections()
