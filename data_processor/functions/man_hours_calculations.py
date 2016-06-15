"""
Man hour calculation functions are in this file
"""

from get_data.models import RawClockData
from datetime import timedelta
import re
from django.utils import timezone


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
    with timezone.override("US/Eastern"):
        return RawClockData.objects.filter(
            PNCHEVNT_IN__year=start.year,
            PNCHEVNT_IN__month=start.month,
            PNCHEVNT_IN__day=start.day,
            PNCHEVNT_OUT__exact=None,
        ).exclude(end_rsn_txt__exact='&out')


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
    :param employee_object:
    :param start: DATETIME object in UTC from the beginning of the snapshot
    :param stop: DATETIME object in UTC from the ending of the snapshot
    :return: float of total employee mh
    """

    # initializing man_hours
    man_hours_time_obj = timedelta(hours=0)
    # print("Punch event: ", employee.PNCHEVNT_IN)
    # print("Event TZ:", employee.PNCHEVNT_IN.tzinfo)

    # catching if employee came in late or before start.
    # If before start, then capture start.
    begin = max(employee.PNCHEVNT_IN, start)
    # print("Begin: ", begin)
    man_hours_time_obj += stop - begin
    man_seconds = man_hours_time_obj.total_seconds()
    total_man_hours = man_seconds / 3600

    return total_man_hours
