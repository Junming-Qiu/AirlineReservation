from utils.general import *

'''

NOTE : these functions do not ensure that the
    AIRLINE parameter matches the staff's employer.
    
    This should be implemented elsewhere.    


'''

# USE CASE 1: view flights
def staff_view_flight_all(AIRLINE: str, before, after, source, destination, s_city, d_city, mysql) -> tuple:
    if not before:
        before = date_in_X_days(0)

    if not after:
        after = date_in_X_days(30)

    sql = f'''
        SELECT f.flight_num, f.airline, f.airplane_id,
        f.arrv_datetime, f.dept_datetime, f.base_price,
        f.origin, f.destination, f.flight_status
        FROM flight as f JOIN airport as a ON f.origin=a.name JOIN airport as b ON f.destination=b.name
        WHERE f.airline = '{AIRLINE}'
    '''

    if before and after:
        sql += f" AND f.dept_datetime BETWEEN {before} AND {after}"

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
        AND t.dept_datetime = {DEPT_DT};
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
    VALUES('{FNUM}', '{AIRLINE}', '{AIRPLANE_ID}', {ARRV_DT},
           {DEPT_DT}, {BASE_PRICE}, '{ORGN}', '{DEST}', '{FSTAUS}');
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
            AND dept_datetime={DEPT_DT};
    '''
    exec_sql(sql, mysql, commit=True)



# USE CASE 4: add an airline
def staff_create_airplane(ID: str, AIRLINE: str, NUM_SEATS: str,
                          AGE: str, MANUFACTURER: str, mysql) -> tuple:
    insert_sql = f'''
    INSERT INTO airplane
    VALUES ('{ID}', '{AIRLINE}', {NUM_SEATS}, {AGE},'{MANUFACTURER}');
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
def staff_view_avg_rating(FLIGHT_NUM: str, AIRLINE: str, DEPT_DATETIME: str, mysql) -> tuple:
    sql = f'''
    SELECT avg(f.rating)
    FROM flight_review as f join ticket as t on f.ticket_id = t.id
    GROUP BY t.flight_num, t.airline, t.dept_datetime
    HAVING t.flight_num = '{FLIGHT_NUM}'
        AND t.airline = '{AIRLINE}'
        AND t.dept_datetime = '{DEPT_DATETIME}';
    '''
    data = exec_sql(sql, mysql)
    headings=(
        'Avg Rating'
    )
    return (headings,data)

def staff_view_ratings_and_comments(FLIGHT_NUM: str, AIRLINE: str, DEPT_DATETIME: str, mysql) -> tuple:
    sql = f'''
    SELECT rating, comment
    FROM flight_review join ticket on flight_review.ticket_id = ticket.id
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
def staff_view_mfc_range(START: str, END: str, mysql) -> tuple:
    sql = f'''
    SELECT tmp.num as 'num_purchases', c.name, c.email, c.phone_number
    FROM
        (SELECT customer_email, count(*) as num
        FROM purchase
        WHERE purchase_datetime BETWEEEN {START} AND {END}
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

def staff_view_mfc_pastmonth() -> tuple:
    first = str(datetime.today().date().replace(day=1))
    start = first[0:4] + first[5:7] + first[8:10]

    today = str(datetime.date.today())
    end = today[0:4] + today[5:7] + today[8:10]

    return staff_view_mfc_range(start, end)

def staff_view_mfc_pastyear() -> tuple:
    first = str(datetime.today().date().replace(day=1, month=1))
    start = first[0:4] + first[5:7] + first[8:10]

    today = str(datetime.date.today())
    end = today[0:4] + today[5:7] + today[8:10]

    return staff_view_mfc_range(start, end)

def staff_view_customer_flight_history(EMAIL: str, AIRLINE: str, mysql) -> tuple:
    sql = f'''
    SELECT flight_num, airline, dept_datetime
    FROM ticket
    WHERE id IN (
        SELECT ticket_id
        FROM purchase
        WHERE customer_email='{EMAIL}'
        );
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
        AND p.purchase_datetime BETWEEN {START} AND {END}
    '''
    data = exec_sql(sql, mysql)
    headings=('Num Tickets')
    return (headings,data)

def staff_view_tickets_sold_pastmonth(AIRLINE: str, mysqlL) -> tuple:
    first = str(datetime.today().date().replace(day=1))
    month_start = first[0:4] + first[5:7] + first[8:10]

    today = str(datetime.date.today())
    end = today[0:4] + today[5:7] + today[8:10]

    return staff_view_tickets_sold_range(month_start, end, AIRLINE)

def staff_view_tickets_sold_pastyear(AIRLINE: str, mysql) -> tuple:
    first = str(datetime.today().date().replace(day=1, month=1))
    year_start = first[0:4] + first[5:7] + first[8:10]

    today = str(datetime.date.today())
    end = today[0:4] + today[5:7] + today[8:10]

    return staff_view_tickets_sold_range(year_start, end, AIRLINE)



# USE CASE 8: view revenue
def staff_view_revenue_range(START: str, END: str, AIRLINE: str, mysql) -> tuple:
    sql = f'''
    SELECT sum(p.sold_price) as revenue
    FROM ticket as t JOIN purchase as p ON t.id=p.ticket_id
    WHERE t.airline='{AIRLINE}'
        AND p.purchase_datetime BETWEEN {START} AND {END}
    '''
    data = exec_sql(sql, mysql)
    headings=('Revenue')
    return (headings,data)

def staff_view_revenue_pastmonth(AIRLINE: str, mysql) ->  tuple:
    first = str(datetime.today().date().replace(day=1))
    month_start = first[0:4] + first[5:7] + first[8:10]

    today = str(datetime.date.today())
    end = today[0:4] + today[5:7] + today[8:10]

    return staff_view_revenue_range(month_start, end, AIRLINE, mysql)

def staff_view_revenue_pastyear(AIRLINE: str, mysql) ->  tuple:
    first = str(datetime.today().date().replace(day=1, month=1))
    year_start = first[0:4] + first[5:7] + first[8:10]

    today = str(datetime.date.today())
    end = today[0:4] + today[5:7] + today[8:10]

    return staff_view_revenue_range(year_start, end, AIRLINE)
