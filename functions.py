import hashlib
import datetime


#############################################################

# *******
# GENERAL
# *******


# TODO: Wrap SQL statement with Atomic Transaction
def sql_transaction_wrap(sql: str) -> str:
    wrap = f'''
    USE flight_app;

    START TRANSACTION

    {sql}

    if ....
        COMMIT;

    then ... 
        ROLLBACK;
    '''

    return sql


# execute a sql statement
def exec_sql(sql: str) -> list:
    cur = mysql.connection.cursor()
    cur.execute(sql_transaction_wrap(str))
    return cur.fetchall()


# returns an encrypted password
def encrypt_password(password: str) -> str:
    hash_object = hashlib.md5(password.encode())
    return hash_object.hexdigest()


def check_datetime_format(DATE: str) -> None:
    try:
        datetime.datetime.strptime(DATE, '%Y%m%d')
    except ValueError:
        raise ValueError(f'Incorrect date format {DATE}, must be YYYYMMDD')


def date_in_X_days(NUM_DAYS: int) -> str:
    today_plus_X = str(datetime.date.today() + datetime.timedelta(days=NUM_DAYS))
    time_str = today_plus_X[0:4] + today_plus_X[5:7] + today_plus_X[8:10]
    check_datetime_format(time_str)
    return time_str


# ******
# LOG IN
# ******

# check if a staff's log in credentials exists
def query_staff_credentials(USERNAME: str, PASSWORD: str) -> list:
    ENCRYPTED_PASSWORD = encrypt_password(PASSWORD)
    sql = f'''
        SELECT *
        FROM airline_staff
        WHERE username = '{USERNAME}'
            AND password = '{ENCRYPTED_PASSWORD}';
        '''
    return exec_sql(sql)


# check if a customer's log in credentials exists
def query_customer_credentials(EMAIL: str, PASSWORD: str) -> list:
    ENCRYPTED_PASSWORD = encrypt_password(PASSWORD)
    sql = f'''
        SELECT *
        FROM customer
        WHERE email = '{EMAIL}'
            AND password = '{ENCRYPTED_PASSWORD}';
        '''
    return exec_sql(sql)


# ******************
# STAFF REGISTRATION
# ******************

# check if a staff's username exists
def query_staff_username(USERNAME: str) -> bool:
    sql = f'''
    SELECT *
    FROM airline_staff
    WHERE username = '{USERNAME}';
    '''
    username_exists = exec_sql(sql)
    if username_exists:
        return True
    return False


# check if a staff's employer exists
def query_staff_employer(EMPLOYER: str) -> bool:
    sql = f'''
    SELECT *
    FROM airline
    WHERE name = '{EMPLOYER}';
    '''
    employer_exists = exec_sql(sql)
    if employer_exists:
        return True
    return False


# create a staff account
def create_staff_account(USERNAME: str, PASSWORD: str, FNAME: str,
                         LNAME: str, DOB: str, EMPLOYER: str) -> None:
    ENCRYPTED_PASSWORD = encrypt_password(PASSWORD)
    sql = f'''
    INSERT INTO airline_staff
    VALUES ('{USERNAME}','{ENCRYPTED_PASSWORD}','{FNAME}',
        '{LNAME}','{DOB}','{EMPLOYER}');
    '''
    exec_sql(sql)


# *********************
# CUSTOMER REGISTRATION
# *********************

# check if a customer's email exists
def query_customer_email(EMAIL: str) -> bool:
    sql = f'''
    SELECT *
    FROM customer
    WHERE email = '{EMAIL}';
    '''

    account_exists = exec_sql(sql)
    if account_exists:
        return True
    return False


# create a customer account
def create_customer_account(EMAIL: str, NAME: str, PASSWORD: str, BUILDING_NUM: str, CITY: str, STATE: str,
                            STREET: str, PP_COUNTRY: str, PP_NUM: str, PP_EXPR: str, DOB: str,
                            PHONE_NUM: str, ) -> None:
    ENCRYPTED_PASSWORD = encrypt_password(PASSWORD)
    sql = f'''
    INSERT INTO customer
    VALUES ('{EMAIL}','{NAME}','{ENCRYPTED_PASSWORD}','{BUILDING_NUM}','{CITY}','{STATE}',
            '{STREET}','{PP_COUNTRY}','{PP_NUM}','{PP_EXPR}','{DOB}','{PHONE_NUM}');
    '''
    exec_sql(sql)

