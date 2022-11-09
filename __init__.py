from flask import Flask,request,render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '***' # TODO: Change this password
app.config['MYSQL_DB'] = 'flight_app'
app.config['MYSQL_PORT'] = 8080

mysql = MySQL(app)

with app.app_context():
    curs = mysql.connection.cursor()

def exec_sql(sql: str) -> list:
    cur = mysql.connection.cursor()
    cur.execute(sql)
    return cur.fetchall()

def get_staff(USERNAME: str, PASSWORD: str) -> list:
    sql = f'''
        SELECT *
        FROM airline_staff
        WHERE username = '{USERNAME}'
            AND password = '{PASSWORD}';
        '''
    return exec_sql(sql)

def get_customer(EMAIL: str, PASSWORD: str) -> list:
    sql = f'''
        SELECT *
        FROM customer
        WHERE email = '{EMAIL}'
            AND password = '{PASSWORD}';
        '''
    return exec_sql(sql)

# Making Users in Flask
# 1. have separate log-in portals for different users
# 2. authenticate username and password
# 3. create an instance of an object --staff or customer--
#     with those credentials
# 4. call on methods in that class instance

class Airline_Staff:
  def __init__(self, username, password, fname, lname, dob, employer):
      self.username = username
      self.password = password
      self.fname = fname
      self.lname = lname
      self.dob = dob
      self.employer = employer

@app.route('/')
def hello_world():
    return render_template("login.html")

@app.route('/form_login', methods=['POST', 'GET'])
def login():
    username = request.form['username']
    password = request.form['password']

    staff_cred = get_staff(username, password)
    cust_cred = get_customer(username, password)

    if staff_cred:
        return render_template('staff_home.html', name=username)

    if cust_cred:
        return render_template('customer_home.html', name=username)

    return render_template('login.html',info='Invalid Password')

if __name__ == '__main__':
    app.run()
