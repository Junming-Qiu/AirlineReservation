from utils.general import *

'''
These functions provide public flight info.

They should be called by some function that:
    1. reads user input
    2. calls this functions
    3. returns render_template( 'table_template',
                                 headings=rtn[0],
                                 data=rtn[1] ) 

Inputs:
    mysql       : MySQL connection
    START_DATE  : Optional(str)
    END_DATE    : Optional(str)
    AP_ORIGIN   : Optional(str)
    AP_DEST     : Optional(str)
    CITY_ORIGIN : Optional(str)
    CITY_DEST   : Optional(str)
    
Output:
    (table_headings, table_data) : tuple

This covers:
 1. Customer use case 2
 2. Homepage when not logged in

'''


def public_view_twoway_flights(mysql, START_DATE=None, END_DATE=None,
                                      AP_ORIGIN=None, AP_DEST=None,
                                      CITY_ORIGIN=None, CITY_DEST=None) ->  tuple:
    sql = '''
        SELECT DISTINCT ap_origin.city, ap_dest.city,
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
        AND f1.dept_datetime>={START_DATE}'''                                                                              # TODO: should this be range or exact date?
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
        AND ap_origin.city='{CITY_ORIGIN}' '''

    if CITY_DEST:
        sql += f'''
        AND ap_dest.city='{CITY_DEST}' '''

    sql+=';'
    data=exec_sql(sql,mysql)
    headings=('Origin',
              'Destination',
              'Flight Number 1',
              'Airline 1',
              'Departure 1',
              'Flight Number 2',
              'Airline 2',
              'Departure 2',
              'Price')
    return (headings,data)

# search for one-way flights
def public_view_oneway_flights(mysql, START_DATE=None, END_DATE=None,
                                      AP_ORIGIN=None, AP_DEST=None,
                                      CITY_ORIGIN=None, CITY_DEST=None) ->  tuple:
    sql = '''
    SELECT DISTINCT ap_origin.city, ap_dest.city,
    f.flight_num, f.airline, f.dept_datetime, f.base_price
    FROM flight as f, airport as ap_origin, airport as ap_dest
    WHERE f.origin=ap_origin.name
        AND f.destination=ap_dest.name'''

    if START_DATE: # NOT NULL
        sql+=f'''
        AND f.dept_datetime>={START_DATE}'''                                                                              # TODO: should this be range or exact date?
    else:
        today = date_in_X_days(0)
        sql+=f'''
        AND f.dept_datetime>={today}'''

    if END_DATE:
        sql+=f'''
        AND f.dept_datetime<={END_DATE} '''

    if AP_ORIGIN:
        sql+=f'''
        AND f.origin='{AP_ORIGIN}' '''

    if AP_DEST:
        sql+=f'''
        AND f.destination='{AP_DEST}' '''

    if CITY_ORIGIN:
        sql+=f'''
        AND ap_origin.name='{CITY_ORIGIN}' '''

    if CITY_DEST:
        sql+=f'''
        AND ap_dest.name='{CITY_DEST}' '''

    sql+=';'
    data=exec_sql(sql,mysql)
    headings=('Origin',
              'Destination',
              'Flight Number',
              'Airline',
              'Departure',
              'Price')
    return (headings,data)
