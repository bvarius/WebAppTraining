import sqlite3
import argparse


def create_entry(conn, vm_name, web_app_name, web_app_user, web_app_pass,
                 os_type, os_user, os_pass, config_location):
    """
    Create a new entry in the SQLite database.
    """
    cursor = conn.cursor()
    query = """
    INSERT INTO vms (vm_name, web_app_name, web_app_user, web_app_pass, os_type, os_user, os_pass, config_location)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, (vm_name, web_app_name, web_app_user, web_app_pass,
                           os_type, os_user, os_pass, config_location))
    conn.commit()

def check_fields(fields):
    for field in fields:
        if (fields[field] != ''):
            fields[field] = prompt_user_for_field(field)

def prompt_user_for_field(field_name):
    """
    Prompt the user to enter a value for a field.
    """
    return input(f"Enter {field_name}: ")

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--vm_name', help='VM name')
    parser.add_argument('--web_app_name', help='Web application name')
    parser.add_argument('--web_app_user', help='Web application username')
    parser.add_argument('--web_app_pass', help='Web application password')
    parser.add_argument('--os_type', help='Operating system type')
    parser.add_argument('--os_user', help='Operating system username')
    parser.add_argument('--os_pass', help='Operating system password')
    parser.add_argument('--config_location', help='Configuration location')
    args = parser.parse_args()

    # Get field values
    row = {}
    row['vm_name'] = args.vm_name
    row['web_app_name'] = args.web_app_name
    row['web_app_user'] = args.web_app_user
    row['web_app_pass'] = args.web_app_pass
    row['os_type'] = args.os_type
    row['os_user'] = args.os_user
    row['os_pass'] = args.os_pass
    row['config_location'] = args.config_location

    check_fields(row)

    # Connect to the SQLite database
    connection = sqlite3.connect('webapps.db')

    # Create the entry in the database
    create_entry(connection, row['vm_name'], row['web_app_name'], row['web_app_user'], row['web_app_pass'],
                 row['os_type'], row['os_user'], row['os_pass'], row['config_location'])

    # Close the database connection
    connection.close()
    
if __name__ == '__main__':
    main()
