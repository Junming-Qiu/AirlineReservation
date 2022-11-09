
def select_test() -> str:
    sql = '''
    SELECT *
    FROM flight
    WHERE flight_status = 'delayed' 
	OR flight_status = 'on time';
    '''

    return str(exec_sql(sql))

def insert_test() -> str:
    sql = '''
    INSERT INTO airline
    VALUES ('LATAM')
    '''
    exec_sql(sql)

    sql_2 = '''
    SELECT * 
    FROM airline;
    '''
    return str(exec_sql(sql_2))

def check_creds(USERNAME: str, PASSWORD: str, TABLE: str) -> bool:
    sql = f'''
        SELECT username, password
        FROM {TABLE}
        WHERE username = {USERNAME}
            AND password = {PASSWORD};
        '''
    return sql
    if exec_sql(sql):
        return True
    return False

username_invalid = '1'
password_invalid = '2'
username_valid = 'kbennit283'
password_valid = '2hB!-@Xkv-T(0l'
table = 'airline_staff'