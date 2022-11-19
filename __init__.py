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
