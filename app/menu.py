from utils import bcolors


blue = bcolors["blue"]
cyan = bcolors["cyan"]
green = bcolors["green"]
header = bcolors["header"]
white = bcolors["white"]
yellow = bcolors["yellow"]


def roles_options():
    print("\n")
    print("======== ROLES =========")
    print("[1] - sales representative")
    print("[2] - customer support")
    print("[3] - account manager")
    print("===CREATE NEW USER===")


def menu():
    print(green + "======== MENU =========")
    print("[1] - create new event")
    print("[2] - edit event")
    print("[3] - display all events")
    print("=========================")
    print("[4] - create new contract")
    print("[5] - edit contract")
    print("[6] - display all contracts")
    print("=========================")
    print("[7] - create new user")
    print("[8] - edit user")
    print("[9] - display all users")
    print("[10] - delete user")
    print("=========================")
    print("[11] - create new client")
    print("[12] - edit client")
    print("[13] - display all clients" + white)


def restart():
    print("\n")
    print(green + "======== MENU =========")
    print("[1] - make another query")
    print("[2] - quit")
    print("=========================" + white)
    print("\n")


def display_events_menu():
    print("\n")
    print(green + "======== MENU =========")
    print("[1] - display all events")
    print("[2] - filter event with no support contact")
    print("=========================" + white)
    print("\n")


def contract_filters():
    print("\n")
    print(green + "======== CONTRACTS =========")
    print("[1] - created")
    print("[2] - signed")
    print("[3] - paid" + white)


def login_menu():
    print(green + "=======================")
    print("[14] - logout")
    print("[15] - exit" + white)
