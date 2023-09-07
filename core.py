# Import necessary libraries
import sqlite3
import random
from flask import Flask, render_template, request, session
from termcolor import colored

app = Flask(__name__)

app.secret_key = '12345'

NUM_ROWS = 2
ROWS = [x for x in range(1,NUM_ROWS+1)]
CURRENT_ROW = 0
CORRECT_ANSWERS = 0
ATTEMPTS = 0

# Define a route to render the initial page
@app.route('/')
def index():
    #reset variables if not first time through
    global CURRENT_ROW, CORRECT_ANSWERS, ATTEMPTS
    random.shuffle(ROWS)
    CURRENT_ROW = 0
    CORRECT_ANSWERS = 0
    ATTEMPTS = 0
    
    # Connect to the SQLite database
    connection = sqlite3.connect('webapps.db')

    row_number = ROWS[CURRENT_ROW]
    row_data = read_row(connection, row_number)
    connection.close()

    if row_data:
        _, vm_name, _, _r, _, _, os_user, os_pass, _ = row_data
        session['row_number'] = row_number

    else:
        return "Invalid row number"

    return render_template('index.html', vm_name=vm_name, os_user=os_user, os_pass=os_pass)

# Define a route to handle the form submission and display results
@app.route('/check_credentials', methods=['POST'])
def check_credentials():
    global ATTEMPTS, CORRECT_ANSWERS, CURRENT_ROW

    connection = sqlite3.connect('webapps.db')

    row_number = session['row_number']

    row_data = read_row(connection, row_number)
    if row_data:
        _, vm_name, _, db_web_app_user, db_web_app_pass, _, os_user, os_pass, db_config_location = row_data

    # Retrieve form data
    web_app_user = request.form['webapp_user']
    web_app_pass = request.form['webapp_pass']
    config_location = request.form['webapp_path']

    result = validate_credentials(web_app_user, web_app_pass, config_location,
                                        db_web_app_user, db_web_app_pass, db_config_location)

    ATTEMPTS += 1

    if (result):
        CORRECT_ANSWERS += 1
        CURRENT_ROW += 1

        if CURRENT_ROW >= NUM_ROWS:
            return render_template('result.html', correct_answers=CORRECT_ANSWERS, attempts=ATTEMPTS)
        row_number = ROWS[CURRENT_ROW]
        row_data = read_row(connection, row_number)

        if row_data:
            _, vm_name, _, _r, _, _, os_user, os_pass, _ = row_data
            session['row_number'] = row_number

        else:
            connection.close()
            return "Invalid row number"
    connection.close()
    # Render the results using a template
    return render_template('feedback.html', vm_name=vm_name, os_user=os_user, os_pass=os_pass,
                           result=result)

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

if __name__ == '__main__':
    app.run(debug=True)