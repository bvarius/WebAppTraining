import sqlite3
import argparse


def create_entry(connection, vm_name, web_app_name, web_app_user, web_app_pass,
                 os_type, os_user, os_pass, config_location):
    """
    Create a new entry in the SQLite database.
    """
    cursor = connection.cursor()
    query = """
    INSERT INTO vms (vm_name, web_app_name, web_app_user, web_app_pass, os_type, os_user, os_pass, config_location)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, (vm_name, web_app_name, web_app_user, web_app_pass,
                           os_type, os_user, os_pass, config_location))
    connection.commit()


def prompt_user_for_field(field_name):
    """
    Prompt the user to enter a value for a field.
    """
    return input(f"Enter {field_name}: ")


def get_field_value(field_name, args):
    """
    Get the value of a field either from command line arguments or by prompting the user.
    """
    value = getattr(args, field_name.replace('_', '-'))
    if value:
        return value
    return prompt_user_for_field(field_name)


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--vm-name', help='VM name')
    parser.add_argument('--web-app-name', help='Web application name')
    parser.add_argument('--web-app-user', help='Web application username')
    parser.add_argument('--web-app-pass', help='Web application password')
    parser.add_argument('--os-type', help='Operating system type')
    parser.add_argument('--os-user', help='Operating system username')
    parser.add_argument('--os-pass', help='Operating system password')
    parser.add_argument('--config-location', help='Configuration location')
    args = parser.parse_args()

    # Get field values
    vm_name = get_field_value('vm_name', args)
    web_app_name = get_field_value('web_app_name', args)
    web_app_user = get_field_value('web_app_user', args)
    web_app_pass = get_field_value('web_app_pass', args)
    os_type = get_field_value('os_type', args)
    os_user = get_field_value('os_user', args)
    os_pass = get_field_value('os_pass', args)
    config_location = get_field_value('config_location', args)

    # Connect to the SQLite database
    connection = sqlite3.connect('webapps.db')

    # Create the entry in the database
    create_entry(connection, vm_name, web_app_name, web_app_user, web_app_pass,
                 os_type, os_user, os_pass, config_location)

    # Close the database connection
    connection.close()
