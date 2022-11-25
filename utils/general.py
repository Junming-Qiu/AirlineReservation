import hashlib
import datetime
from flask_mysqldb import MySQL


#############################################################

# *******
# GENERAL
# *******


# TODO: Wrap SQL statement with Atomic Transaction
def sql_transaction_wrap(sql: str) -> str:
    wrap_tmp = f'''
    USE flight_app;
    
    {sql}
    '''
    #
    # START TRANSACTION
    #
    # {sql}
    #
    # if ....
    #     COMMIT;
    #
    # then ...
    #     ROLLBACK;
    # '''

    return wrap_tmp


# execute a sql statement
def exec_sql(sql: str, mysql) -> list:
    cur = mysql.connection.cursor()
    cur.execute(sql_transaction_wrap(sql))
    mysql.connection.commit()
    return cur.fetchall()


# returns an encrypted password
def encrypt_password(password: str) -> str:
    hash_object = hashlib.md5(password.encode())
    return hash_object.hexdigest()


def check_datetime_format(DATE: str) -> None:
    try:
        datetime.datetime.strptime(DATE, '%Y%m%d %H%M%S')
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
    print(f'MySQL: Query Staff Password {ENCRYPTED_PASSWORD}')
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


# ******************
# STAFF REGISTRATION
# ******************

# check if a staff's username exists
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
    exec_sql(sql, mysql)


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
    exec_sql(sql, mysql)


# Takes many works and checks that they are valid as a group
def parse_input(inputs: list[str], ispass=False) -> bool:
    print("parsing", inputs, ispass)
    alpha_lower = "abcdefghijklmnopqrstuvwxyz"
    alpha_upper = alpha_lower.capitalize()
    nums = "0123456789"
    restrict = ['\0', '\'', '\"', '\b', '\n', '\r', '\t', '\Z', '\\', '\%', '\_', \
        '?', '-', '(', ')', '{', '}', '[', ']']

    for word in inputs:
        if ispass:
            print("password", ' ' in word)
            if ' ' in word:
                print(f"failed to parse {word}")
                return False

            if len(word) <= 8:
                print(f"failed to parse {word}")
                return False

        for c in word:
            if c not in alpha_lower and c not in alpha_upper and c not in nums and c in restrict:
                print(f"failed to parse {word}")
                return False
    return True