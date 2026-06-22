from datetime import datetime


def get_time():

    return datetime.now().strftime(
        "%I:%M %p"
    )


def get_date():

    return datetime.now().strftime(
        "%d-%m-%Y"
    )


def multiply(
    a,
    b
):

    return a * b