from utils.general import *

'''

NOTE : these functions do not ensure that the
    AIRLINE parameter matches the staff's employer.
    
    This should be implemented elsewhere.    


'''



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


def staff_create_flight(FNUM: str, AIRLINE: str, AIRPLANE_ID: str,
                            ARRV_DT: str, DEPT_DT: str, BASE_PRICE: str,
                            ORGN: str, DEST: str, FSTAUS: str, mysql) -> None:
    sql=f'''
    INSERT INTO flight
    VALUES('{FNUM}', '{AIRLINE}', '{AIRPLANE_ID}', {ARRV_DT},
           {DEPT_DT}, {BASE_PRICE}, '{ORGN}', '{DEST}', '{FSTAUS}');
    '''
    exec_sql(sql, mysql, commit=True)

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