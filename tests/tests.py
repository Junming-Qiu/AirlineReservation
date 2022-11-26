from flask import Flask, render_template, request, session, url_for, redirect
from flask_mysqldb import MySQL
import random
import string
import datetime

# Initialize the app from Flask
app = Flask(__name__)


app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'walrus123' # TODO: Change this password
app.config['MYSQL_DB'] = 'flight_app'
app.config['MYSQL_PORT'] = 8080

mysql = MySQL(app)

with app.app_context():
    curs = mysql.connection.cursor()

    # TODO: Wrap SQL statement with Atomic Transaction
    def sql_transaction_wrap(sql: str) -> str:

        return f'''
        USE flight_app;
        {sql}
        '''

    def clean_rtn(rtn: tuple) -> tuple:
        cleaned=[]
        for t in rtn:
            cleaned.append(tuple([t[i] for i in range(len(rtn)-1)]))
        return tuple(cleaned)

    def exec_sql(sql: str) -> list:
        cur = mysql.connection.cursor()
        cur.execute(sql)
        return cur.fetchall()


def public_view_oneway_flights(mysql,
                               START_DATE=None, END_DATE=None,
                               AP_ORIGIN=None, AP_DEST=None,
                               CITY_ORIGIN=None, CITY_DEST=None) -> tuple:
    sql = f'''
    SELECT f.flight_num, f.airline, f.dept_datetime, f.flight_status
    FROM flight as f'''

    if START_DATE:  # NOT NULL
        sql += f'''
        AND f.dept_datetime>={START_DATE})'''  # TODO, should this be =?

    if END_DATE:
        sql += f'''
        AND f.dept_datetime<={END_DATE} '''

    if AP_ORIGIN:
        sql += f'''
        AND f.origin='{AP_ORIGIN}' '''

    if AP_DEST:
        sql += f'''
        AND f.destination='{AP_DEST}' '''

    if CITY_ORIGIN:
        sql += f'''
        AND ap_origin.name='{CITY_ORIGIN}' '''

    if CITY_DEST:
        sql += f'''
        AND ap_dest.name='{CITY_DEST}' '''

    sql += ';'
    headings=('Flight Number', 'Airline', 'Departure Datetime', 'Status')
    data=exec_sql(sql)
    return (headings,data)

def puiblic_view_twoway_flights(START_DATE=None, END_DATE=None,
                                        AP_ORIGIN=None, AP_DEST=None,
                                        CITY_ORIGIN=None, CITY_DEST=None) ->  tuple:
    sql = '''
        SELECT DISTINCT f1.origin, f1.destination,
        f1.flight_num, f1.airline, f1.dept_datetime,
        f2.flight_num, f2.airline, f2.dept_datetime,
        f1.base_price+f2.base_price as combined_base_price
        FROM flight as f1, flight as f2,
        airport as ap_origin, airport as ap_dest
        WHERE f1.origin=ap_origin.name
            AND f1.destination=ap_dest.name
            AND f1.destination=f2.origin
            AND f1.origin=f2.destination
            AND f1.arrv_datetime>f2.dept_datetime'''
    if START_DATE:  # NOT NULL
        sql += f'''
        AND f1.dept_datetime>={START_DATE}'''
    else:
        today = date_in_X_days(0)
        sql+=f'''
        AND f1.dept_datetime>={today}'''

    if END_DATE:
        sql += f'''
        AND f2.dept_datetime<={END_DATE} '''

    if AP_ORIGIN:
        sql += f'''
        AND f1.origin='{AP_ORIGIN}' '''

    if AP_DEST:
        sql += f'''
        AND f1.destination='{AP_DEST}' '''

    if CITY_ORIGIN:
        sql += f'''
        AND ap_origin.name='{CITY_ORIGIN}' '''

    if CITY_DEST:
        sql += f'''
        AND ap_dest.name='{CITY_DEST}' '''

    sql+=';'
    return sql



sql='''SELECT * FROM airline;'''

@app.route('/')
def hello():
    headings,data=public_view_oneway_flights(sql)

    return render_template("table_template.html", headings=headings, data=data)


if __name__ == "__main__":
    app.run('127.0.0.1', port=5000, debug=True)