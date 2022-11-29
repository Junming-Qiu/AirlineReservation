from flask import Flask, render_template, request, session, url_for, redirect
from flask_mysqldb import MySQL
import os
import sys
sys.path.insert(0, os.getcwd())

from utils.customer import *
from utils.staff import *
from utils.public_info import *
from utils.general import *
from utils.register import *
from utils.login import *

global customer_tokens
global staff_tokens

customer_tokens = {}
staff_tokens = {}

app = Flask(__name__)
app.static_folder = 'static'


app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'walrus123' # TODO: Change this password
app.config['MYSQL_DB'] = 'flight_app'
app.config['MYSQL_PORT'] = 8080 # TODO: Change this port

mysql = MySQL(app)

with app.app_context():
    curs = mysql.connection.cursor()


# Define a route to hello function
@app.route('/')
def hello():
    return render_template('index.html')


### PUBLIC FLIGHT INFO ###
'''
1. View Public Info: All users, whether logged in or not, can

a. Search for future flights based on source city/airport name, destination city/airport name,
    departure date for one way (departure and return dates for round trip).

b. Will be able to see the flights status based on airline name, flight number, arrival/departure date.
'''
@app.route('/public')
def public():
    headings,data=public_view_oneway_flights(mysql)
    return render_template('public_info.html',headings=headings,data=data)

@app.route("/public_view_flights", methods=['GET', 'POST'])
def public_view_flight():
    try:
        f_type = request.form['flight_type']
        if f_type=='two way':
            headings, data = public_view_twoway_flights(mysql)
            return render_template('public_info.html', headings=headings, data=data)
        if f_type=='one way':
            headings, data = public_view_oneway_flights(mysql)
            return render_template('public_info.html', headings=headings, data=data)
        else:
            error="Flight Type must be 'one way' or 'two way'"
            render_template('public_info.html', error=error)            # error msg not displaying for some reason
    except:
        pass
    headings, data = public_view_oneway_flights(mysql)
    return render_template('public_info.html', headings=headings, data=data)

### STAFF LOG IN ###

@app.route("/staff")
def staff():
    _, s_logged = store_verify(session, customer_tokens, staff_tokens)
    if s_logged:
        return render_template('staff home.html') #TODO: CHANGE TO STAFF HOMEPAGE
    return redirect(url_for("login_staff"))

@app.route('/login_staff')
def login_staff():
    _, s_logged = store_verify(session, customer_tokens, staff_tokens)

    if s_logged:
        return redirect(url_for("staff"))

    return render_template('login_staff.html')

@app.route('/loginAuthStaff', methods=['POST', 'GET'])
def loginAuthStaff():
    try:
        username = request.form['username']
        employer = request.form['employer']
        password = request.form['password']
    except:
        return redirect(url_for("login_staff"))

    # Parse input for security
    if not parse_input([username]):
        return redirect(url_for("login_staff"))

    if not parse_input([employer]):
        return redirect(url_for("login_staff"))

    if not parse_input([password], True):
        return redirect(url_for("login_staff"))

    is_staff = query_staff_credentials(username, password, employer, mysql)

    if is_staff:
        session['username'] = username
        session['key'] = encrypt_password(username + password)
        session['employer'] = employer
        staff_tokens[username] = session["key"]
        return redirect(url_for("staff"))

    error = 'Log in credentials are incorrect'
    return render_template('login_staff.html', error=error)



### CUSTOMER LOG IN ###
# Define route for login
@app.route('/login_customer')
def login_customer():
    c_logged, _ = store_verify(session, customer_tokens, staff_tokens)

    if c_logged:
        return redirect(url_for("customer"))

    return render_template('login_customer.html')

@app.route("/customer")
def customer():
    c_logged, _ = store_verify(session, customer_tokens, staff_tokens)
    if c_logged:
        return render_template('customer home.html') #TODO: CHANGE TO CUSTOMER HOMEPAGE
    return redirect(url_for("login_customer"))

@app.route('/loginAuthCust', methods=['POST', 'GET'])
def loginAuthCust():
    try:
        email = request.form['username']
        password = request.form['password']
    except:
        return redirect(url_for("login"))

    # Parse input for security
    if not parse_input([email]):
        return redirect(url_for("login"))


    if not parse_input([password], True):
        return redirect(url_for("login"))

    is_customer = query_customer_credentials(email, password, mysql)
    if is_customer:
        session['username'] = email
        session['key'] = encrypt_password(email + password)
        customer_tokens[email] = session["key"]
        return redirect(url_for("customer"))

    error = 'Log in credentials are incorrect'
    return render_template('login_customer.html', error=error)

@app.route('/logout')
def logout():
    session["username"] = ""
    session["key"] = ""
    session["employer"] = ""
    return redirect(url_for("login"))



### STAFF REGISTER ###

# Define route for staff register
@app.route('/register_staff')
def register_staff():
    return render_template('register staff.html')

# Authenticates the register
@app.route('/registerAuthStaff', methods=['GET', 'POST'])
def registerAuthStaff():
    username = ""
    password = ""
    fname = ""
    lname = ""
    dob = ""
    employer = ""

    # Check all input is there
    try:
        username = request.form['username']
        password = request.form['password']
        fname = request.form['fname']
        lname = request.form['lname']
        dob = request.form['dob']
        employer = request.form['employer']

    except:
        error = "Input Missing"
        return render_template('register staff.html', error=error)

    # Parse input for security
    if not parse_input([password], True):
        error = "Username or Password Error. Password may not contain space or '\Z', '\\', '\%', '\_', \
        '?', '-', '(', ')', '{', '}', '[', ']', and must be 8 characters or more"
        return render_template('register staff.html', error=error)

    if not parse_input([username, fname, lname, dob, employer]):
        error = "Input Error"
        return render_template('register staff.html', error=error)

    # check if username exists
    if query_staff_username(username, mysql):
        error = f'Account with username {username} already exists'
        return render_template('register staff.html', error=error)

    # check if employer does not exist
    if not query_staff_employer(employer, mysql):
        error = f'Airline {employer} does not exist'
        return render_template('register staff.html', error=error)

    # create account
    create_staff_account(username, password, fname,
                         lname, dob, employer, mysql)
    # render homepage
    return render_template('index.html')  # TODO: change to homepage



### CUSTOMER REGISTER ###

# Define route for customer register
@app.route('/register_customer')
def register_customer():
    return render_template('register customer.html')

# Authenticates the register
@app.route('/registerAuthCustomer', methods=['GET', 'POST'])
def registerAuthCustomer():
    email = ""
    name = ""
    password = ""
    building_num = ""
    city = ""
    state = ""
    street = ""
    pp_country = ""
    pp_num = ""
    pp_expr = ""
    dob = ""
    phone_num = ""

    # Make sure all input is there
    try:
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
    except:
        error = "Input Missing"
        return render_template('register customer.html', error=error)

    # Parse input for security
    if not parse_input([password], True):
        error = "Username or Password Error. Password may not contain space or '\Z', '\\', '\%', '\_', \
        '?', '-', '(', ')', '{', '}', '[', ']', and must be 8 characters or more"
        return render_template('register customer.html', error=error)

    if not parse_input([email, name, building_num, city, state, street, pp_country, pp_num, pp_expr, dob, phone_num]):
        error = "Input Error"
        return render_template('register customer.html', error=error)

    # check if email exists
    if query_customer_email(email, mysql):
        error = f'Account with email {email} already exists'
        return render_template('register customer.html', error=error)

    # create account
    create_customer_account(email,name,password,building_num,city,state,
                            street,pp_country,pp_num,pp_expr,dob,phone_num, mysql)

    # render homepage
    return render_template('index.html') #TODO: change to homepage



#
app.secret_key = 'some key that you will never guess'
# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask
# for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)