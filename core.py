import sqlite3
from termcolor import colored

def read_row(connection, row_number):
    cursor = connection.cursor()
    query = "SELECT * FROM vms WHERE id = ?"
    cursor.execute(query, (row_number,))
    return cursor.fetchone()

def print_vm_info(vm_name, os_user, os_pass):
    print("VM Name:", vm_name)
    print("OS User:", os_user)
    print("OS Pass:", os_pass)

def validate_credentials(web_app_user, web_app_pass, config_location, db_web_app_user, db_web_app_pass, db_config_location):
    if (web_app_user == db_web_app_user and
            web_app_pass == db_web_app_pass and
            config_location == db_config_location):
        print(colored("Great Job!", "green"))
        print_vm_info(db_web_app_user, db_web_app_pass, db_config_location)
        return True
    else:
        print(colored("Correct Values:", "green"))
        if web_app_user == db_web_app_user:
            print("Webapp Username: ", web_app_user)
        if web_app_pass == db_web_app_pass:
            print("Webapp Password: ", web_app_pass)
        if config_location == db_config_location:
            print("Webapp Config: ", config_location)
        print(colored("Incorrect Values:", "red"))
        if web_app_user != db_web_app_user:
            print("Webapp Username: ", web_app_user)
        if web_app_pass != db_web_app_pass:
            print("Webapp Password: ", web_app_pass)
        if config_location != db_config_location:
            print("Webapp Config: ", config_location)
        return False

def main():
    connection = sqlite3.connect('webapps.db')
    row_number = int(input("Enter the row number: "))

    row_data = read_row(connection, row_number)
    if row_data:
        _, vm_name, _, db_web_app_user, db_web_app_pass, _, os_user, os_pass, db_config_location = row_data
        print(row_data)

        print_vm_info(vm_name, os_user, os_pass)

        while True:
            web_app_user = input("Enter Webapp username: ")
            web_app_pass = input("Enter Webapp password: ")
            config_location = input("Enter config file path: ")

            if validate_credentials(web_app_user, web_app_pass, config_location,
                                    db_web_app_user, db_web_app_pass, db_config_location):
                break
    else:
        print("Invalid row number.")

    connection.close()

if __name__ == '__main__':
    main()
