import click
import datetime
from app.config import session


from app.models import Contract, Event, Client, Collaborator
from app.menu import menu, roles_options, restart, contract_filters
from app.permissions import UserPermissions

from utils import display_contract_status, display_role_status, get_current_user, get_role
import sentry_sdk

# MENU


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
        create_collaborator()
    elif int(option) == 8:
        edit_collaborator()
    elif int(option) == 9:
        get_all_collaborators()
    elif int(option) == 10:
        delete_collaborator()
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

# READ


def get_all_contracts():
    current_user = get_current_user()
    if UserPermissions.can_read_contract(current_user):
        contracts = session.query(Contract).all()
        for contract in contracts:
            client = session.query(Client).filter(Client.id ==
                                                  contract.client_id).first()
            event = session.query(Event).filter(Event.id ==
                                                contract.event_id).first()

            support = session.query(Collaborator).filter(Collaborator.id
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


def get_all_collaborators():
    collaborators = session.query(Collaborator).all()
    for collaborator in collaborators:
        print("id:", collaborator.id, ",", "name:", collaborator.name, "email:",
              collaborator.email, "phone:", collaborator.phone, "role:",
              display_role_status(collaborator.role))
    return collaborators


def get_all_clients():
    clients = session.query(Client).all()
    for client in clients:
        support = session.query(Collaborator).filter(Collaborator.id
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

            support = session.query(Collaborator).filter(Collaborator.id
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
def create_collaborator(name, email, phone, role):
    try:
        role_name = get_role(role)
        current_user = get_current_user()

        if UserPermissions.can_create_collaborator(current_user) or UserPermissions.can_update_collaborator(current_user) or UserPermissions.can_delete_collaborator(current_user):

            collaborator = Collaborator(
                name=name, email=email, phone=phone, role=role_name)
            session.add(collaborator)
            session.commit()
            print("✅ collaborator successfully created")
        else:
            print("🛑 You don't have the permission to create a collaborator")
    except Exception as e:
        # Alternatively the argument can be omitted
        sentry_sdk.capture_exception(e)
        sentry_sdk.capture_message('Something went wrong')


@click.command()
@click.option('--event_id', prompt='select event')
@click.option('--client_id', prompt='select client')
@click.option('--response', prompt='create contract ? [y/n]]')
def create_contract(client_id, event_id, response):
    current_user = get_current_user()
    if UserPermissions.can_create_contract(current_user) or UserPermissions.can_update_contract(current_user):
        contract = Contract(client_id=int(client_id), event_id=int(event_id),
                            created_at=datetime.datetime.now())
        if response == "y":
            session.add(contract)
            session.commit()
            print("✅ collaborator successfully created")
    else:
        print("🛑 You don't have the permission to create a collaborator")


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
    if UserPermissions.can_create_client(current_user):
        client = Client(name=name, email=email, phone=phone,
                        company_name=company_name, support_id=current_user.id)
        session.add(client)
        session.commit()
        print("✅ collaborator successfully created")
    else:
        print("🛑 You don't have the permission to create a client")


# UPDATE


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


def edit_client():
    current_user = get_current_user()
    if UserPermissions.can_update_client(current_user):
        clients = session.query(Client).filter(
            Client.support_id == current_user.id).first()
        edit_one_client()
        for client in clients:
            print("id:", client.id, ",", "name:", client.name, "email:",
                  client.email, "phone:", client.phone, "company name:",
                  client.company_name)
    else:
        print("🛑 You don't have the permission to create a client")


@click.command()
@click.option('--name', prompt='name')
@click.option('--email', prompt='email')
@click.option('--phone', prompt='phone')
@click.option('--id', prompt='phone')
def edit_one_client(id, name, email, phone):
    client = session.query(Client).filter(
        Client.id == int(id)).first()

    client.name = name
    client.email = email
    client.phone = phone
    session.commit()


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
        Collaborator).filter(Collaborator.id == int(id)).first()
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
    if UserPermissions.can_update_client(current_user):
        for contract in contracts:

            event = session.query(Event).filter(Event.id ==
                                                contract.event_id).first()

            support = session.query(Collaborator).filter(Collaborator.id
                                                         == event.support_contact_id).first()

            print("id:", contract.id, "\n",
                  "\n", "client:", client.name, "\n",
                  "support: ", support.name, "\n",
                  "event:", event.name, "\n", "status:",
                  display_contract_status(contract.status))
        edit_contract_my_clients()
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
def delete_collaborator(id):
    session.query(Collaborator).delete(
        Collaborator.id == int(id)).first()
    print("user successfully deleted")
    session.commit()


if __name__ == '__main__':
    menu()
    selections()
