# Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import os
import sys
sys.path.insert(0, os.getcwd())

from utils.staff import *
from utils.customer import *
from utils.general import *
global customer_tokens
global staff_tokens

customer_tokens = {}
staff_tokens = {}
#       TODO -> CONSTRAINT: for flight on airplane, # tickets of flight <= # seats of airplane // don't allow customers to overbook flights

# Initialize the app from Flask
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

# Define route for login
@app.route('/login')
def login():
    c_logged, s_logged = store_verify(session, customer_tokens, staff_tokens)

    if c_logged:
        return redirect(url_for("customer"))

    if s_logged:
        return redirect(url_for("staff"))
        

    return render_template('login.html')

@app.route('/logout')
def logout():
    session["username"] = ""
    session["key"] = ""
    return redirect(url_for("login"))

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
    username = ""
    password = ""
    fname = ""
    lname = ""
    dob = ""
    employer = ""

    #Check all input is there
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
       
    #Parse input for security
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
    return render_template('index.html') #TODO: change to homepage


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

@app.route('/loginAuth', methods=['POST', 'GET'])
def loginAuth():
    try:
        username_or_email = request.form['username']
        password = request.form['password']
    except:
        return redirect(url_for("login"))
    
    # Parse input for security
    if not parse_input([username_or_email]):
        return redirect(url_for("login"))

    if not parse_input([password], True):
        return redirect(url_for("login"))


    is_staff = query_staff_credentials(username_or_email, password, mysql)
    is_customer = query_customer_credentials(username_or_email, password, mysql)

    if is_staff:
        session['username'] = username_or_email
        session['key'] = encrypt_password(username_or_email+password)
        staff_tokens[username_or_email] = session["key"]
        return redirect(url_for("staff"))
        
    if is_customer:     
        session['username'] = username_or_email
        session['key'] = encrypt_password(username_or_email+password)
        customer_tokens[username_or_email] = session["key"]
        return redirect(url_for("customer"))

    error = 'Log in credentials are incorrect'
    return render_template('login.html', error=error)















































@app.route("/staff")
def staff():
    _, s_logged = store_verify(session, customer_tokens, staff_tokens)
    if s_logged:
        return render_template('staff home.html') #TODO: CHANGE TO STAFF HOMEPAGE
    return redirect(url_for("login"))

@app.route("/staff_view_flights", methods=['GET', 'POST'])
def staff_view_flights():
    _, s_logged = store_verify(session, customer_tokens, staff_tokens)
    if s_logged:

        before = ""
        after = ""
        source = ""
        destination = ""
        s_city = ""
        d_city = ""
        flights = []

        try:
            before = request.form['before']
            after = request.form['after']
            source = request.form['source']
            destination = request.form['destination']
            s_city = request.form['s_city']
            d_city = request.form['d_city']

        # Allow some inputs to be missing
        except:
            pass

        # Input security
        if not parse_input([before, after, source, destination, s_city, d_city]):
            return render_template('staff_view_flights.html', flights=flights)

        airline = f'''
        SELECT employer 
        FROM airline_staff
        WHERE username = '{session['username']}';'''

        airline = exec_sql(airline, mysql)[0][0]

        flights = staff_view_flight_all(airline, before, after, source, destination, s_city, d_city, mysql)

        return render_template('staff_view_flights.html', flights=flights)

    return redirect(url_for("login"))

@app.route("/staff_view_flights_customer/<string:flight_number>/<string:airline>/<string:dept_dt>")
def staff_view_flights_customer(flight_number, airline, dept_dt):
    _, s_logged = store_verify(session, customer_tokens, staff_tokens)
    if s_logged:
        dept_dt = "".join(dept_dt.split(" ")[0].split("-"))

        customers = staff_view_flight_passengers(flight_number, airline, dept_dt, mysql)

        if len(customers) > 0:
            result = True
        else:
            result = False

        return render_template('staff_view_flights_customers.html', customers=customers, flight_number=flight_number, result=result)

    return redirect(url_for("login"))

@app.route("/staff_create_flight")
def staff_create_flight_view():
    _, s_logged = store_verify(session, customer_tokens, staff_tokens)
    if s_logged:
        airline = f'''
        SELECT employer
        FROM airline_staff
        WHERE username = '{session['username']}';
        '''

        airline = exec_sql(airline, mysql)[0][0]

        airline_choices = f'''
        SELECT id
        FROM airplane
        WHERE airline = '{airline}';
        '''

        airline_choices = exec_sql(airline_choices, mysql)

        return render_template("staff_create_flight.html", airline=airline, planes=airline_choices)

    return redirect(url_for("login"))

@app.route('/staff_create_flight_submit', methods=["POST", "GET"])
def staff_create_flight_submit():
    _, s_logged = store_verify(session, customer_tokens, staff_tokens)
    if s_logged:
        flight_num = ""
        dept_time = ""
        arr_time = ""
        source = ""
        destination = ""
        base_price = ""
        airplane_id = ""
        status = ""

        airline = f'''
        SELECT employer
        FROM airline_staff
        WHERE username = '{session['username']}';
        '''

        airline = exec_sql(airline, mysql)[0][0]

        try:
            flight_num = request.form['flight_num']
            dept_time = request.form['dept_time']
            arr_time = request.form['arr_time']
            source = request.form['source']
            destination = request.form['destination']
            base_price = request.form['base_price']
            airplane_id = request.form['airplane_id']
            status = request.form['status']
        except:
            return redirect(url_for('staff_create_flight'))

        if not parse_input([flight_num, dept_time, arr_time, source, destination, base_price, airplane_id, status]):
            return redirect(url_for('staff_create_flight'))

        staff_create_flight(flight_num, airline, airplane_id, arr_time, dept_time, base_price, source, destination, status, mysql)

        return render_template("success.html", title='Airline Staff Add Flight', \
            message=f'Flight {flight_num} ({airplane_id}) departing at {dept_time} from {source} and arriving at {arr_time} in {destination} with price {base_price} and status {status}',\
                next='/staff')

    return redirect(url_for("login"))

@app.route("/customer")
def customer():
    c_logged, _ = store_verify(session, customer_tokens, staff_tokens)
    if c_logged:
        return render_template('customer home.html') #TODO: CHANGE TO CUSTOMER HOMEPAGE
    return redirect(url_for("login"))


#
app.secret_key = 'some key that you will never guess'
# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask
# for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
