def get_user_data():
    name = input("Enter user name: ")
    lastname = input("Enter user last name: ")
    password = input("Enter user password: ")
    role = input("Enter user role: ")

    return name, lastname, password, role


def get_user_login_data():
    name = input("Enter user name: ")
    password = input("Enter user password: ")

    return name, password