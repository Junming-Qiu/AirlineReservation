from functions import *

# ****************
# CUSTOMER USE CASES
# ****************

# 1.1 show future, purchased flights
# TODO refactor with Airline Staff functions
def customer_view_flight_purchased(EMAIL: str, mysql) ->  list[tuple]:
    today = date_in_X_days(0)
    sql = f'''
    SELECT *
    FROM ticket as t JOIN flight as f ON
        t.flight_num = f.flight_num
        t.airline = f.airline
        t.dept_datetime = f.dept_datetime
    WHERE t.id IN (SELECT p.ticket_id
                    FROM purchase as p
                    WHERE p.customer_email='{EMAIL}'
                        AND p.purchase_datetime>={today});
    '''
    rtn = exec_sql(sql, mysql)
    return rtn

# 1.2 view flights within a range of dates
def customer_view_flight_range(START: str, END: str, mysql) -> list[tuple]:
    sql = f'''
    SELECT *
    FROM flight
    WHERE dept_datetime BETWEEN {START} AND {END};
    '''
    rtn = exec_sql(sql, mysql)
    return rtn

# 1.3 view flights based on airport origin
def customer_view_flight_airport_origin(ORIGIN: str, mysql) -> list[tuple]:
    sql = f'''
    SELECT *
    FROM flight
    WHERE origin = '{ORIGIN}';
    '''
    rtn = exec_sql(sql, mysql)
    return rtn
# 1.4 view flights based on airport destination
def customer_view_flight_airport_dest(DESTINATION: str, mysql) -> list[tuple]:
    sql = f'''
    SELECT *
    FROM flight
    WHERE origin = '{DESTINATION}';
    '''
    rtn = exec_sql(sql, mysql)
    return rtn

# 1.5 view flights based on city origin
def customer_view_flight_city_origin(CITY: str, mysql) -> list[tuple]:
    sql = f''' 
    SELECT f.flight_num, f.airline, f.airplane_id,
        f.arrv_datetime, f.dept_datetime, f.base_price,
        f.origin, f.destination, f.flight_status
    FROM flight as f JOIN airport as a ON f.origin=a.name
    WHERE a.city = '{CITY}';    
    '''
    rtn = exec_sql(sql, mysql)
    return rtn
# 1.6 view flights based on city destination
def customer_view_flight_city_dest(CITY: str, mysql) -> list[tuple]:
    sql = f''' 
    SELECT f.flight_num, f.airline, f.airplane_id,
        f.arrv_datetime, f.dept_datetime, f.base_price,
        f.origin, f.destination, f.flight_status
    FROM flight as f JOIN airport as a ON f.destination=a.name
    WHERE a.city = '{CITY}';    
    '''
    rtn = exec_sql(sql, mysql)
    return rtn

# 2.1 view one-way flights based on city origin

# 2.2 view one-way flights based on city destination

# 2.3 view one-way flights based on airport origin

# 2.4 view one-way flights based on airport destination
def customer_view_flight_oneway(CITY: str, CITY: str,
                                )



# 2.5 view one-way flights based on date (dept)

# 2.6 view two-way flights based on city origin and destination

# 2.7 view two-way flights based on airport origin and destination

# 2.8 view two-way flights based on dates (dept and/or return)

# 3.1 purchase ticket

# 4.1 cancel trip (that's 24+ hours out), remove ticket and purchase

# 5.1 rate and comment on flight

# 6.1 ...