from functions import *
from flask_mysqldb import MySQL
# ****************
# STAFF USE CASES
# ****************
'''
    THESE ARE ALL
        UNTESTED
        INITIAL VERSIONS

    THESE ALL ASSUME THAT:
    1. Dates are correctly formatted; see check_datetime_format()

'''


# 1.1 view flight based on next 30 days
def staff_view_flight_all(AIRLINE: str, before, after, source, destination, s_city, d_city, mysql) -> list[tuple]:
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
    print(sql)
    rtn = exec_sql(sql, mysql)
    return rtn

# 1.2 view flight based on airline (combined)
def staff_view_flight_airline(AIRLINE: str, mysql) -> list[tuple]:
    sql = f'''
    SELECT *
    FROM flight
    WHERE airline = '{AIRLINE}';
    '''
    rtn = exec_sql(sql, mysql)
    return rtn

# 1.3 view flight based on a range of dates (combined)
def staff_view_flight_date_range(START: str, END: str, mysql) -> list[tuple]:
    sql = f'''
    SELECT *
    FROM flight
    WHERE dept_datetime BETWEEN {START} AND {END};
    '''
    rtn = exec_sql(sql, mysql)
    return rtn

# 1.4 view flight based on airport source (combined)
def staff_view_flight_airport_origin(ORIGIN: str, mysql) -> list[tuple]:
    sql = f'''
    SELECT *
    FROM flight
    WHERE origin = '{ORIGIN}';
    '''
    rtn = exec_sql(sql, mysql)
    return rtn

# 1.5 view flight based on airport destination (combined)
def staff_view_flight_airport_dest(DESTINATION: str, mysql) -> list[tuple]:
    sql = f'''
    SELECT *
    FROM flight
    WHERE origin = '{DESTINATION}';
    '''
    rtn = exec_sql(sql, mysql)
    return rtn

# 1.6 view flight based on city origin (combined)
def staff_view_flight_city_origin(CITY: str, mysql) -> list[tuple]:
    sql = f''' 
    SELECT f.flight_num, f.airline, f.airplane_id,
        f.arrv_datetime, f.dept_datetime, f.base_price,
        f.origin, f.destination, f.flight_status
    FROM flight as f JOIN airport as a ON f.origin=a.name
    WHERE a.city = '{CITY}';    
    '''
    rtn = exec_sql(sql, mysql)
    return rtn

# 1.7 view flight based on city destination (combined)
def staff_view_flight_city_destination(CITY: str, mysql) -> list[tuple]:
    sql = f''' 
    SELECT f.flight_num, f.airline, f.airplane_id,
        f.arrv_datetime, f.dept_datetime, f.base_price,
        f.origin, f.destination, f.flight_status
    FROM flight as f JOIN airport as a ON f.destination=a.name
    WHERE a.city = '{CITY}';    
    '''
    rtn = exec_sql(sql, mysql)
    return rtn

# 1.8 view customers on a flight
def staff_view_flight_passengers(FNUM: str, AIRLINE: str, DEPT_DT: str, mysql) -> list[tuple]:
    sql = f'''
    SELECT c.name, c.email, c.phone_number
    FROM customer as c, purchase as p, ticket as t
    WHERE c.email = p.customer_email
        AND p.ticket_id = t.id
        AND t.flight_num = '{FNUM}'
        AND t.airline = '{AIRLINE}'
        AND t.dept_datetime = {DEPT_DT};
    '''

    rtn = exec_sql(sql, mysql)
    return rtn

# 2.1 create a new flight
def staff_create_flight(FNUM: str, AIRLINE: str, AIRPLANE_ID: str,
                            ARRV_DT: str, DEPT_DT: str, BASE_PRICE: str,
                            ORGN: str, DEST: str, FSTAUS: str, mysql) -> None:
    sql =f'''
        BEGIN
        IF NOT EXISTS (SELECT * 
                        FROM flight 
                        WHERE flight_num='{FNUM}'
                            AND airline='{AIRLINE}'
                            AND dept_datetime={DEPT_DT};)
        BEGIN
            INSERT INTO flight
            VALUES ('{FNUM}', '{AIRLINE}', '{AIRPLANE_ID}', {ARRV_DT},
             {DEPT_DT}, {BASE_PRICE}, '{ORGN}', '{DEST}', '{FSTAUS}')
        END
    END;
    '''

    print(sql)

    exec_sql(sql, mysql)

# 3.1 change flight status
def staff_update_flight_status(FNUM: str, AIRLINE: str,
                                 DEPT_DT: str, STATUS: str, mysql) -> None:
    sql =f'''
    BEGIN
        IF EXISTS (SELECT * 
                    FROM flight 
                    WHERE flight_num='{FNUM}'
                        AND airline='{AIRLINE}'
                        AND dept_datetime={DEPT_DT};)
        BEGIN
            UPDATE flight 
            SET flight_status='{STATUS}' 
            WHERE flight_num='{FNUM}'
                AND airline='{AIRLINE}'
                AND dept_datetime={DEPT_DT};
        END
    END;
    '''
    exec_sql(sql, mysql)

# 4.1 add airplane in the system,
#   display all airplanes owned by airline
def staff_create_airplane(ID: str, AIRLINE: str, NUM_SEATS: str,
                          AGE: str, MANUFACTURER: str, mysql) -> list[tuple]:
    insert_sql = f'''
    BEGIN
        IF NOT EXISTS (SELECT * FROM airplane
                    WHERE id='{ID}' AND airline='{AIRLINE}';)
        BEGIN
            INSERT INTO airplane
            VALUES ('{ID}', '{AIRLINE}', {NUM_SEATS}, {AGE},'{MANUFACTURER}')
        END
    END;
    '''
    exec_sql(insert_sql, mysql)

    view_sql = f'''
    SELECT *
    FROM airplane
    WHERE airline='{AIRLINE}';
    '''
    rtn = exec_sql(view_sql)
    return rtn

# 5.1 add new airport
def staff_create_airport(NAME: str, CITY: str, COUNTRY: str, TYPE: str, mysql) -> None:
    sql = f'''
    BEGIN
        IF NOT EXISTS (SELECT * FROM airport WHERE name='{NAME}';)
        BEGIN
            INSERT INTO airport
            VALUES ('{NAME}', '{CITY}', '{COUNTRY}', '{TYPE}')
        END
    END;
    '''
    exec_sql(sql, mysql)

# 6.1 view flight average rating
def staff_view_flight_avg_rating(FLIGHT_NUM: str, AIRLINE: str, DEPT_DATETIME: str, mysql): #TODO Type?
    sql = f'''
    SELECT avg(f.rating)
    FROM flight_review as f join ticket as t on f.ticket_id = t.id
    GROUP BY t.flight_num, t.airline, t.dept_datetime
    HAVING t.flight_num = '{FLIGHT_NUM}'
        AND t.airline = '{AIRLINE}'
        AND t.dept_datetime = '{DEPT_DATETIME}';
    '''
    rtn = exec_sql(sql, mysql)
    return rtn

# 6.2 view flight ratings and comments
def staff_view_flight_avg_rating(FLIGHT_NUM: str, AIRLINE: str, DEPT_DATETIME: str, mysql) -> list[tuple]:
    sql = f'''
    SELECT rating, comment
    FROM flight_review join ticket on flight_review.ticket_id = ticket.id
    WHERE flight_num = '{FLIGHT_NUM}'
        AND airline = '{AIRLINE}'
        AND dept_datetime = '{DEPT_DATETIME}';
    '''
    rtn = exec_sql(sql, mysql)
    return rtn

# 7.1 return most frequent customer (fc) within a date range
# DO NOT CALL !!!
def staff_view_frequent_customer_range(START: str, END: str, mysql) -> list[tuple]:
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
    rtn = exec_sql(sql, mysql)
    return rtn

# 7.2 view most frequent customer in the last month
def staff_view_frequent_customer_month() -> list[tuple]:
    first = str(datetime.today().date().replace(day=1))
    start = first[0:4] + first[5:7] + first[8:10]

    today = str(datetime.date.today())
    end = today[0:4] + today[5:7] + today[8:10]

    return staff_view_frequent_customer_range(start, end)

# 7.3 view most frequent customer in the last year
def staff_view_frequent_customer_year() -> list[tuple]:
    first = str(datetime.today().date().replace(day=1, month=1))
    start = first[0:4] + first[5:7] + first[8:10]

    today = str(datetime.date.today())
    end = today[0:4] + today[5:7] + today[8:10]

    return staff_view_frequent_customer_range(start, end)

# 7.4 view a customer's flight history
def staff_view_customer_flight_history(EMAIL: str, AIRLINE: str, mysql: MySQL) -> list[tuple]:
    sql = f'''
    SELECT flight_num, airline, dept_datetime
    FROM ticket
    WHERE id IN (
        SELECT ticket_id
        FROM purchase
        WHERE customer_email='{EMAIL}'
        );
    '''
    rtn = exec_sql(sql, mysql)
    return rtn

# 8.1 return the total number of tickets sold based on a range of dates
def staff_view_tickets_sold_range(START: str, END: str, AIRLINE: str, mysql: MySQL) -> list[tuple]:
    sql = f'''
    SELECT count(*) as ticket_sold
    FROM ticket as t JOIN purchase as p ON t.id=p.ticket_id
    WHERE t.airline='{AIRLINE}'
        AND p.purchase_datetime BETWEEN {START} AND {END}
    '''
    rtn = exec_sql(sql, mysql)
    return rtn

# 8.2 return the total number of tickets sold in the last month
def staff_view_tickets_sold_month(AIRLINE: str, mysql: MySQL) -> list[tuple]:
    first = str(datetime.today().date().replace(day=1))
    month_start = first[0:4] + first[5:7] + first[8:10]

    today = str(datetime.date.today())
    end = today[0:4] + today[5:7] + today[8:10]

    return staff_view_tickets_sold_range(month_start, end, AIRLINE)

# 8.3 return the total number of tickets sold in the last year
def staff_view_tickets_sold_year(AIRLINE: str, mysql: MySQL) -> list[tuple]:
    first = str(datetime.today().date().replace(day=1, month=1))
    year_start = first[0:4] + first[5:7] + first[8:10]

    today = str(datetime.date.today())
    end = today[0:4] + today[5:7] + today[8:10]

    return staff_view_tickets_sold_range(year_start, end, AIRLINE)

# 9.1 return the total number of revenue based on a range of dates
def staff_view_revenue_range(START: str, END: str, AIRLINE: str, mysql: MySQL) -> list[tuple]:
    sql = f'''
    SELECT sum(p.sold_price) as revenue
    FROM ticket as t JOIN purchase as p ON t.id=p.ticket_id
    WHERE t.airline='{AIRLINE}'
        AND p.purchase_datetime BETWEEN {START} AND {END}
    '''
    rtn = exec_sql(sql, mysql)
    return rtn

# 9.2 return the total amount of revenue in the last month
def staff_view_revenue_month(AIRLINE: str, mysql: MySQL) -> list[tuple]:
    first = str(datetime.today().date().replace(day=1))
    month_start = first[0:4] + first[5:7] + first[8:10]

    today = str(datetime.date.today())
    end = today[0:4] + today[5:7] + today[8:10]

    return staff_view_revenue_range(month_start, end, AIRLINE, mysql)

# 9.3 return the total amount of revenue in the last year
def staff_view_revenue_year(AIRLINE: str, mysql: MySQL) -> list[tuple]:
    first = str(datetime.today().date().replace(day=1, month=1))
    year_start = first[0:4] + first[5:7] + first[8:10]

    today = str(datetime.date.today())
    end = today[0:4] + today[5:7] + today[8:10]

    return staff_view_revenue_range(year_start, end, AIRLINE)

# TODO: 10 LogOut