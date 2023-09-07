import sqlite3
import random
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
    return_value = False
    if (web_app_user == db_web_app_user and
            web_app_pass == db_web_app_pass and
            config_location == db_config_location):
        return_value = True
    print(colored("Correct Values:", "green"))
    if web_app_user == db_web_app_user:
        print("Webapp Username: ", web_app_user)
    if web_app_pass == db_web_app_pass:
        print("Webapp Password: ", web_app_pass)
    if config_location == db_config_location:
        print("Webapp Config: ", config_location)
    if (return_value == False):
        print(colored("Incorrect Values:", "red"))
        if web_app_user != db_web_app_user:
            print("Webapp Username: ", web_app_user)
        if web_app_pass != db_web_app_pass:
            print("Webapp Password: ", web_app_pass)
        if config_location != db_config_location:
            print("Webapp Config: ", config_location)
    else:
        print(colored("Great Job!", "green"))
    return return_value

def main():
    connection = sqlite3.connect('webapps.db')
    stop = 'n'

    num_rows = 2
    rows = [x for x in range(1,num_rows+1)]
    random.shuffle(rows)
    current_row = 0

    while(stop != 'y' and current_row < num_rows):
        row_number = rows[current_row]
        current_row += 1
        row_data = read_row(connection, row_number)
        if row_data:
            _, vm_name, _, db_web_app_user, db_web_app_pass, _, os_user, os_pass, db_config_location = row_data

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

        stop = input("Do you want to quit? (y/n): ")

    connection.close()

if __name__ == '__main__':
    main()
