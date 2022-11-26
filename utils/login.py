from general import *

'''







'''


#
def store_verify(session, customer_tokens, staff_tokens):
    username_or_email = ""
    key = ""
    c_logged = False
    s_logged = False

    if "username" in session:
        username_or_email = session["username"]
    if "key" in session:
        key = session["key"]

    if username_or_email in customer_tokens:
        if customer_tokens[username_or_email] == key:
            c_logged = True

    if username_or_email in staff_tokens:
        if staff_tokens[username_or_email] == key:
            s_logged = True

    return c_logged, s_logged


# check if a staff's log in credentials exists
def query_staff_credentials(USERNAME: str, PASSWORD: str, mysql) -> list:
    ENCRYPTED_PASSWORD = encrypt_password(PASSWORD)
    sql = f'''
        SELECT *
        FROM airline_staff
        WHERE username = '{USERNAME}'
            AND password = '{ENCRYPTED_PASSWORD}';
        '''
    return exec_sql(sql, mysql)


# check if a customer's log in credentials exists
def query_customer_credentials(EMAIL: str, PASSWORD: str, mysql) -> list:
    ENCRYPTED_PASSWORD = encrypt_password(PASSWORD)
    sql = f'''
        SELECT *
        FROM customer
        WHERE email = '{EMAIL}'
            AND password = '{ENCRYPTED_PASSWORD}';
        '''
    return exec_sql(sql, mysql)