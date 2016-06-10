from datetime import datetime, timedelta
from django.utils import timezone

from .claims_calculations import get_range_of_claims
from .man_hours_calculations import get_emp_man_hours, get_emp_dept, get_clocked_in
from .hpv_calcuations import get_hpv

from generic_dripper.views import the_dripper


def get_now():
    return the_dripper.simulated_time

def get_master_by_dept_dict():
    """
    made this for readability purposes and to have
    one version of the truth for this dict.
    :return: RETURNS a zero'd out dict with lists in it.
    The first items in the list are as follows, in order:
    'mh' = man hours for that dept
    'ne' = number of employees for clocked in
    'hpv' = hours per vehicle
    """
    master_by_dept_dict = {
        'CIW': {
            'mh': 0,
            'ne': 0,
            'hpv': 0,
        },
        'FCB': {
            'mh': 0,
            'ne': 0,
            'hpv': 0,
        },
        'PNT': {
            'mh': 0,
            'ne': 0,
            'hpv': 0,
        },
        'PCH': {
            'mh': 0,
            'ne': 0,
            'hpv': 0,
        },
        'FCH': {
            'mh': 0,
            'ne': 0,
            'hpv': 0,
        },
        'DAC': {
            'mh': 0,
            'ne': 0,
            'hpv': 0,
        },
        'MAINT': {
            'mh': 0,
            'ne': 0,
            'hpv': 0,
        },
        'QA': {
            'mh': 0,
            'ne': 0,
            'hpv': 0,
        },
        'MAT': {
            'mh': 0,
            'ne': 0,
            'hpv': 0,
        },
        'OTHER': {
            'mh': 0,
            'ne': 0,
            'hpv': 0,
        },
        'PLANT': {
            'mh': 0,
            'ne': 0,
            'hpv': 0,
        },
        'claims_for_range': 0
    }

    return master_by_dept_dict


def main(start, stop):
    """
    Main function that queries the DB to return HPV by dept.
    :param start: DATETIME TIMEZONE AWARE object
    :param shift: Which shift, string
    :return: completed_by_dept_dict that is based on master by dept dict fully calculated.
    """
    print("/"*50)
    print("PROCESS DATA MAIN FUNCTION")
    print("/"*50)

    # stop = timezone.now()
    # stop = get_now()
    print("START= ",start,"STOP =", stop)


    # create instance of master dept dict
    by_dept_dict = get_master_by_dept_dict()
    # populate claims for range
    by_dept_dict['claims_for_range'] = get_range_of_claims(start, stop)
    print("CLAIMS FOR RANGE: ", by_dept_dict['claims_for_range'])
    currently_clocked_in = get_clocked_in(start)

    print("CURRENTLY CLOCKED IN ",len(currently_clocked_in))
    for employee in currently_clocked_in:
        # getting emp's department
        emp_dept = get_emp_dept(employee.HM_LBRACCT_FULL_NAM)

        if emp_dept in by_dept_dict:
            by_dept_dict[emp_dept]['ne'] += 1
            by_dept_dict[emp_dept]['mh'] += get_emp_man_hours(employee, start, stop)

    completed_by_dept_dict = get_hpv(by_dept_dict)

    return completed_by_dept_dict