from plantsettings.models import PlantSetting
from api.models import HPVATM
from .processor_shift import get_day_start


def get_dept_day_stats(hpv_dict, now, dept):
    """
    Calculates the HPV for the current shift by dividing shift manhours by the claims. If no claims, HPV is set to 0 to avoid a DivisionByZero error.

    :param hpv_dict: A dictionary object containing hpv, manhours, number clocked in by department as well as number of claims that shift.
    :param now: The simulated time - datetime object.
    :param dept: The department to calculate for - string.
    :return: Float value - plant shift HPV.
    """
    # Find start of the current day
    plant_settings = PlantSetting.objects.latest('timestamp')
    day_start = get_day_start(plant_settings, now)

    # Get all API entries since the day start
    all_since_start = HPVATM.objects.filter(timestamp__gte=day_start)

    # Set the current hpv, manhours, and claims to dictionary values
    cur_hpv = hpv_dict[dept]['hpv']
    cur_mh = hpv_dict[dept]['mh']
    cur_claims = hpv_dict['claims_for_range']

    # Checks number of shifts to know how many to look for when calculating
    # day totals in later shifts.
    if plant_settings.num_of_shifts == 3:
        hpv, mh = get_three_shifts_dept_day_hpv(hpv_dict, dept, all_since_start, cur_hpv, cur_mh, cur_claims)
    elif plant_settings.num_of_shifts == 2:
        hpv, mh = get_two_shifts_dept_day_hpv(hpv_dict, dept, all_since_start, cur_hpv, cur_mh, cur_claims)
    else:
        hpv, mh = cur_hpv, cur_mh
    return hpv, mh


def get_three_shifts_dept_day_hpv(hpv_dict, dept, all_since_start, cur_hpv, cur_mh, cur_claims):
    """
    Calculates the HPV for the department based on 3 shifts active in settings. Gets the final snapshots from previous shifts to add to the current shift values. HPV is calculated based on manhour and and claim totals for the day so far.

    :param hpv_dict: A dictionary object containing hpv, manhours, number clocked in by department as well as number of claims that shift.
    :param dept: The department to calculate for - string.
    :param all_since_start: Queryset object - API entries since the start of the day
    :param cur_hpv: shift hpv value for the department - float.
    :param cur_mh: shift manhours value for the department - integer.
    :param cur_claims: shift claims value - integer.
    :return: Float value - plant shift HPV.
    """
    if hpv_dict['shift'] == 3:
        hpv, mh =  cur_hpv, cur_mh
    # If we are in a later shift, add previous shift values to current
    elif hpv_dict['shift'] == 1:
        last_shift = all_since_start.filter(shift=3).last()
        hpv, mh = get_last_shift_dept_day_hpv(dept, cur_mh, cur_claims, last_shift)
    elif hpv_dict['shift'] == 2:
        hpv, mh = get_last_two_shifts_dept_day_hpv(dept, all_since_start, cur_mh, cur_claims)

    return hpv, mh


def get_last_shift_dept_day_hpv(dept, cur_mh, cur_claims, last_shift):
    """
    Calculates the HPV for the department based on only 1 previous shift. Gets the final snapshots from the previous shift to add to the current shift values. HPV is calculated based on manhour and and claim totals for the day so far.

    :param dept: The department to calculate for - string.
    :param cur_mh: shift manhours value for the department - integer.
    :param cur_claims: shift claims value - integer.
    :param last_shift: HPVATM model object - API entry for the previous shift.
    :return: Float value - plant shift HPV.
    """
    # If no previous entries, day totals are equal to shift totals
    if last_shift is None:
        mh = cur_mh
        claims = cur_claims
    # If previous shifts, add to current
    else:
        mh = float(getattr(last_shift, '{}_s_mh'.format(dept))) + cur_mh
        claims = last_shift.claims_s + cur_claims
    hpv = calc_hpv(mh, claims)
    return hpv, mh

def get_last_two_shifts_dept_day_hpv(dept, all_since_start, cur_mh, cur_claims):
    """
    Returns the total hpv for the day when there are 2 shifts before the current time to check. Checks for and handles missing entries for either previous shift.

    :param dept: The department to calculate for - string.
    :param all_since_start: HPVATM queryset object - API entries for the current day.
    :param cur_mh: shift manhours value for the department - integer.
    :param cur_claims: shift claims value - integer.
    :return: Float value - plant shift HPV AND Integer for manhours.
    """
    # Get the last entries for each previous shift.
    s3 = all_since_start.filter(shift=3).last()
    s1 = all_since_start.filter(shift=1).last()

    # If missing a shift, send to other functions to calculate.
    if s3 is None:
        mh, claims = get_last_two_shifts_dept_day_hpv_missing_shift_three(dept, s1, cur_mh, cur_claims)
    elif s1 is None:
        mh, claims = get_last_two_shifts_dept_day_hpv_missing_shift_one(dept, s3, cur_mh, cur_claims)
    else:
        mh = float(getattr(s3, '{}_s_mh'.format(dept))) + float(getattr(s1, '{}_s_mh'.format(dept))) + cur_mh
        claims = s3.claims_s + s1.claims_s + cur_claims
    hpv = calc_hpv(mh, claims)
    return hpv, mh


def get_last_two_shifts_dept_day_hpv_missing_shift_three(dept, s1, cur_mh, cur_claims):
    if s1 is None:
        mh = cur_mh
        claims = cur_claims
    else:
        mh = float(getattr(s1, '{}_s_mh'.format(dept))) + cur_mh
        claims = s1.claims_s + cur_claims
    return mh, claims


def get_last_two_shifts_dept_day_hpv_missing_shift_one(dept, s3, cur_mh, cur_claims):
    mh = float(getattr(s3, '{}_s_mh'.format(dept))) + cur_mh
    claims = s3.claims_s + cur_claims
    if s3 is None:
        mh = cur_mh
        claims = cur_claims
    return mh, claims


def get_two_shifts_dept_day_hpv(hpv_dict, dept, all_since_start, cur_hpv, cur_mh, cur_claims):
    if hpv_dict['shift'] == 1:
        hpv, mh = cur_hpv, cur_mh
    elif hpv_dict['shift'] == 2:
        last_shift = all_since_start.filter(shift=1).last()
        hpv, mh = get_last_shift_dept_day_hpv(dept, cur_mh, cur_claims, last_shift)
    return hpv, mh
