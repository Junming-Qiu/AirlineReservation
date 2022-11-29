import hashlib
import datetime

'''

General purpose functions.





'''

# DO NOT CALL OUTSIDE exec_sql()
def _clean_rtn(rtn: tuple) -> tuple:
    cleaned=[]
    for t in rtn:
        cleaned.append(tuple([t[i] for i in range(len(t-1))]))
    return tuple(cleaned)


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


# make sure that datetime is in a MYSQL-friendly format
def check_datetime_format(DATE: str) -> None: # TODO : make sure all date times are okay
    try:
        datetime.datetime.strptime(DATE, '%Y%m%d %H%M%S')
    except ValueError:
        raise ValueError(f'Incorrect date format {DATE}, must be YYYYMMDD HHMMSS')

# return the date X days from today
def date_in_X_days(NUM_DAYS: int) -> str:
    today_plus_X = str(datetime.date.today() + datetime.timedelta(days=NUM_DAYS))
    time_str = today_plus_X[0:4] + today_plus_X[5:7] + today_plus_X[8:10] #+ ' 000000' # TODO: fix this formatting
    #check_datetime_format(time_str) # TODO: fix this formatting
    return time_str

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