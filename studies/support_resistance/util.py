from datetime import datetime


def date_only(current_date):
    one_date = datetime(
        current_date.year, current_date.month, current_date.day)
    return one_date
