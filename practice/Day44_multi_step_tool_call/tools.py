from datetime import datetime, timedelta


def get_time():

    return datetime.now().strftime(
        "%I:%M %p"
    )


def get_date():

    return datetime.now().strftime(
        "%d-%m-%Y"
    )


def get_tomorrow_date():

    tomorrow = datetime.now() + timedelta(days=1)

    return tomorrow.strftime(
        "%d-%m-%Y"
    )


def multiply(a, b):

    return a * b