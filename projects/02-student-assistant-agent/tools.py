from datetime import datetime
import time


def get_time():
    return datetime.now().strftime("%I:%M %p")


def get_date():
    return datetime.now().strftime("%d-%m-%Y")


def multiply(a, b):
    return a * b


def calculate_gpa(total_gp, total_courses):
    return round(total_gp / total_courses, 2)


def start_timer(seconds):
    time.sleep(seconds)
    return f"Timer finished: {seconds} seconds"