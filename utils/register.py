from utils.general import *

'''

Register a staff or customer account





'''

# ******************
# STAFF REGISTRATION
# ******************

# check if a staff's username already exists
def query_staff_username(USERNAME: str, mysql) -> bool:
    sql = f'''
    SELECT *
    FROM airline_staff
    WHERE username = '{USERNAME}';
    '''
    username_exists = exec_sql(sql, mysql)
    if username_exists:
        return True
    return False


# check if a staff's employer exists
def query_staff_employer(EMPLOYER: str, mysql) -> bool:
    sql = f'''
    SELECT *
    FROM airline
    WHERE name = '{EMPLOYER}';
    '''
    employer_exists = exec_sql(sql, mysql)
    if employer_exists:
        return True
    return False


# create a staff account
def create_staff_account(USERNAME: str, PASSWORD: str, FNAME: str,
                         LNAME: str, DOB: str, EMPLOYER: str, mysql) -> None:
    ENCRYPTED_PASSWORD = encrypt_password(PASSWORD)
    sql = f'''
    INSERT INTO airline_staff
    VALUES ('{USERNAME}','{ENCRYPTED_PASSWORD}','{FNAME}',
        '{LNAME}','{DOB}','{EMPLOYER}');
    '''
    exec_sql(sql, mysql, commit=True)


# *********************
# CUSTOMER REGISTRATION
# *********************

# check if a customer's email exists
def query_customer_email(EMAIL: str, mysql) -> bool:
    sql = f'''
    SELECT *
    FROM customer
    WHERE email = '{EMAIL}';
    '''

    account_exists = exec_sql(sql, mysql)
    if account_exists:
        return True
    return False


# create a customer account
def create_customer_account(EMAIL: str, NAME: str, PASSWORD: str, BUILDING_NUM: str, CITY: str, STATE: str,
                            STREET: str, PP_COUNTRY: str, PP_NUM: str, PP_EXPR: str, DOB: str,
                            PHONE_NUM: str, mysql) -> None:
    ENCRYPTED_PASSWORD = encrypt_password(PASSWORD)
    sql = f'''
    INSERT INTO customer
    VALUES ('{EMAIL}','{NAME}','{ENCRYPTED_PASSWORD}','{BUILDING_NUM}','{CITY}','{STATE}',
            '{STREET}','{PP_COUNTRY}','{PP_NUM}','{PP_EXPR}','{DOB}','{PHONE_NUM}');
    '''
    exec_sql(sql, mysql, commit=True)


