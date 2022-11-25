from utils.general import *
import random
import string






# TODO: Refactor Airline Staff, fix datetime stuff



# USE CASE 1: view purchased flights

# return a joined table containing flights purchased by email (DO NOT CALL)
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

# view the flights purchased by a customer (optionally, given some filter param)
def customer_view_my_flights(EMAIL: str,
                             START_DATE=None, END_DATE=None,
                             AP_ORIGIN=None, AP_DEST=None,
                             CITY_ORIGIN=None, CITY_DEST=None) ->  list[tuple]:
    '''



    :return:
    '''



    sql = f'''
    SELECT f.flight_num, f.airline, f.dept_datetime, f.status {_my_flight_table(EMAIL)} '''

    if START_DATE: # NOT NULL
        sql+=f'''
        AND f.dept_datetime>={START_DATE})'''

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
    print(sql)
    #return exec_sql(sql, mysql)




# USE CASE 2: view future flights

# search for two-way flights
def customer_view_twoway_flights(START_DATE=None, END_DATE=None,
                                        AP_ORIGIN=None, AP_DEST=None,
                                        CITY_ORIGIN=None, CITY_DEST=None) ->  list[tuple]:
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


# search for one-way flights
def customer_view_oneway_flights(START_DATE=None, END_DATE=None,
                                        AP_ORIGIN=None, AP_DEST=None,
                                        CITY_ORIGIN=None, CITY_DEST=None) ->  list[tuple]:
    sql = '''
    SELECT DISTINCT f.origin, f.destination, 
    f.flight_num, f.airline, f.dept_datetime, f.base_price
    FROM flight as f, airport as ap_origin, airport as ap_dest
    WHERE f.origin=ap_origin.name
        AND f.destination=ap_dest.name'''

    if START_DATE: # NOT NULL
        sql+=f'''
        AND f.dept_datetime>={START_DATE}'''
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
    return sql



# USE CASE 3: purchase tickets

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
    exec_sql(sql,mysql)
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

    if not (_card_exists(NUM)):
        sql=f'''
        INSERT INTO card_info
        VALUES ('{NUM}',{EXPR},'{NAME}','{TYPE}');
        '''
        exec_sql(sql,mysql)

# make a new row in purchase (DO NOT CALL)
def _create_purchase(EMAIL: str, TID: str, PURCHASE_DT: str, SOLD_PRICE: str,
                     BASE_PRICE: str, CARD_NUM: str, mysql) -> None:

    sql=f'''
    INSERT INTO purchase
    VALUES ('{EMAIL}','{TID}',{PURCHASE_DT},{SOLD_PRICE},{BASE_PRICE},'{CARD_NUM}');
    '''
    exec_sql(sql, mysql)

# purchase a ticket of a flight TODO CALL THIS FUNCTION
def customer_purchase_ticket(FNUM: str, AIRLINE: str, DEPT_DT: str,         # flight info
                             SPRICE: str, BPRICE: str,
                             CNUM: str, EXPR: str, NAME: str, TYPE: str,    # card info
                             EMAIL: str,                                    # customer info
                             mysql):

    # ?. check for available seats

    # 1. make ticket
    ticket_id=_create_ticket(FNUM, AIRLINE, DEPT_DT, mysql)

    # 2. check for card info / make card info
    try:
        _create_card_info(CNUM, EXPR, NAME, TYPE)
    except:
        pass

    # 3. make purchase
    today = date_in_X_days(0)
    _create_purchase(EMAIL, ticket_id, today, SPRICE, BPRICE, CNUM)



# USE CASE 4: cancel a trip

# check that a ticket exists in purchase table with customer email (DO NOT CALL)
def _validate_ticket_ownership(EMAIL, TID, mysql):
    sql=f'''
    SELECT *
    FROM purchase
    WHERE customer_email='{EMAIL}'
        AND ticket_id='{TID}';
    '''
    return exec_sql(sql, mysql)

# check that a ticket exists in ticket table (DO NOT CALL)
def _validate_ticket_exists(TID, mysql):
    sql=f'''
    SELECT * 
    FROM ticket
    WHERE id='{TID}';
    '''
    return exec_sql(sql, mysql)

# remove a row from ticket
def customer_cancel_ticket(EMAIL, TID, mysql):
    if _validate_ticket_ownership(EMAIL, TID, mysql): # ticket was purchased by customer
        if _validate_ticket_exists(TID, mysql): # ticket was not already cancelled
            sql=f'''
            DELETE FROM ticket
            WHERE id='{TID}';
            '''
            exec_sql(sql, mysql)
        else:
            raise Exception('Ticket already was cancelled')
    else:
        raise Exception('Ticket not associated with customer email')

# USE CASE 5: create flight_review

# check if ticket id exists in ticket & purchase,
#   in purchase with customer email (DO NOT CALL)
def _validate_customer_took_flight(EMAIL, TID, mysql):
    sql = f'''
    SELECT *
    FROM purchase as p, ticket as t
    WHERE p.ticket_id=t.id
        AND p.customer_email='{EMAIL}'
        AND t.id='{TID}';
    '''
    exec_sql(sql, mysql)

# make a new row in flight review
def customer_create_flight_review(EMAIL, TID, RATING, COMMENT, mysql):

    if _validate_customer_took_flight(EMAIL, TID, mysql): # customer was on flight
        sql=f'''
        INSERT INTO flight_rating
        VALUES ('{EMAIL}', '{TID}', {RATING}, '{COMMENT}');
        '''
        exec_sql(sql, mysql)
    else:
        raise Exception('No available record of flight attendance')




# USE CASE 6: track spending

def customer_view_spending_interval(EMAIL, START, END, mysql) -> int:
    sql=f'''
    SELECT sum(sold_price)
    FROM purchase
    WHERE purchase_datetime BETWEEN {START} AND {END}
    GROUP BY customer_email
    HAVING customer_email={EMAIL};
    '''
    rtn=exec_sql(sql, mysql)
    return rtn[0]

def customer_view_spending_past6months(EMAIL, mysql) -> int:
    start = date_in_X_days(-183)
    end = date_in_X_days(0)
    return customer_view_spending_interval(EMAIL, start, end, mysql)

def customer_view_spending_pastyear(EMAIL, mysql) -> int:
    start = date_in_X_days(-365)
    end = date_in_X_days(0)
    return customer_view_spending_interval(EMAIL, start, end, mysql)



# USE CASE 7: logout