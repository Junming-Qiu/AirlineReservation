import datetime
from utils.general import *




def staff_view_mfc_pastmonth1() -> tuple:
    today = datetime.datetime.today()
    past_month = today.replace(month=(today.month-1))
    return (str(past_month)[0:-7], str(today)[0:-7])

print(staff_view_mfc_pastmonth1())


def check_datetime_format(DATE: str) -> None: # TODO : make sure all date times are okay
    try:
        datetime.datetime.strptime(DATE, '%Y%m%d %H%M%S')
    except ValueError:
        raise ValueError(f'Incorrect date format {DATE}, must be YYYYMMDD HHMMSS')

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

