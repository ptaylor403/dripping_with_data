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
    return random.choice(['CIW', 'FCB', 'PCH', 'FCH', 'PNT'])


def get_truck_serial():
    serial = random.choice(['HX', 'HY', 'HV', 'JB']) + str(random.randint(3201, 8900))
    return serial


def get_completed(day, hour):
    minute = random.randint(0, 59)
    clock = datetime(2016, 6, day, hour, minute)
    return clock
