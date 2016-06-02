import random
from datetime import datetime


def get_employee():
    return random.randint(64000, 64999)


def clock_in(day, hour):
    minute = random.randint(0, 29)
    clock = datetime(2016, 6, day, hour, minute)
    return clock


def clock_out(day, hour):
    clock = datetime(2016, 6, day, hour + 9, 0)
    return clock


def get_dept():
    return random.choice(['CIW', 'FCB', 'PCH', 'FCH'])


def gen_data():
    shift_starts = [6, 2]
    for day in range(1, 6):
        for hour in shift_starts:
            emp = get_employee()
            dept = get_dept()
            time_in = clock_in(day, hour)

            if day != 5:
                time_out = clock_out(day, hour)
            else:
                time_out = None
