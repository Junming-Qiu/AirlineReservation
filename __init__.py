# Import Flask Library
#from functions import *
from flask import Flask, render_template, request, session, url_for, redirect
from flask_mysqldb import MySQL
import hashlib


# TODO LIST
# 3. get seperate files working together




# Initialize the app from Flask
app = Flask(__name__)


app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '***' # TODO: Change this password
app.config['MYSQL_DB'] = 'flight_app'
app.config['MYSQL_PORT'] = 8080

mysql = MySQL(app)

with app.app_context():
    curs = mysql.connection.cursor()

#############################################################

# *******
# GENERAL
# *******

# execute a sql statement
def exec_sql(sql: str) -> list:
    cur = mysql.connection.cursor()
    cur.execute(sql)
    return cur.fetchall()

# returns an encrypted password
def encrypt_password(password: str) -> str:
    hash_object = hashlib.md5(password.encode())
    return hash_object.hexdigest()


# ******
# LOG IN
# ******

# check if a staff's log in credentials exists
def query_staff_credentials(USERNAME: str, PASSWORD: str) -> list:
    ENCRYPTED_PASSWORD = encrypt_password(PASSWORD)
    sql = f'''
        SELECT *
        FROM airline_staff
        WHERE username = '{USERNAME}'
            AND password = '{ENCRYPTED_PASSWORD}';
        '''
    return exec_sql(sql)

# check if a customer's log in credentials exists
def query_customer_credentials(EMAIL: str, PASSWORD: str) -> list:
    ENCRYPTED_PASSWORD = encrypt_password(PASSWORD)
    sql = f'''
        SELECT *
        FROM customer
        WHERE email = '{EMAIL}'
            AND password = '{ENCRYPTED_PASSWORD}';
        '''
    return exec_sql(sql)


# ******************
# STAFF REGISTRATION
# ******************

# check if a staff's username exists
def query_staff_username(USERNAME: str) -> bool:
    sql = f'''
    SELECT *
    FROM airline_staff
    WHERE username = '{USERNAME}';
    '''
    username_exists = exec_sql(sql)
    if username_exists:
        return True
    return False

# check if a staff's employer exists
def query_staff_employer(EMPLOYER: str) -> bool:
    sql = f'''
    SELECT *
    FROM airline
    WHERE name = '{EMPLOYER}';
    '''
    employer_exists = exec_sql(sql)
    if employer_exists:
        return True
    return False

# create a staff account
def create_staff_account(USERNAME: str, PASSWORD: str, FNAME: str,
                         LNAME: str, DOB: str, EMPLOYER: str) -> None:
    ENCRYPTED_PASSWORD = encrypt_password(PASSWORD)
    sql = f'''
    INSERT INTO airline_staff
    VALUES ('{USERNAME}','{ENCRYPTED_PASSWORD}','{FNAME}',
        '{LNAME}','{DOB}','{EMPLOYER}');
    '''
    exec_sql(sql)

# *********************
# CUSTOMER REGISTRATION
# *********************

# check if a customer's email exists
def query_customer_email(EMAIL: str) -> bool:
    sql = f'''
    SELECT *
    FROM customer
    WHERE email = '{EMAIL}';
    '''

    account_exists = exec_sql(sql)
    if account_exists:
        return True
    return False

# create a customer account
def create_customer_account(EMAIL: str,NAME: str,PASSWORD: str,BUILDING_NUM: str,CITY: str,STATE: str,
                            STREET: str,PP_COUNTRY: str,PP_NUM: str,PP_EXPR: str,DOB: str,PHONE_NUM: str,) -> None:
    ENCRYPTED_PASSWORD = encrypt_password(PASSWORD)
    sql = f'''
    INSERT INTO customer
    VALUES ('{EMAIL}','{NAME}','{ENCRYPTED_PASSWORD}','{BUILDING_NUM}','{CITY}','{STATE}',
            '{STREET}','{PP_COUNTRY}','{PP_NUM}','{PP_EXPR}','{DOB}','{PHONE_NUM}');
    '''
    exec_sql(sql)

###################################################################


# Define a route to hello function
@app.route('/')
def hello():
    return render_template('index.html')

# Define route for login
@app.route('/login')
def login():
    return render_template('login.html')

# Define route for staff register
@app.route('/register_staff')
def register_staff():
    return render_template('register staff.html')

# Define route for customer register
@app.route('/register_customer')
def register_customer():
    return render_template('register customer.html')

# Authenticates the register
@app.route('/registerAuthStaff', methods=['GET', 'POST'])
def registerAuthStaff():
    username = request.form['username']
    password = request.form['password']
    fname = request.form['fname']
    lname = request.form['lname']
    dob = request.form['dob']
    employer = request.form['employer']

    # check if username exists
    if query_staff_username(username):
        error = f'Account with username {username} already exists'
        return render_template('register staff.html', error=error)

    # check if employer does not exist
    if not query_staff_employer(employer):
        error = f'Airline {employer} does not exist'
        return render_template('register staff.html', error=error)

    # create account
    create_staff_account(username, password, fname,
                         lname, dob, employer)
    # render homepage
    return render_template('index.html') #TODO: change to homepage


@app.route('/registerAuthCustomer', methods=['GET', 'POST'])
def registerAuthCustomer():
    email = request.form['email']
    name = request.form['name']
    password = request.form['password']
    building_num = request.form['building_num']
    city = request.form['city']
    state = request.form['state']
    street = request.form['street']
    pp_country = request.form['pp_country']
    pp_num = request.form['pp_num']
    pp_expr = request.form['pp_expr']
    dob = request.form['dob']
    phone_num = request.form['phone_num']

    # check if email exists
    if query_customer_email(email):
        error = f'Account with email {email} already exists'
        return render_template('register customer.html', error=error)

    # create account
    create_customer_account(email,name,password,building_num,city,state,
                            street,pp_country,pp_num,pp_expr,dob,phone_num)

    # render homepage
    return render_template('index.html') #TODO: change to homepage

@app.route('/loginAuth', methods=['POST', 'GET'])
def loginAuth():
    username_or_email = request.form['username']
    password = request.form['password']

    is_staff = query_staff_credentials(username_or_email, password)
    is_customer = query_customer_credentials(username_or_email, password)

    if is_staff:
        session['username'] = username_or_email
        return render_template('index.html') #TODO: CHANGE TO STAFF HOMEPAGE

    if is_customer:
        session['username'] = username_or_email
        return render_template('index.html') #TODO: CHANGE TO CUSTOMER HOMEPAGE

    error = 'Log in credentials are incorrect'
    return render_template('login.html', error=error)


#
app.secret_key = 'some key that you will never guess'
# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask
# for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
