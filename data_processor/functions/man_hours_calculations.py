"""
Man hour calculation functions are in this file
"""

from get_data.models import RawClockData
from datetime import timedelta
import re
from django.utils import timezone
from decimal import Decimal
from decimal import getcontext

LOCAL_TIME_ZONE = ''
REGEX_FOR_DEPT = {
    'shift': "/([1-9])/"
}

DEPARTMENT_LOOKUP_DICT = {
    '1': 'CIW',
    '2': 'FCB',
    '3': 'PNT',
    '4': 'PCH',
    '5': 'FCH',
    '6': 'DAC',
    '7': 'MAINT',
    '8': 'QA',
    '9': 'MAT',
}


def get_clocked_in(start):
    """
    Filters employees who clocked in before shift time, excluding those who have clocked out from previous shifts
    :param start: datetime object the start of time that you want to look at
    :return: filtered objects before the start value
    """
    print('/*' * 50)
    print("GET CLOCKED IN")
    print('/*' * 50)
    with timezone.override("US/Eastern"):
        return RawClockData.objects.filter(
            PNCHEVNT_IN__year=start.year,
            PNCHEVNT_IN__month=start.month,
            PNCHEVNT_IN__day=start.day,
            PNCHEVNT_OUT__exact=None,
        ).exclude(end_rsn_txt__exact='&out')


def get_emp_who_left_during_shift(start, stop):
    """
    Filters employees who clocked out before the stop
    :param start: datetime object the start of time that you want to look at
    :param stop: datetime object the end of time that you want to look at
    :return: filtered objects within the start and stop range
    """

    with timezone.override("US/Eastern"):
        present_today = RawClockData.objects.filter(
            PNCHEVNT_IN__year=start.year,
            PNCHEVNT_IN__month=start.month,
            PNCHEVNT_IN__day=start.day,
        )

        left_for_day = present_today.filter(
            PNCHEVNT_OUT__lte=stop,
            end_rsn_txt__exact='&out',
        ).exclude(PNCHEVNT_OUT__lte=start)

        print("LEFT FOR DAY= ", len(left_for_day))

        return left_for_day


def get_emp_who_left_on_break(start, stop):
    """
    Filters employees who clocked out before the stop
    :param start: datetime object the start of time that you want to look at
    :param stop: datetime object the end of time that you want to look at
    :return: filtered objects within the start and stop range
    """

    with timezone.override("US/Eastern"):
        present_today = RawClockData.objects.filter(
            PNCHEVNT_IN__year=start.year,
            PNCHEVNT_IN__month=start.month,
            PNCHEVNT_IN__day=start.day,
        )

        went_on_break = present_today.filter(
            PNCHEVNT_OUT__lte=stop,
            end_rsn_txt__exact='&break',
        ).exclude(PNCHEVNT_OUT__lte=start)

        return went_on_break


def get_emp_shift(dept_string):
    """
    Regex lookup command to find which shift the employee is in
    :param dept_string: expects a string from column HM_LBRACCT_FULL_NAM that looks like '017.30000.00.51.05/1/-/017.P000051/-/-/-'
    :return: a string of shift containing shift number
    """
    try:
        regex_compiled = re.compile(REGEX_FOR_DEPT['shift'])
        shift = re.findall(regex_compiled, dept_string)[0]
    except ValueError:
        print('/*' * 50)
        print("REGEX ERROR FOR DEPT CODE <GET SHIFT in MAN_HOUR>")
        print("WAS GIVEN ", dept_string)
        print('/*' * 50)
        shift = 0

    # catching null values as a jic scenario
    if shift == '':
        shift = 0

    return shift


def get_emp_dept(dept_string):
    """
    Analyzes which department, plant, and shift that employee belongs too.
    :param dept_string: expects a string from column HM_LBRACCT_FULL_NAM that looks like '017.30000.00.51.05/1/-/017.P000051/-/-/-'
    :return: emp_dept as string of 3 letter code, i.e. 'CIW'/'FCB'
    """
    emp_dept_code = dept_string[4:5]

    if emp_dept_code in DEPARTMENT_LOOKUP_DICT:
        emp_dept = DEPARTMENT_LOOKUP_DICT[emp_dept_code]
    else:
        emp_dept = 'OTHER'

    return emp_dept


def get_emp_plant_code(dept_string):
    """
    :param dept_string: expects a string from column HM_LBRACCT_FULL_NAM that looks like '017.30000.00.51.05/1/-/017.P000051/-/-/-'
    :return: Returns string of plant code for employee
    """
    return dept_string[:3]


def get_emp_man_hours(employee, start, stop):
    """
    Calculates the employee's man hours from start to stop.
    :param employee: employee object
    :param start: DATETIME timezone aware object from the beginning of the snapshot
    :param stop: DATETIME timezone aware object from the ending of the snapshot
    :return: float of total employee mh
    """
    begin, end = set_begin_and_end_for_emp(employee, start, stop)
    emp_man_hours = ((end - begin).total_seconds()) / 3600
    return emp_man_hours


def set_begin_and_end_for_emp(employee, start, stop):
    """
    takes in the employee and computes when the begin and stop times for
     the employee should be as employees clock in and out before/during shifts
    :param employee: employee object
    :param start: DATETIME timezone aware object from the start
    :param stop: DATETIME timezone aware object from the ending
    :return: the begin and ending results as DATETIME timezone aware objects
    """
    # If before start, then capture start.
    begin = max(employee.PNCHEVNT_IN, start)
    if employee.PNCHEVNT_OUT:
        end = min(employee.PNCHEVNT_OUT, stop)
    else:
        end = stop
    return begin, end
