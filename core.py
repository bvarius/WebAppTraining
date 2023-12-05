# Import necessary libraries
import sqlite3
import random
from flask import Flask, render_template, request, session
from termcolor import colored

app = Flask(__name__)

app.secret_key = '12345'

def get_row_count(database):
    conn = sqlite3.connect(database)

    cursor = conn.cursor()

    table_name = 'vms'
    query = f'SELECT COUNT(*) FROM {table_name}'

    cursor.execute(query)

    row_count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return row_count

# Define a route to render the initial page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/web_apps', methods=['GET', 'POST'])
def web_apps():

    connection = sqlite3.connect('webapps.db')

    if (request.method == 'GET'): #First time through
        #randomize list
        res_message = ''
        session['row_numbers'] = [x for x in range(1,get_row_count('webapps.db')+1)]
        random.shuffle(session['row_numbers'])
        session['correct_answers'] = 0
        session['attempts'] = 0

    else:
        #increment attempts count
        session['attempts'] += 1
        # Retrieve form data
        web_app_user = request.form['webapp_user']
        web_app_pass = request.form['webapp_pass']
        config_location = request.form['webapp_path']

        result = validate_credentials(web_app_user, web_app_pass, config_location,
                                        session['db_web_app_user'], session['db_web_app_pass'], session['db_config_location'])
        #check credentials
        if (result):
            session['correct_answers'] += 1
            res_message = 'Correct! Great Job!'
            #select next question info
            session['current_row'] = session['row_numbers'].pop(0)
            row_data = read_row(connection, session['current_row'])
            connection.close()
            if row_data:
                _, session['vm_name'], _, session['db_web_app_user'], session['db_web_app_pass'], _, session['os_user'], session['os_pass'], session['db_config_location'] = row_data
            else:
                return "Invalid row number"

            #check if row_numbers array is empty
            if (not session['row_numbers']):
                #display results page
                return render_template('result.html', correct_answers=session['correct_answers'], attempts=session['attempts'])
        else:
            res_message = 'Incorrect! Try Again!'

    return render_template('web_apps.html', vm_name=session['vm_name'], os_user=session['os_user'], os_pass=session['os_pass'], res_message=res_message)

@app.route('/win_firewalls', methods=['GET','POST'])
def firewalls():
    connection = sqlite3.connect('firewalls.db')
    
    if (request.method == 'GET'): #First time through
        #randomize list
        res_message = ''
        session['row_numbers'] = [x for x in range(1,get_row_count('firewalls.db')+1)]
        random.shuffle(session['row_numbers'])
        session['correct_answers'] = 0
        session['attempts'] = 0

    else:
        #increment attempts count
        session['attempts'] += 1
        # Retrieve form data
        web_app_user = request.form['webapp_user']
        web_app_pass = request.form['webapp_pass']
        config_location = request.form['webapp_path']

        result = validate_credentials(web_app_user, web_app_pass, config_location,
                                        session['db_web_app_user'], session['db_web_app_pass'], session['db_config_location'])
        #check credentials
        if (result):
            session['correct_answers'] += 1
            res_message = 'Correct! Great Job!'
            #select next question info
            session['current_row'] = session['row_numbers'].pop(0)
            row_data = read_row(connection, session['current_row'])
            connection.close()
            if row_data:
                _, session['vm_name'], _, session['db_web_app_user'], session['db_web_app_pass'], _, session['os_user'], session['os_pass'], session['db_config_location'] = row_data
            else:
                return "Invalid row number"

            #check if row_numbers array is empty
            if (not session['row_numbers']):
                #display results page
                return render_template('result.html', correct_answers=session['correct_answers'], attempts=session['attempts'])
        else:
            res_message = 'Incorrect! Try Again!'

    return render_template('firewalls.html')#, service_name, port, executable, ip_address)

@app.route('/update_form', methods=['GET', 'POST'])
def update_form():
    return render_template('add_vm_form.html')

@app.route('/update_database', methods=['POST'])
def update_database():
    connection = sqlite3.connect('webapps.db')

    vm_name = request.form['vm_name']
    webapp_name = request.form['webapp_name']
    webapp_user = request.form['webapp_user']
    webapp_pass = request.form['webapp_pass']
    os_type = request.form['os_type']
    os_user = request.form['os_user']
    os_pass = request.form['os_pass']
    config_location = request.form['config_location']
    
    create_entry(conn=connection, vm_name=vm_name, web_app_name=webapp_name, web_app_user=webapp_user, web_app_pass=webapp_pass,
                 os_type=os_type, os_user=os_user, os_pass=os_pass, config_location=config_location)
    
    connection.close()
    return render_template('update_complete.html')
def create_entry(conn, vm_name, web_app_name, web_app_user, web_app_pass,
                 os_type, os_user, os_pass, config_location):

    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS vms (
                id INTEGER PRIMARY KEY,
                vm_name TEXT,
                web_app_name TEXT, web_app_user TEXT,
                web_app_pass TEXT,
                os_type TEXT,
                os_user TEXT,
                os_pass TEXT,
                config_location TEXT
            )
        ''')
    query = """
    INSERT INTO vms (vm_name, web_app_name, web_app_user, web_app_pass, os_type, os_user, os_pass, config_location)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, (vm_name, web_app_name, web_app_user, web_app_pass,
                           os_type, os_user, os_pass, config_location))
    conn.commit()

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

def validate_rule():
    return True

if __name__ == '__main__':
    app.run(debug=True)