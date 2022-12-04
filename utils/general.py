import hashlib
import datetime

'''

General purpose functions.





'''



# execute a sql statement, return a tuple of tuples corresponding to rows in a table
def exec_sql(sql: str, mysql, commit=False) -> tuple:
    cur = mysql.connection.cursor()
    print(f'''
    EXECUTING QUERY:
    {sql}''')
    cur.execute(sql)
    if commit:
        mysql.connection.commit()
    raw_data=cur.fetchall()
    # print(raw_data)
    # return _clean_rtn(raw_data)
    return raw_data

# returns an encrypted password
def encrypt_password(password: str) -> str:
    hash_object = hashlib.md5(password.encode())
    return hash_object.hexdigest()

# return the date X days from today
def date_in_X_days(NUM_DAYS: int) -> str:
    '''
    :param NUM_DAYS: number of days different from current datetime
    :return: 'YYYY-MM-DD'
    '''
    today_plus_X = str(datetime.date.today() + datetime.timedelta(days=NUM_DAYS))
    return today_plus_X

def datetime_in_X_days(NUM_DAYS: int) -> str:
    '''
    :param NUM_DAYS: number of days different from current datetime
    :return: 'YYYY-MM-DD HH:MM:SS'
    '''
    today_plus_X = str(datetime.datetime.today() + datetime.timedelta(days=NUM_DAYS))[0:-7]
    return today_plus_X


def check_datetime_format(DATETIME: str) -> bool:
    if DATETIME is None:
        return True

    try:
        datetime.datetime.strptime(DATETIME, '%Y-%m-%d %H:%M:%S')
        return True
    except:
        return False


def check_date_format(DATE: str) -> bool:
    if DATE is None:
        return True

    try:
        datetime.datetime.strptime(DATE, '%Y-%m-%d')
        return True
    except:
        return False



# Takes many works and checks that they are valid as a group
def parse_input(inputs: list[str], ispass=False) -> bool:
    print("parsing", inputs, ispass)
    alpha_lower = "abcdefghijklmnopqrstuvwxyz"
    alpha_upper = alpha_lower.capitalize()
    nums = "0123456789"
    whitelist = ['-']
    restrict = ['\0', '\'', '\"', '\b', '\n', '\r', '\t', '\Z', '\\', '\%', '\_', \
        '?', '(', ')', '{', '}', '[', ']']

    for word in inputs:
        if word is None: # added this for optional params w/o input
            continue

        if ispass:
            print("password", ' ' in word)
            if ' ' in word:
                print(f"a. failed to parse {word}")
                return False

            if len(word) <= 8:
                print(f"b. failed to parse {word}")
                return False

        for c in word:
            if c not in alpha_lower and c not in alpha_upper and c not in nums and c not in whitelist and c in restrict:
                print(f"c. failed to parse {c} in {word}", c not in alpha_lower, c not in alpha_upper, c not in nums, c not in whitelist, c in restrict)
                return False
    print(f'Successfully parsed: {inputs}')
    return True

# increment month in datetime object
def increment_dt_month(dt: str) -> str:
    if dt.month < 12:
        dt = dt.replace(month=(dt.month + 1))
    else:
        dt = dt.replace(month=1, year=(dt.year + 1))
    return dt
