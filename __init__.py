from flask import Flask, render_template, request, session, url_for, redirect
from flask_mysqldb import MySQL
import os
import sys
sys.path.insert(0, os.getcwd())
from utils.general import *
from utils.customer import *
from utils.staff import *
from utils.public_info import *
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



### STAFF LOG IN ###

@app.route("/staff")
def staff():
    _, s_logged = store_verify(session, customer_tokens, staff_tokens)
    if s_logged:
        return render_template('staff.html', is_staff = True, username=session["username"])
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
        return render_template('customer.html', is_customer=True, username=session["username"])
    return redirect(url_for("login_customer"))

@app.route('/loginAuthCust', methods=['POST', 'GET'])
def loginAuthCust():
    try:
        email = request.form['username']
        password = request.form['password']
    except:
        return redirect(url_for("login_customer"))

    # Parse input for security
    if not parse_input([email]):
        return redirect(url_for("login_customer"))


    if not parse_input([password], True):
        return redirect(url_for("login_customer"))

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
    return redirect('/')

@app.route('/homepage_redirect')
def homepage_redirect():
    c_logged, s_logged = store_verify(session, customer_tokens, staff_tokens)
    if s_logged:
        return redirect(url_for('staff'))
    if c_logged:
        return redirect(url_for('customer'))
    return redirect('/')

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

    if not check_date_format(dob):
        error = 'Date of Birth must be formate YYYY-MM-DD'
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
    return redirect('/')



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

    if not check_date_format(dob):
        error = 'Date of Birth must be formate YYYY-MM-DD'
        return render_template('register customer.html', error=error)

    # check if email exists
    if query_customer_email(email, mysql):
        error = f'Account with email {email} already exists'
        return render_template('register customer.html', error=error)

    # create account
    create_customer_account(email,name,password,building_num,city,state,
                            street,pp_country,pp_num,pp_expr,dob,phone_num, mysql)

    # render homepage
    return redirect('/')



### PUBLIC FLIGHT INFO ###
@app.route('/public_info')
def public_info():
    #headings,data=public_view_oneway_flights(mysql)
    return render_template('public_info.html')

@app.route("/public_view_flights", methods=['GET', 'POST'])
def public_view_flight():
    c_org = None
    c_dest = None
    a_org = None
    a_dest = None
    dept_dt = None
    return_dt = None
    f_type = None
    headings = []
    data = []

    try:
        f_type = request.form['flight_type']
        c_org = request.form['city_origin']
        c_dest = request.form['city_dest']
        a_org = request.form['airport_origin']
        a_dest = request.form['airport_dest']
        dept_dt = request.form['dept_dt']
        return_dt = request.form['return_dt']
    except:
        pass

    if not parse_input([c_org,c_dest,a_org,a_dest,dept_dt,return_dt,f_type]):
        return render_template('public_info.html', headings=headings, data=data)

    if not check_datetime_format(dept_dt) and check_datetime_format(return_dt):
        error = 'Datetime must be formate YYYY-MM-DD HH:MM:SS'
        return render_template('public_info.html', error=error)

    if f_type=='two way':
        headings, data = public_view_twoway_flights(mysql,CITY_ORIGIN=c_org,CITY_DEST=c_dest,AP_ORIGIN=a_org,
                                                    AP_DEST=a_dest,START_DATE=dept_dt,END_DATE=return_dt)
        return render_template('public_info.html', headings=headings, data=data)
    elif f_type=='one way':
        headings, data = public_view_oneway_flights(mysql,CITY_ORIGIN=c_org,CITY_DEST=c_dest,AP_ORIGIN=a_org,
                                                    AP_DEST=a_dest,START_DATE=dept_dt,END_DATE=return_dt)
        return render_template('public_info.html', headings=headings, data=data)
    else:
        error="Flight Type must be 'one way' or 'two way'"
        render_template('public_info.html', error=error)

@app.route('/public_status')
def public_status():
    return render_template('public_status.html')

@app.route("/public_check_status", methods=['GET', 'POST'])
def public_check_status():
    fnum = None
    airline = None
    dept_dt = None

    try:
        fnum=request.form['flight_num']
        airline=request.form['airline']
        dept_dt=request.form['dept_dt']
    except:
        error='Bad inputs'
        return render_template('public_status.html', error=error)

    if not parse_input([fnum,airline,dept_dt]):
        error = 'Bad inputs'
        return render_template('public_status.html', error=error)

    if not check_datetime_format(dept_dt):
        error = 'Datetime must be formate YYYY-MM-DD HH:MM:SS'
        return render_template('public_status.html', error=error)

    headings, data = public_view_flight_status(mysql, fnum, airline, dept_dt)
    return render_template('public_status.html', headings=headings, data=data)



### STAFF USE CASES ###
@app.route("/staff_view_flights", methods=['GET', 'POST'])
def staff_view_flights():
    _, s_logged = store_verify(session, customer_tokens, staff_tokens)
    if s_logged:

        # Before and after are none because they will be set to the wrong value in the sql function otherwise
        before = None
        after = None
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

        if not check_datetime_format(before) and check_datetime_format(after):
            error = 'Datetime must be formate YYYY-MM-DD HH:MM:SS'
            return render_template('staff_view_flights.html', error=error)

        airline = session['employer']
        headings, flights = staff_view_flight_all(airline, before, after, source, destination, s_city, d_city, mysql)

        return render_template('staff_view_flights.html', flights=flights, headings=headings)

    return redirect('/')


@app.route("/staff_view_flights_customer/<string:flight_number>/<string:airline>/<string:dept_dt>")
def staff_view_flights_customer(flight_number, airline, dept_dt):
    _, s_logged = store_verify(session, customer_tokens, staff_tokens)
    if s_logged:
       # dept_dt = "".join(dept_dt.split(" ")[0].split("-"))

        headings, data = staff_view_flight_passengers(flight_number, airline, dept_dt, mysql)

        if len(data) > 0:
            result = True
        else:
            result = False

        return render_template('staff_view_flights_customers.html', headings=headings, customers=data, flight_number=flight_number, result=result)

    return redirect(url_for("staff_login"))

@app.route("/staff_create_flight")
def staff_create_flight_view():
    _, s_logged = store_verify(session, customer_tokens, staff_tokens)
    if s_logged:

        airline = session['employer']
        planes = planes_of_airline(airline,mysql)

        return render_template("staff_create_flight.html", airline=airline, planes=planes)

    return redirect(url_for("login_staff"))

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

        airline = session['employer']

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
            return redirect(url_for('staff_create_flight_view'))

        if not parse_input([flight_num, dept_time, arr_time, source, destination, base_price, airplane_id, status]):
            return redirect(url_for('staff_create_flight_view'))

        if not check_datetime_format(dept_time) and check_datetime_format(arr_time):
            return redirect(url_for('staff_create_flight_view'))

        if not check_datetime_format(dept_time) and check_datetime_format(arr_time):
            return redirect(url_for('staff_create_flight_view'))

        staff_create_flight(flight_num, airline, airplane_id, arr_time, dept_time, base_price, source, destination, status, mysql)

        return render_template("success.html", title='Airline Staff Add Flight', \
            message=f'Flight {flight_num} ({airplane_id}) departing at {dept_time} from {source} and arriving at {arr_time} in {destination} with price {base_price} and status {status}',\
                next='/staff')

    return redirect(url_for("login_staff"))

@app.route('/staff_change_flight_status')
def staff_change_flights():
    _, s_logged = store_verify(session, customer_tokens, staff_tokens)

    if s_logged:
        return render_template("staff_change_flight_status.html")

    return redirect(url_for("login_staff"))

@app.route('/staff_change_flight_status_submit', methods=['GET', 'POST'])
def staff_change_flights_submit():
    _, s_logged = store_verify(session, customer_tokens, staff_tokens)
    if s_logged:
        flight_num = ""
        dept_time = None
        status = ""

        airline = session["employer"]

        try:
            flight_num = request.form['flight_num']
            dept_time = request.form['dept_time']
            status = request.form['status']

        except:
            return redirect(url_for("staff_change_flights"))

        if not parse_input([flight_num, dept_time, status]):
            return redirect(url_for("staff_change_flights"))

        if not check_datetime_format(dept_time):
            return redirect(url_for("staff_change_flights"))

        staff_update_flight_status(flight_num, airline, dept_time, status, mysql)

        return render_template("success.html", title='Airline Staff Change Flight', \
            message=f'Flight {flight_num} changed', next='/staff')

    return redirect(url_for("login_staff"))

@app.route('/staff_add_new_airplane')
def staff_add_new_airplane():
    _, s_logged = store_verify(session, customer_tokens, staff_tokens)
    if s_logged:
        return render_template("staff_add_new_airplane.html")

    return redirect(url_for("login_staff"))

@app.route('/staff_add_new_airplane_submit', methods=['GET', 'POST'])
def staff_add_new_airplane_submit():
    _, s_logged = store_verify(session, customer_tokens, staff_tokens)
    if s_logged:
        airplane_id = ""
        num_seats = ""
        age = None
        manufacturer = ""
        airline = session['employer']

        try:
            airplane_id = request.form['airplane_id']
            num_seats = request.form['num_seats']
            age = request.form['age']
            manufacturer = request.form['manufacturer']
        except:
            return redirect(url_for("staff_add_new_airplane"))

        if not parse_input([airplane_id, num_seats, age]):
            return redirect(url_for("staff_add_new_airplane"))

        if not check_date_format(age):
            redirect(url_for("staff_add_new_airplane"))

        staff_create_airplane(airplane_id, airline, num_seats, age, manufacturer, mysql)

        return render_template('success.html', title="Airline Staff Add Airplane", \
            message=f" Plane with ID: {airplane_id} has been added to {airline}",\
                next='/staff')

    return redirect(url_for("login_staff"))

@app.route('/staff_add_new_airport')
def staff_add_new_airport():
    _, s_logged = store_verify(session, customer_tokens, staff_tokens)
    if s_logged:
        return render_template("staff_add_new_airport.html")

    return redirect(url_for("login_staff"))

@app.route('/staff_add_new_airport_submit', methods=['GET', 'POST'])
def staff_add_new_airport_submit():
    _, s_logged = store_verify(session, customer_tokens, staff_tokens)
    if s_logged:
        name = ""
        city = ""
        country = ""
        airport_type = ""

        try:
            name = request.form['name']
            city = request.form['city']
            country = request.form['country']
            airport_type = request.form['airport_type']
        except:
            return redirect(url_for("staff_add_new_airport"))
        
        if not parse_input([name, city, country, airport_type]):
            return  redirect(url_for("staff_add_new_airport"))
        
        staff_create_airport(name, city, country, airport_type, mysql)

        return render_template('success.html', title="Airline Staff Add Airplane",\
            message=f"{airport_type} Airport {name} in {city}, {country} Added",\
            next="/staff")


    return redirect(url_for("login_staff"))

### CUSTOMER USE CASES ###
@app.route('/customer_view_flight', methods=["POST", "GET"])
def customer_view_flight():
    c_logged, _ = store_verify(session, customer_tokens, staff_tokens)
    if c_logged:
        s_date = None
        e_date = None
        a_org = None
        a_dest = None
        c_org = None
        c_dest = None
        flights = []

        try:
            s_date = request.form['after']
            e_date = request.form['before']
            a_org = request.form['source']
            a_dest = request.form['destination']
            c_org = request.form['s_city']
            c_dest = request.form['d_city']
        except:
            pass

        if not parse_input([s_date,e_date,a_org,a_dest,c_org,c_dest]):
            return render_template('customer_view_flights.html')

        if not check_datetime_format(s_date) and check_datetime_format(e_date):
            error = 'Datetime must be formate YYYY-MM-DD HH:MM:SS'
            return render_template('customer_view_flights.html', error=error)

        email = session['username']
        headings, data = customer_view_my_flights(email, mysql, START_DATE=s_date, END_DATE=e_date,
                                               AP_ORIGIN=a_org, AP_DEST=a_dest, CITY_ORIGIN=c_org, CITY_DEST=c_dest)
        return render_template('customer_view_flights.html', headings=headings, data=data)
    else:
        return redirect('/')

@app.route('/customer_search_flight')
def customer_search_flight():
    return redirect(url_for("public_info"))

@app.route('/customer_init_purchase', methods=["POST", "GET"])
def customer_init_purchase():
    c_logged, _ = store_verify(session, customer_tokens, staff_tokens)
    if c_logged:

        headings, data = public_view_oneway_flights(mysql)
        return render_template('customer_purchase_flight.html', headings=headings, data=data)

    return redirect(url_for('/login_customer'))


# DOES NOT HANDLE two-way flights
@app.route('/customer_purchase_search_flights', methods=["POST", "GET"])
def customer_purchase_search_flights():
    c_logged, _ = store_verify(session, customer_tokens, staff_tokens)
    if c_logged:
        c_org = None
        c_dest = None
        a_org = None
        a_dest = None
        dept_dt = None
        return_dt = None
        headings = []
        data = []

        try:
            c_org = request.form['city_origin']
            c_dest = request.form['city_dest']
            a_org = request.form['airport_origin']
            a_dest = request.form['airport_dest']
            dept_dt = request.form['dept_dt']
            return_dt = request.form['return_dt']
        except:
            pass

        if not parse_input([c_org, c_dest, a_org, a_dest, dept_dt, return_dt]):
            return render_template('customer_purchase_flight.html', headings=headings, data=data)

        if not check_datetime_format(dept_dt) and check_datetime_format(return_dt):
            error = 'Datetime must be formate YYYY-MM-DD HH:MM:SS'
            return render_template('customer_purchase_flight.html', headings=headings, data=data, error=error)

        headings, data = public_view_oneway_flights(mysql, CITY_ORIGIN=c_org, CITY_DEST=c_dest, AP_ORIGIN=a_org,
                                                    AP_DEST=a_dest, START_DATE=dept_dt, END_DATE=return_dt)
        return render_template('customer_purchase_flight.html', headings=headings, data=data)

    return redirect(url_for("login_customer"))

@app.route('/customer_stage_purchase/<string:flight_number>/<string:airline>/<string:dept_dt>/<string:base_price>',
           methods=["POST", "GET"])
def customer_stage_purchase(flight_number, airline, dept_dt, base_price):
    c_logged, _ = store_verify(session, customer_tokens, staff_tokens)
    if c_logged:
        #clean_dt = dept_dt[0:4] + dept_dt[5:7] + dept_dt[8:10]

        sp=get_sold_price(flight_number,airline,dept_dt,base_price,mysql)
        if sp==None:
            error='Failed to purchase ticket. Flight capacity full.'
            return render_template('customer_stage_purchase.html', error=error)
        heading=('Final Price')
        data=(str(sp))
        flight_data = [flight_number,airline,dept_dt,base_price,sp]
        return render_template('customer_stage_purchase.html', flight_data=flight_data, header=heading, data=data)

    return redirect(url_for("login_staff"))

@app.route('/customer_confirm_purchase/<string:flight_number>/<string:airline>/<string:dept_dt>/<string:base_price>',
           methods=["POST", "GET"])
def customer_confirm_purchase(flight_number, airline, dept_dt, base_price):
    c_logged, _ = store_verify(session, customer_tokens, staff_tokens)
    if c_logged:

        cc_num = None
        cc_expr = None
        cc_name = None
        cc_type = None
        sold_price = None
        flight_data=[]
        try:
            cc_num = request.form['cc_num']
            cc_expr = request.form['cc_expr']
            cc_name = request.form['cc_name']
            cc_type = request.form['cc_type']
        except:
            error = 'Bad Inputs'
            return render_template('customer_stage_purchase.html', error=error)

        if not parse_input( [cc_num,cc_expr,cc_name,cc_type] ):
            error = 'Bad inputs'
            return render_template('customer_stage_purchase.html', error=error)

        if cc_type not in ['credit', 'debit']:
            error = "Bad inputs. Card type must be 'credit' or 'debit'"
            render_template('customer_stage_purchase.html', error=error)

        email = session['username']

        sold_price = get_sold_price(flight_number, airline, dept_dt, base_price, mysql)
        customer_purchase_ticket(flight_number, airline, dept_dt, sold_price, base_price, cc_num, cc_expr, cc_name,
                                 cc_type, email, mysql)
        flight_data = [flight_number, airline, dept_dt, base_price, sold_price]
        return render_template('customer_stage_purchase.html', confirmation=' Purchase Created', flight_data=flight_data)

    return redirect(url_for("login_staff"))

@app.route('/customer_init_delete', methods=["POST", "GET"])
def customer_init_delete():
    c_logged, _ = store_verify(session, customer_tokens, staff_tokens)
    if c_logged:

        email = session['username']
        headings, data = customer_view_my_flights(email, mysql)
        return render_template('customer_delete_flight.html', headings=headings, data=data)

    return redirect(url_for('/login_customer'))

@app.route('/customer_delete_search_flights', methods=["POST", "GET"])
def customer_delete_search_flights():
    c_logged, _ = store_verify(session, customer_tokens, staff_tokens)
    if c_logged:
        c_org = None
        c_dest = None
        a_org = None
        a_dest = None
        dept_dt = None
        return_dt = None
        headings = []
        data = []

        try:
            c_org = request.form['city_origin']
            c_dest = request.form['city_dest']
            a_org = request.form['airport_origin']
            a_dest = request.form['airport_dest']
            dept_dt = request.form['dept_dt']
            return_dt = request.form['return_dt']
        except:
            pass

        if not parse_input([c_org, c_dest, a_org, a_dest, dept_dt, return_dt]):
            return render_template('customer_purchase_flight.html', headings=headings, data=data)

        if not check_datetime_format(dept_dt) and check_datetime_format(return_dt):
            error = 'Datetime must be formate YYYY-MM-DD HH:MM:SS'
            return render_template('customer_purchase_flight.html', headings=headings, data=data, error=error)

        email = session['username']
        headings, data = customer_view_my_flights(email, mysql, START_DATE=dept_dt, END_DATE=return_dt,
                                                  AP_ORIGIN=a_org, AP_DEST=a_dest, CITY_ORIGIN=c_org, CITY_DEST=c_dest)
        return render_template('customer_delete_flight.html', headings=headings, data=data)

    return redirect(url_for("/login_customer"))

@app.route('/customer_confirm_delete/<string:ticket_id>',  methods=["POST", "GET"])
def customer_confirm_delete(ticket_id):
    c_logged, _ = store_verify(session, customer_tokens, staff_tokens)
    if c_logged:

        email = session['username']
        customer_cancel_ticket(email, ticket_id, mysql)
        return redirect(url_for("customer_init_delete"))

    return redirect(url_for("login_customer"))

@app.route('/customer_spending',  methods=["POST", "GET"])
def customer_spending():
    c_logged, _ = store_verify(session, customer_tokens, staff_tokens)
    if c_logged:
        email = session['username']
        headings, data = customer_view_spending_pastyear(email, mysql)
        return render_template('customer_spending.html', headings=headings, data=data)

    return redirect(url_for('/login_customer'))
@app.route('/customer_spending_search',  methods=["POST", "GET"])
def customer_spending_search():
    c_logged, _ = store_verify(session, customer_tokens, staff_tokens)
    if c_logged:
        s_date = datetime_in_X_days(-365)
        e_date = datetime_in_X_days(0)

        try:
            s_date = request.form['before']
            e_date = request.form['after']
        except:
            pass

        if not parse_input( [s_date, e_date] ):
            error = 'Bad Inputs'
            return render_template('customer_spending.html', error=error)

        if not check_datetime_format(s_date) and check_datetime_format(e_date):
            error = 'Datetime must be formate YYYY-MM-DD HH:MM:SS'
            return render_template('customer_spending.html', error=error)

        email = session['username']
        headings, data = customer_view_spending_interval(email, s_date, e_date, mysql)
        return render_template('customer_spending.html', headings=headings, data=data)

    return redirect(url_for('/login_customer'))

@app.route('/customer_spending_6months',  methods=["POST", "GET"])
def customer_spending_6months():
    c_logged, _ = store_verify(session, customer_tokens, staff_tokens)
    if c_logged:

        email = session['username']
        headings, data = customer_view_spending_past6months(email, mysql)
        return render_template('customer_spending.html', headings=headings, data=data)

    return redirect(url_for('/login_customer'))

@app.route('/customer_spending_year', methods=["POST", "GET"])
def customer_spending_year():
    c_logged, _ = store_verify(session, customer_tokens, staff_tokens)
    if c_logged:
        email = session['username']
        headings, data = customer_view_spending_pastyear(email, mysql)
        return render_template('customer_spending.html', headings=headings, data=data)

    return redirect(url_for('/login_customer'))

@app.route('/customer_rate_and_comment', methods=["POST", "GET"])
def customer_rate_and_comment():
    c_logged, _ = store_verify(session, customer_tokens, staff_tokens)
    if c_logged:

        email = session['username']
        r_headings, r_data = customer_view_review(email, mysql)

        today = datetime_in_X_days(0)
        f_headings, f_data = customer_view_my_flights(email, mysql, END_DATE=today)

        return render_template('customer_rate_and_comment.html',
                                r_headings=r_headings, r_data=r_data,
                                f_headings=f_headings, f_data=f_data)

    return redirect(url_for('/login_customer'))

@app.route('/customer_stage_rate_and_comment/<string:ticket_id>', methods=["POST", "GET"])
def customer_stage_rate_and_comment(ticket_id):
    c_logged, _ = store_verify(session, customer_tokens, staff_tokens)
    if c_logged:
        return render_template('customer_stage_rate_and_comment.html', ticket_id=ticket_id)
    return redirect(url_for("login_customer"))


@app.route('/customer_create_rate_and_comment/<string:ticket_id>', methods=["POST", "GET"])
def customer_create_rate_and_comment(ticket_id):
    c_logged, _ = store_verify(session, customer_tokens, staff_tokens)
    if c_logged:
        rating = None
        comment = None

        try:
            rating = request.form['rating']
            comment = request.form['comment']
        except:
            error = 'Bad Inputs'
            return render_template('customer_stage_rate_and_comment.html', error=error)

        if rating not in ['1','2','3','4','5']:
            error = 'Rating must be 1-5'
            return render_template('customer_stage_rate_and_comment.html', error=error)

        if len(comment) > 400:
            error = 'Comment cannot be more than 400 char'
            return render_template('customer_stage_rate_and_comment.html', error=error)

        email = session['username']
        customer_create_review(email, ticket_id, rating, comment, mysql)

        return redirect(url_for('customer_rate_and_comment'))

    return redirect(url_for('/login_customer'))





app.secret_key = 'some key that you will never guess'
# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask
# for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)


