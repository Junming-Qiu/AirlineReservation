from utils.general import *
import random
import string

'''

CUSTOMER EXCLUSIVE FUNCTIONS



'''


### VIEW MY FLIGHTS ###

# DO NOT CALL
def _my_flight_table(EMAIL: str):
    sql = f'''
    FROM flight as f, ticket as t, purchase as p,
        airport as ap_origin, airport as ap_dest
    WHERE f.flight_num=t.flight_num
        AND f.airline=t.airline
        AND f.dept_datetime=t.dept_datetime
        AND f.origin=ap_origin.name
        AND f.destination=ap_dest.name
        AND t.id=p.ticket_id
        AND p.customer_email='{EMAIL}' '''
    return sql


# view the flights purchased by a customer
def customer_view_my_flights(EMAIL: str, mysql,
                             START_DATE=None, END_DATE=None,
                             AP_ORIGIN=None, AP_DEST=None,
                             CITY_ORIGIN=None, CITY_DEST=None) ->  list[tuple]:
    sql = f'''
    SELECT DISTINCT t.id, ap_origin.city, ap_dest.city,
    f.flight_num, f.airline, f.dept_datetime, f.base_price {_my_flight_table(EMAIL)} '''

    if START_DATE: # NOT NULL
        sql+=f'''
        AND f.dept_datetime>={START_DATE}'''                                                                                   # TODO, should this be =?

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
        AND ap_origin.city='{CITY_ORIGIN}' '''

    if CITY_DEST:
        sql+=f'''
        AND ap_dest.city='{CITY_DEST}' '''

    sql += ';'
    data = exec_sql(sql, mysql)
    headings = ('Ticket ID',
                'Origin',
                'Destination',
                'Flight Number',
                'Airline',
                'Departure',
                'Price')
    return (headings, data)




### PURCHASE TICKET ###

# make unique, unused ticket id (DO NOT CALL)
def _generate_ticket_id(mysql) -> str:

    id=''
    sql = f'''
    SELECT *
    FROM purchase
    WHERE purchase.ticket_id='{id}';'''

    while True:
        id = ''.join(random.choices(string.hexdigits, k=7)).upper()
        if not (exec_sql(sql,mysql)):
            return id

# make a new row in ticket (DO NOT CALL)
def _create_ticket(FNUM: str, AIRLINE: str, DEPT_DT: str, mysql) -> str:
    tid=_generate_ticket_id(mysql)
    sql=f'''
    INSERT INTO ticket
    VALUES ('{tid}','{FNUM}','{AIRLINE}',{DEPT_DT});'''
    exec_sql(sql,mysql,commit=True)
    return tid

# check if a card number exists (DO NOT CALL)
def _card_exists(NUM: str, mysql) -> bool:
    sql=f'''
    SELECT *
    FROM card_info
    WHERE card_number='{NUM}';
    '''
    return exec_sql(sql, mysql)

# make a new row in card info (DO NOT CALL)
def _create_card_info(NUM: str, EXPR: str, NAME: str,
                      TYPE: str, mysql) -> None:

    if TYPE not in ('credit', 'debit'):
        raise Exception('Invalid card type')

    if not (_card_exists(NUM, mysql)):
        sql=f'''
        INSERT INTO card_info
        VALUES ('{NUM}',{EXPR},'{NAME}','{TYPE}');
        '''
        exec_sql(sql,mysql,commit=True)

# make a new row in purchase (DO NOT CALL)
def _create_purchase(EMAIL: str, TID: str, PURCHASE_DT: str, SOLD_PRICE: str,
                     BASE_PRICE: str, CARD_NUM: str, mysql) -> None:

    sql=f'''
    INSERT INTO purchase
    VALUES ('{EMAIL}','{TID}',{PURCHASE_DT},{SOLD_PRICE},{BASE_PRICE},'{CARD_NUM}');
    '''
    exec_sql(sql, mysql, commit=True)
    
    
def get_sold_price(FNUM: str, AIRLINE: str, DEPT_DT: str,
                   BPRICE: str, mysql):
    """Determines if 25% surcharge is added onto ticket base price before selling
    (decided by flight capacity). Also makes sure flight isn't already full."""
    sql = f'''
            SELECT ap.num_seats
            FROM airplane as ap JOIN flight as f
                ON ap.id = f.airplane_id
            WHERE f.flight_num = '{FNUM}'
             AND f.airline = '{AIRLINE}'
             AND f.dept_datetime = {DEPT_DT};
            '''
    try:
        capacity = exec_sql(sql, mysql)[0][0]
    except:
        capacity = -1 # TODO change to error msg - result of bad seasrch


    # assuming tickets are only created when a customer tries to buy one
    # so number of tickets in purchase table = num tickets sold
    sql = f'''
            SELECT COUNT(*)
            FROM purchase as p JOIN ticket as t 
                ON p.ticket_id = t.id
            GROUP BY t.flight_num, t.airline, t.dept_datetime
            HAVING t.flight_num = '{FNUM}'
             AND t.airline = '{AIRLINE}'
             AND t.dept_datetime = {DEPT_DT};
            '''
    try:
        tickets_sold = exec_sql(sql, mysql)[0][0]
    except:
        tickets_sold = 0
    print(f'Tickets Sold: {tickets_sold}')
    print(f'Capacity: {capacity}')
    if tickets_sold >= capacity:
        price = None
    elif tickets_sold >= (0.6 * capacity):
        price = float(BPRICE) * 1.25
    else:
        price = float(BPRICE)

    return price


def get_base_price(FNUM: str, AIRLINE: str, DEPT_DT: str, mysql):
    sql=f'''
    SELECT base_price
    FROM flight
    WHERE flight_num='{FNUM}'
        AND airline='{AIRLINE}'
        AND dept_datetime={DEPT_DT};
    '''
    return exec_sql(sql, mysql)[0][0]

# purchase a ticket of a flight
def customer_purchase_ticket(FNUM: str, AIRLINE: str, DEPT_DT: str,         # flight info
                             SPRICE: str, BPRICE: str,
                             CNUM: str, EXPR: str, NAME: str, TYPE: str,    # card info
                             EMAIL: str,                                    # customer info
                             mysql):

    # 0. check for available seats
    # MOVED TO __init__


    # 1. make ticket
    ticket_id=_create_ticket(FNUM, AIRLINE, DEPT_DT, mysql)

    # 2. check for card info / make card info
    _create_card_info(CNUM, EXPR, NAME, TYPE, mysql)


    # 3. make purchase
    today = date_in_X_days(0)
    _create_purchase(EMAIL, ticket_id, today, SPRICE, BPRICE, CNUM, mysql)



### CANCEL A TRIP ##

# DO NOT CALL
def _validate_ticket_ownership(EMAIL: str, TID: str, mysql):
    sql=f'''
    SELECT *
    FROM purchase
    WHERE customer_email='{EMAIL}'
        AND ticket_id='{TID}';
    '''
    return exec_sql(sql, mysql)


# DO NOT CALL
def _validate_ticket_exists(TID: str, mysql):
    sql=f'''
    SELECT * 
    FROM ticket
    WHERE id='{TID}';
    '''
    return exec_sql(sql, mysql)


# remove a row from ticket
def customer_cancel_ticket(EMAIL: str, TID: str, mysql):
    if _validate_ticket_ownership(EMAIL, TID, mysql): # ticket was purchased by customer
        if _validate_ticket_exists(TID, mysql): # ticket was not already cancelled
            sql=f'''
            DELETE FROM ticket
            WHERE id='{TID}';
            '''
            exec_sql(sql, mysql, commit=True)
        else:
            raise Exception('Ticket already was cancelled')
    else:
        raise Exception('Ticket not associated with customer email')

### MAKE FLIGHT REVIEW / COMMENT ###

# DO NOT CALL
def _validate_customer_took_flight(EMAIL: str, TID: str, mysql):
    sql = f'''
    SELECT *
    FROM purchase as p, ticket as t
    WHERE p.ticket_id=t.id
        AND p.customer_email='{EMAIL}'
        AND t.id='{TID}';
    '''
    return exec_sql(sql, mysql)



# create a review, comment
def customer_create_review(EMAIL: str, TID: str, RATING: str, COMMENT: str, mysql):

    if _validate_customer_took_flight(EMAIL, TID, mysql): # customer was on flight
        print('HERE')
        sql=f'''
        INSERT INTO flight_review
        VALUES ('{EMAIL}', '{TID}', {RATING}, '{COMMENT}');
        '''
        exec_sql(sql, mysql, commit=True)
    else:
        raise Exception('No available record of flight attendance')

def customer_view_review(EMAIL, mysql):
    sql=f'''
    SELECT ticket_id, rating, comment
    FROM flight_review
    WHERE customer_email='{EMAIL}';
    '''
    data = exec_sql(sql, mysql)
    headings = (
        'Ticket ID',
        'Rating',
        'Comment'
    )
    return (headings, data)

### TRACK SPENDING ###

# sum spending in a given interval
def customer_view_spending_interval(EMAIL: str, START: str, END: str, mysql) -> tuple:
    sql=f'''
    SELECT sum(sold_price)
    FROM purchase
    WHERE purchase_datetime BETWEEN {START} AND {END}
    GROUP BY customer_email
    HAVING customer_email='{EMAIL}';
    '''
    try:
        data=exec_sql(sql, mysql)[0][0]
    except:
        data='0'
    headings='Spending'
    return (headings,data)


# sum spending in the past 6 months
def customer_view_spending_past6months(EMAIL: str, mysql) -> tuple:
    start = date_in_X_days(-183)
    end = date_in_X_days(0)
    return customer_view_spending_interval(EMAIL, start, end, mysql)


# sum spending in the past year
def customer_view_spending_pastyear(EMAIL: str, mysql) -> tuple:
    start = date_in_X_days(-365)
    end = date_in_X_days(0)
    return customer_view_spending_interval(EMAIL, start, end, mysql)
