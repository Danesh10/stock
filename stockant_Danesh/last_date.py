from datetime import *
from dateutil import relativedelta

today = date.today()


def LastFriday():

    last_day_of_month = today + relativedelta.relativedelta(months=1, day=1) - timedelta(days=1)

    week_num = last_day_of_month.weekday() + 1
    print(last_day_of_month)
    print(week_num)
    if week_num == 5:
        last_friday = last_day_of_month
    else:
        last_friday = (last_day_of_month - timedelta(days=week_num + 2))
    return last_friday


def get_quarter(date):
    return (date.month - 1) // 3 + 1


def get_last_friday_of_the_quarter(date):
    quarter = get_quarter(date)
    last_day_of_the_quarter = datetime(date.year + 3 * quarter // 12, 3 * quarter % 12 + 1, 1) + timedelta(days=-1)
    week_num = last_day_of_the_quarter.weekday() + 1
    if week_num == 5:
        last_friday = last_day_of_the_quarter
    else:
        last_friday = (last_day_of_the_quarter - timedelta(days=week_num + 2))
    return last_friday


print(today)
