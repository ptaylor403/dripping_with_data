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


def get_dept_lookup_dict():
    dept_lookup_dict = {
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
    return dept_lookup_dict
