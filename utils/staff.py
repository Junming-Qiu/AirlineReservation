from utils.general import *

'''

NOTE : these functions do not ensure that the
    AIRLINE parameter matches the staff's employer.
    
    This should be implemented elsewhere.    


'''

# USE CASE 1: view flights
def staff_view_flight_all(AIRLINE: str, before, after, source, destination, s_city, d_city, mysql) -> tuple:
    # Must be checking for none, otherwise an empty form will set default to 30 days after today
    if before == None:
        before = datetime_in_X_days(0)

    if after == None:
        after = datetime_in_X_days(30)

    sql = f'''
        SELECT f.flight_num, f.airline, f.airplane_id,
        f.arrv_datetime, f.dept_datetime, f.base_price,
        f.origin, f.destination, f.flight_status
        FROM flight as f JOIN airport as a ON f.origin=a.name JOIN airport as b ON f.destination=b.name
        WHERE f.airline = '{AIRLINE}'
    '''

    if before and after:
        sql += f" AND f.dept_datetime BETWEEN '{before}' AND '{after}'"

    if source:
        sql += f" AND f.origin = '{source}'"

    if destination:
        sql += f" AND f.destination = '{destination}'"

    if s_city:
        sql += f" AND a.city = '{s_city}'"

    if d_city:
        sql += f" AND b.city = '{d_city}'"

    sql += ";"

    data = exec_sql(sql, mysql)
    headings =(
        'Flight Number',
        'Airline',
        'Airplane ID',
        'Arrival',
        'Departure',
        'Base Price',
        'Arrival',
        'Destination',
        'Status',
    )
    return (headings ,data)

def staff_view_flight_passengers(FNUM: str, AIRLINE: str, DEPT_DT: str, mysql) -> tuple:
    sql = f'''
    SELECT c.name, c.email, c.phone_number
    FROM customer as c, purchase as p, ticket as t
    WHERE c.email = p.customer_email
        AND p.ticket_id = t.id
        AND t.flight_num = '{FNUM}'
        AND t.airline = '{AIRLINE}'
        AND t.dept_datetime = '{DEPT_DT}';
    '''

    data = exec_sql(sql, mysql)
    headings=(
        'Name',
        'Email',
        'Phone Number'
    )
    return (headings,data)



# USE CASE 2: create flight
def staff_create_flight(FNUM: str, AIRLINE: str, AIRPLANE_ID: str,
                            ARRV_DT: str, DEPT_DT: str, BASE_PRICE: str,
                            ORGN: str, DEST: str, FSTAUS: str, mysql) -> None:
    sql=f'''
    INSERT INTO flight
    VALUES('{FNUM}', '{AIRLINE}', '{AIRPLANE_ID}', '{ARRV_DT}',
           '{DEPT_DT}', {BASE_PRICE}, '{ORGN}', '{DEST}', '{FSTAUS}');
    '''
    exec_sql(sql, mysql, commit=True)



# USE CASE 3: update flight status
def staff_update_flight_status(FNUM: str, AIRLINE: str,
                                 DEPT_DT: str, STATUS: str, mysql) -> None:
    sql =f'''
        UPDATE flight 
        SET flight_status='{STATUS}' 
        WHERE flight_num='{FNUM}'
            AND airline='{AIRLINE}'
            AND dept_datetime='{DEPT_DT}';
    '''
    exec_sql(sql, mysql, commit=True)



# USE CASE 4: add an airplane
def staff_create_airplane(ID: str, AIRLINE: str, NUM_SEATS: str,
                          AGE: str, MANUFACTURER: str, mysql) -> tuple:
    insert_sql = f'''
    INSERT INTO airplane
    VALUES ('{ID}', '{AIRLINE}', {NUM_SEATS}, '{AGE}','{MANUFACTURER}');
    '''
    exec_sql(insert_sql, mysql, commit=True)

    view_sql = f'''
    SELECT *
    FROM airplane
    WHERE airline='{AIRLINE}';
    '''
    data = exec_sql(view_sql, mysql)
    headings=(
        'ID',
        'Airline',
        'Num Seats',
        'Age',
        'Manufacturer',
    )
    return (headings,data)



# USE CASE 5: add new airport
def staff_create_airport(NAME: str, CITY: str, COUNTRY: str, TYPE: str, mysql) -> None:
    sql = f'''
    INSERT INTO airport
    VALUES ('{NAME}', '{CITY}', '{COUNTRY}', '{TYPE}');
    '''
    exec_sql(sql, mysql, commit=True)



# USE CASE 6: view  flight rating and comments
# Defaults to showing all flights before today for this airline
def staff_view_avg_rating(FLIGHT_NUM: str, AIRLINE: str, DEPT_DATETIME: str, mysql) -> tuple:

    sql = f'''
    SELECT t.flight_num, t.dept_datetime ,avg(f.rating)
    FROM flight_review as f join ticket as t on f.ticket_id = t.id
    GROUP BY t.flight_num, t.airline, t.dept_datetime
    HAVING t.airline = '{AIRLINE}'
    '''

    if FLIGHT_NUM:
        sql += f" AND t.flight_num = '{FLIGHT_NUM}'"

    if not FLIGHT_NUM and not DEPT_DATETIME:
        DEPT_DATETIME = datetime_in_X_days(0)
        sql += f" AND t.dept_datetime < '{DEPT_DATETIME}'"
    elif DEPT_DATETIME:
        sql += f" AND t.dept_datetime = '{DEPT_DATETIME}'"
    
    sql += ";"

    data = exec_sql(sql, mysql)
    headings=(
        'Flight Number',
        'Departure Date',
        'Avg Rating'
    )
    return (headings,data)

def staff_view_ratings_and_comments(FLIGHT_NUM: str, AIRLINE: str, DEPT_DATETIME: str, mysql) -> tuple:
    sql = f'''
    SELECT rating, comment
    FROM flight_review JOIN ticket ON flight_review.ticket_id = ticket.id
    WHERE flight_num = '{FLIGHT_NUM}'
        AND airline = '{AIRLINE}'
        AND dept_datetime = '{DEPT_DATETIME}';
    '''
    data = exec_sql(sql, mysql)
    headings=(
        'Rating',
        'Comment'
    )
    return (headings,data)



# USE CASE 7: view most-frequent-customer (mfc) and customer history
#Only needs past year, according to requirements
def staff_view_mfc_range(START: str, END: str, mysql) -> tuple:
    sql = f'''
    SELECT tmp.num as 'num_purchases', c.name, c.email, c.phone_number
    FROM
        (SELECT customer_email, count(*) as num
        FROM purchase
        WHERE purchase_datetime BETWEEN '{START}' AND '{END}'
        GROUP BY customer_email) as tmp
        JOIN customer as c
        ON tmp.customer_email = c.email
    ORDER BY num Desc
    LIMIT 1;
    '''

    data = exec_sql(sql, mysql)
    headings=(
        'Num Purchases',
        'Name',
        'Email',
        'Phone Num'
    )
    return (headings,data)

def staff_view_mfc_pastmonth1(mysql) -> tuple:
    today = datetime.datetime.today()
    past_month = today.replace(month=(today.month-1))
    return staff_view_mfc_range(str(past_month)[0:-7], str(today)[0:-7], mysql)


def staff_view_mfc_pastyear(mysql) -> tuple:
    today = datetime.datetime.today()
    past_year = today.replace(year=(today.year-1))
    return staff_view_mfc_range(str(past_year)[0:-7], str(today)[0:-7], mysql)

def staff_view_customer_flight_history(EMAIL: str, AIRLINE: str, mysql) -> tuple:
    sql = f'''
    SELECT flight_num, airline, dept_datetime
    FROM ticket
    WHERE id IN (
        SELECT ticket_id
        FROM purchase
        WHERE customer_email='{EMAIL}'
        )
        AND airline = '{AIRLINE}' ;
    '''
    data = exec_sql(sql, mysql)
    headings=(
        'Flight Num',
        'Airline',
        'Departure'
    )
    return (headings,data)



# USE CASE 8: view tickets sold
def staff_view_tickets_sold_range(START: str, END: str, AIRLINE: str, mysql) -> tuple:
    sql = f'''
    SELECT count(*) as ticket_sold
    FROM ticket as t JOIN purchase as p ON t.id=p.ticket_id
    WHERE t.airline='{AIRLINE}'
        AND p.purchase_datetime BETWEEN '{START}' AND '{END}'
    '''
    data = exec_sql(sql, mysql)
    headings=('Num Tickets')
    return (headings,data)

# Implemented using JS to autofill field
def staff_view_tickets_sold_pastmonth(AIRLINE: str, mysql) -> tuple:
    today = datetime.datetime.today()
    past_month = today.replace(month=(today.month - 1))
    return staff_view_mfc_range(str(past_month)[0:-7], str(today)[0:-7], AIRLINE, mysql)

# Implemented using JS to autofill field
def staff_view_tickets_sold_pastyear(AIRLINE: str, mysql) -> tuple:
    today = datetime.datetime.today()
    past_year = today.replace(year=(today.year - 1))
    return staff_view_mfc_range(str(past_year)[0:-7], str(today)[0:-7], AIRLINE, mysql)

# Monthly ticket spending for the past year (for bar chart)
def staff_view_tickets_sold_monthly(AIRLINE: str, mysql) -> tuple:
    today = datetime.datetime.today()
    start = today.replace(year=(today.year - 1), day=1)  # 1 year ago, 1st day of month
    end = increment_dt_month(start)
    monthly_totals = []
    for i in range(12):
        start = increment_dt_month(start)
        end = increment_dt_month(end)
        _, t_sold = staff_view_tickets_sold_range(start, end, AIRLINE, mysql)
        t_sold = t_sold[0][0]
        monthly_totals.append(t_sold)
    return monthly_totals, today.month


# USE CASE 8: view revenue
def staff_view_revenue_range(START: str, END: str, AIRLINE: str, mysql) -> tuple:
    sql = f'''
    SELECT sum(p.sold_price) as revenue
    FROM ticket as t JOIN purchase as p ON t.id=p.ticket_id
    WHERE t.airline='{AIRLINE}'
        AND p.purchase_datetime BETWEEN '{START}' AND '{END}'
    '''
    data = exec_sql(sql, mysql)
    headings=('Revenue')
    return (headings,data)

def staff_view_revenue_pastmonth(AIRLINE: str, mysql) ->  tuple:
    today = datetime.datetime.today()
    past_month = today.replace(month=(today.month - 1))
    return staff_view_revenue_range(str(past_month)[0:-7], str(today)[0:-7], AIRLINE, mysql)


def staff_view_revenue_pastyear(AIRLINE: str, mysql) ->  tuple:
    today = datetime.datetime.today()
    past_year = today.replace(year=(today.year - 1))
    return staff_view_revenue_range(str(past_year)[0:-7], str(today)[0:-7], AIRLINE, mysql)


# HELPERS
def planes_of_airline(AIRLINE, mysql):
    sql = f'''
    SELECT id
    FROM airplane
    WHERE airline = '{AIRLINE}';
    '''
    return exec_sql(sql, mysql)