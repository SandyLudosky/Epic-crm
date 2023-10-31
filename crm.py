import sentry_sdk
import click
import datetime
from app.config import session
from app.auth import (
    authentification_initiale,
    get_current_user,
    logout_user
)
from app.views import get_user_login_data
from app.models import Contract, Event, Client, User, ROLE, STATUS
from app.menu import menu, roles_options, restart, login_menu, \
    contract_filters, display_events_menu
from app.permissions import UserPermissions

from utils import display_contract_status, get_role

from utils import bcolors


blue = bcolors["blue"]
cyan = bcolors["cyan"]
green = bcolors["green"]


def start():
    user = get_current_user(session)
    if user:
        print(blue + f"\n WELCOME, {user.name}\n")
        menu()
        login_menu()
        print("\n")
        selections()
    else:
        name, password = get_user_login_data()
        authentification_initiale(session, name, password)
        start()


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
        display_all_events()
        edit_any_event()
    elif int(option) == 3:
        display_all_events()
    elif int(option) == 4:
        display_clients_events()
        create_contract()
    elif int(option) == 5:
        display_contracts()
        edit_contract()
    elif int(option) == 6:
        get_and_filter_all_contracts()
    elif int(option) == 7:
        create_user()
    elif int(option) == 8:
        display_all_users()
        edit_user()
    elif int(option) == 9:
        display_all_users()
    elif int(option) == 10:
        display_all_users()
        delete_user()
    elif int(option) == 11:
        create_client()
    elif int(option) == 12:
        current_user = get_current_user(session)
        display_my_clients_contracts(current_user)
        edit_one_client()
    elif int(option) == 13:
        display_all_clients()
    elif int(option) == 14:
        logout_user()
    elif int(option) == 15:
        exit()
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

# READ


def display_contracts():
    if UserPermissions.can_read_contract():
        print("🛑 You don't have the permission to create a contract")
    else:
        contracts = session.query(Contract).all()
        for contract in contracts:
            client = session.query(Client).filter(Client.id ==
                                                  contract.client_id).first()
            event = session.query(Event).filter(Event.id ==
                                                contract.event_id).first()

            support = session.query(User).filter(User.id
                                                 == event.support_contact_id).first()
            support_name = support.name if support else "No support assigned"
            client_name = client.name if support else "No Client yet    "
            print("id:", contract.id, "client:", client_name, "support: ",
                  support_name, "event:", event.name,  "status:", contract.status)
        return contracts


def display_contracts():
    if UserPermissions.can_read_contract():
        current_user = get_current_user(session)
        if current_user.role == ROLE["SALES"]:
            display_my_clients_contracts(current_user)
        elif current_user.role == ROLE["MANAGER"]:
            display_all_contracts()
        else:
            print("🛑 You don't have the permission to read a contract")
            return


def display_all_contracts():
    try:
        contracts = session.query(Contract).all()
        for contract in contracts:
            client = session.query(Client).filter(Client.id ==
                                                  contract.client_id).first()
            event = session.query(Event).filter(Event.id ==
                                                contract.event_id).first()

            support = session.query(User).filter(User.id
                                                 == event.support_contact_id).first()

            support_name = support.name if support else "No support assigned"
            client_name = client.name if client else "No Client yet"
            print("id:", contract.id, "client:", client_name, "support: ",
                  support_name, "event:", event.name,  "status:", contract.status)
        return contracts
    except Exception as e:
        # Alternatively the argument can be omitted
        print("ERROR")
        print(str(e))
        sentry_sdk.capture_exception(e)
        sentry_sdk.capture_message('Something went wrong')


def display_my_clients_contracts(current_user):
    try:

        clients = session.query(Client).filter(Client.support_id
                                               == current_user.id)
        print(current_user.id)
        print(clients)
        for client in clients:
            print("id:", client.id, ",", "name:", client.name, "email:",
                  client.email, "phone:", client.phone, "company name:",
                  client.company_name, "support: ", current_user.name)

        return clients
    except Exception as e:
        # Alternatively the argument can be omitted
        print("ERROR")
        print(str(e))
        sentry_sdk.capture_exception(e)
        sentry_sdk.capture_message('Something went wrong')


def get_and_filter_all_contracts():
    if UserPermissions.can_read_contract():
        contracts = session.query(Contract).all()
        for contract in contracts:
            client = session.query(Client).filter(Client.id ==
                                                  contract.client_id).first()
            event = session.query(Event).filter(Event.id ==
                                                contract.event_id).first()

            support = session.query(User).filter(User.id
                                                 == event.support_contact_id).first()
            support_name = support.name if support else "No support assigned"
            client_name = client.name if support else "No Client yet    "
            print("id:", contract.id, "client:", client_name, "support: ",
                  support_name, "event:", event.name,  "status:", contract.status)
        contract_filters()
        filter_display_contracts()
        return contracts
    else:
        print("🛑 You don't have the permission to create a contract")
        return


def display_all_users():
    users = session.query(User).all()
    for user in users:
        print("id:", user.id, ",", "name:", user.name, "email:",
              user.email, "phone:", user.phone, "role:",
              user.role)
    return users


def display_all_clients():
    clients = session.query(Client).all()
    for client in clients:
        support = session.query(User).filter(User.id
                                             == client.support_id).first()
        support_name = support.name if support else "No support assigned"
        print("id:", client.id, ",", "name:", client.name, "email:",
              client.email, "phone:", client.phone, "company name:",
              client.company_name, "support: ", support_name)

    return clients


def display_all_events():
    try:
        if UserPermissions.can_manager_read_events():
            events = session.query(Event).all()
            for event in events:
                support_contact_id = event.support_contact_id is None
                contact_support = "NO SUPPORT ASSIGNED" if support_contact_id else event.support_contact_id

                print(f"id:[{event.id}]", ",", "support:", contact_support,
                      "name:", event.name, "start:",
                      event.start_date, "end:", event.end_date, "location:",
                      event.location, "attendees:", event.attendees,
                      "notes:", event.notes)

        elif UserPermissions.can_support_read_events():
            current_user = get_current_user(session)
            events = session.query(Event).all()
            for event in events:
                if event.support_contact_id == current_user.id:
                    print(f"id:[{event.id}]", ",", "name:", event.name, "start:",
                          event.start_date, "end:", event.end_date, "location:",
                          event.location, "attendees:", event.attendees,
                          "notes:", event.notes)
                else:
                    print("No events found.")
        else:
            print("🛑 You don't have the permission to view events")
            return

    except Exception as e:
        # Alternatively the argument can be omitted
        print("ERROR")
        print(str(e))
        sentry_sdk.capture_exception(e)
        sentry_sdk.capture_message('Something went wrong')


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
@click.option('--value', prompt='filter')
def filter_display_contracts(value):
    contracts = []
    if int(value) == 1:
        contracts = session.query(Contract).filter(
            Contract.status == STATUS["CREATED"]).all()
    elif int(value) == 2:
        contracts = session.query(Contract).filter(
            Contract.status == STATUS["SIGNED"]).all()
    elif int(value) == 3:
        contracts = session.query(Contract).filter(
            Contract.status == STATUS["PAID"]).all()
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
            support_name = support.name if support else "No support assigned"
            print("id:", contract.id, "\n",
                  "\n", "client:", client.name, "\n",
                  "support: ", support_name, "\n",
                  "event:", event.name, "\n", "status:", contract.status)

# CREATE


@click.command()
@click.option('--name', prompt='name')
@click.option('--email', prompt='email')
@click.option('--phone', prompt='phone')
@click.option('--password', prompt='password')
def create_user(name, email, phone, password):
    try:
        if UserPermissions.can_create_user():
            roles_options()
            role = input("role: ")
            user = User(
                name=name, email=email, phone=phone,
                password=password,
                role=get_role(int(role)))
            user.set_password(password)
            session.add(user)
            session.commit()
            print("✅ user successfully created")
        else:
            print("🛑 You don't have the permission to create a user")
            return

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
        return


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
    current_user = get_current_user(session)
    if UserPermissions.can_create_client():
        client = Client(name=name, email=email, phone=phone,
                        company_name=company_name, support_id=current_user.id)
        session.add(client)
        session.commit()
        print("✅ client successfully created")
    else:
        print("🛑 You don't have the permission to create a client")
        return


# UPDATE
@click.command()
def edit_user():
    user_id = input("select user: ")
    if UserPermissions.can_update_user():
        user = session.query(User).filter(
            User.id == int(user_id)).first()

        name = input(f"name({user.name}): ")
        email = input(f"email({user.email}): ")
        phone = input(f"phone({user.phone}): ")
        roles_options()
        role = input(f"role({user.role}): ")

        user.name = name if name else user.name
        user.email = email if email else user.email
        user.phone = phone if phone else user.phone
        user.role = get_role(int(role)) if role else user.role
        session.commit()
        print("✅ user successfully edited")
    else:
        print("🛑 You don't have the permission to edit a user")
        return


@click.command()
def edit_one_client():
    client_id = input("select client: ")
    if UserPermissions.can_update_client():
        client = session.query(Client).filter(
            Client.id == int(client_id)).first()

        name = input(f"name({client.name}): ")
        email = input(f"email({client.email}): ")
        phone = input(f"phone({client.phone}): ")
        company = input(f"company name({client.company_name}): ")

        client.name = name if name else client.name
        client.email = email if email else client.email
        client.phone = phone if phone else client.phone
        client.company_name = company if company else client.company_name
        session.commit()
        print("✅ user successfully edited")
    else:
        print("🛑 You don't have the permission to edit a client")
        return


def edit_event():
    if UserPermissions.can_display_events_without_support():
        edit_event_with_no_support()
    else:
        edit_any_event()


@click.command()
@click.option('--id', prompt='select event to edit')
def edit_any_event(id):
    event = session.query(Event).filter(Event.id == int(id)).first()

    name = input(f"name({event.name}): ")
    display_all_users()
    support_id = input(f"select support ({event.support_contact_id}): ")
    start = input(f"phone({event.start_date}): ")
    end = input(f"company name({event.end_date}): ")
    location = input(f"location ({event.location}): ")
    attendees = input(f"attendeed({event.attendees}): ")
    notes = input(f"notes({event.notes}): ")

    event.name = name  # Assuming 'name' is defined elsewhere in your code
    event.support_contact_id = support_id if support_id else event.support_contact_id
    event.start_date = datetime.datetime.strptime(
        start, '%Y-%m-%d') if start else event.start_date
    event.end_date = datetime.datetime.strptime(
        end, '%Y-%m-%d') if end else event.end_date
    event.location = location if location else event.location
    event.attendees = int(
        attendees) if attendees else event.attendees  # Fixed line
    event.notes = notes if notes else event.notes
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


@click.command()
@click.option('--id', prompt='select contract to edit')
def edit_contract(id):
    try:
        if UserPermissions.can_update_contract():
            contract = session.query(Contract).filter(
                Contract.id == int(id)).first()
            contract_filters()

            status = input(f"Edit current status: ")
            contract.status = display_contract_status(status)
            session.commit()
            print("✅ contract successfully edited")
        else:
            print("🛑 You don't have the permission to update a contract")
            return

    except Exception as e:
        print(str(e))
        sentry_sdk.capture_exception(e)
        sentry_sdk.capture_message('Something went wrong')


def display_my_contract(id):
    current_user = get_current_user(session)
    try:
        client = session.query(Client).filter(Client.id == int(id)).first()
        contracts = session.query(Contract).filter(
            client.support_id == current_user.id).all()
        display(contracts)
    except Exception as e:
        print(str(e))
        sentry_sdk.capture_exception(e)
        sentry_sdk.capture_message('Something went wrong')


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
@click.option('--id', prompt='select user:')
def delete_user(id):
    try:
        if UserPermissions.can_delete_user():
            session.query(User).filter(User.id == int(id)).delete(
                synchronize_session='evaluate')
            session.commit()
            print("✅ user successfully deleted")
        else:
            print("🛑 You don't have the permission to edit a user")
            return

    except Exception as e:
        # Alternatively the argument can be omitted
        print("ERROR")
        print(str(e))
        sentry_sdk.capture_exception(e)
        sentry_sdk.capture_message('Something went wrong')


if __name__ == '__main__':
    start()
    # menu()
    # selections()
