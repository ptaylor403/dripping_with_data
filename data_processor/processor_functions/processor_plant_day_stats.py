from plantsettings.models import PlantSetting
from api.models import HPVATM
from .processor_shift import get_day_start
from .processor_hpv_calc import calc_hpv


def get_plant_day_hpv(hpv_dict, now):
    """
    Calculates the HPV for the day by dividing shift manhours by the claims. If no claims, HPV is set to 0 to avoid a DivisionByZero error.

    :param hpv_dict: A dictionary object containing hpv, manhours, number clocked in by department as well as number of claims that shift.
    :param now: The simulated time - datetime object.
    :return: Float value - plant day HPV AND Integer - manhours AND Integer - claims.
    """
    print("/"*50)
    print("GET DAY STATS FUNCTION")
    print("/"*50)
    print("NOW ", now)

    # Find latest plant settings and the start of the day based on number of
    # shifts in settings and current time
    plant_settings = PlantSetting.objects.latest('timestamp')
    day_start = get_day_start(plant_settings, now)

    # Gets all api entries for the day.
    all_since_start = HPVATM.objects.filter(timestamp__gte=day_start)

    # Set the current shift values to the hpv_dict values
    cur_hpv = hpv_dict['plant_s_hpv']
    cur_mh = hpv_dict['plant_s_mh']
    cur_claims = hpv_dict['claims_for_range']

    # Calc hpv based on time and number of shifts
    if plant_settings.num_of_shifts == 3:
        hpv, mh, claims = get_three_shifts_plant_day_hpv(hpv_dict, all_since_start, cur_hpv, cur_mh, cur_claims)
    elif plant_settings.num_of_shifts == 2:
        hpv, mh, claims = get_two_shifts_plant_day_hpv(hpv_dict, all_since_start, cur_hpv, cur_mh, cur_claims)
    else:
        hpv, mh, claims = cur_hpv, cur_mh, cur_claims
    return hpv, mh, claims


def get_three_shifts_plant_day_hpv(hpv_dict, all_since_start, cur_hpv, cur_mh, cur_claims):
    """
    Calculates the HPV for the plant based on 3 shifts active in settings. Gets the final snapshots from previous shifts to add to the current shift values. HPV is calculated based on manhour and claim totals for the day so far.

    :param hpv_dict: A dictionary object containing hpv, manhours, number clocked in by department as well as number of claims that shift.
    :param all_since_start: Queryset object - API entries since the start of the day
    :param cur_hpv: shift hpv value for the department - float.
    :param cur_mh: shift manhours value for the department - integer.
    :param cur_claims: shift claims value - integer.
    :return: Float value - plant day HPV AND Integer - manhours AND Integer - claims.
    """
    if hpv_dict['shift'] == 3:
        return cur_hpv, cur_mh, cur_claims
    # If in a later shift, add previous shift info
    elif hpv_dict['shift'] == 1:
        last_shift = all_since_start.filter(shift=3).last()
        hpv, mh, claims = get_last_shift_plant_day_hpv(cur_hpv, cur_mh, cur_claims, last_shift)
    elif hpv_dict['shift'] == 2:
        s3 = all_since_start.filter(shift=3).last()
        s1 = all_since_start.filter(shift=1).last()
        hpv, mh, claims = get_three_shifts_plant_day_hpv_2nd_shift(s3, s1, cur_mh, cur_claims)

    return hpv, mh, claims


def get_three_shifts_plant_day_hpv_2nd_shift(s3, s1, cur_mh, cur_claims):
    """
    Calculates the HPV for the plant based on 3 shifts active in settings and "now" being in the second shift. Gets the final snapshots from previous shifts to add to the current shift values. HPV is calculated based on manhour and claim totals for the day so far.

    :param s3: HPVATM model instance - final entry for today's third shift.
    :param s1: HPVATM model instance - final entry for today's first shift. clocked in by department as well as number of claims that shift.
    :param cur_mh: shift manhours value for the department - integer.
    :param cur_claims: shift claims value - integer.
    :return: Float value - plant day HPV AND Integer - manhours AND Integer - claims.
    """
    # Check for missing api entries and calc with existing data
    if s3 is None:
        if s1 is None:
            mh = cur_mh
            claims = cur_claims
        else:
            mh = s1.PLANT_s_mh + cur_mh
            claims = s1.claims_s + cur_claims
    #already checked for
    elif s1 is None:
        mh = s3.PLANT_s_mh + cur_mh
        claims = s3.claims_s + cur_claims
    else:
        mh = s3.PLANT_s_mh + s1.PLANT_s_mh + cur_mh
        claims = s3.claims_s + s1.claims_s + cur_claims
    hpv = calc_hpv(mh, claims)

    return hpv, mh, claims


def get_two_shifts_plant_day_hpv(hpv_dict, all_since_start, cur_hpv, cur_mh, cur_claims):
    """
    Calculates the HPV for the plant based on 2 shifts active in settings. Gets the final snapshots from the previous shift to add to the current shift values. HPV is calculated based on manhour and claim totals for the day so far.

    :param hpv_dict: A dictionary object containing hpv, manhours, number clocked in by department as well as number of claims that shift.
    :param all_since_start: Queryset object - API entries since the start of the day
    :param cur_hpv: shift hpv value for the department - float.
    :param cur_mh: shift manhours value for the department - integer.
    :param cur_claims: shift claims value - integer.
    :return: Float value - plant day HPV AND Integer - manhours AND Integer - claims.
    """
    if hpv_dict['shift'] == 1:
        hpv, mh, claims = cur_hpv, cur_mh, cur_claims
    elif hpv_dict['shift'] == 2:
        last_shift = all_since_start.filter(shift=1).last()
        hpv, mh, claims = get_last_shift_plant_day_hpv(cur_hpv, cur_mh, cur_claims, last_shift)
    return hpv, mh, claims


def get_last_shift_plant_day_hpv(cur_hpv, cur_mh, cur_claims, last_shift):
    """
    Calculates the HPV for the department based on only 1 previous shift. Gets the final snapshots from the previous shift to add to the current shift values. HPV is calculated based on manhour and claim totals for the day so far.

    :param cur_hpv: shift hpv value for the department - float.
    :param cur_mh: shift manhours value for the department - integer.
    :param cur_claims: shift claims value - integer.
    :param last_shift: HPVATM model object - API entry for the previous shift.
    :return: Float value - department day HPV AND Integer - manhours.
    """
    if last_shift is None or last_shift.PLANT_s_mh is None:
        hpv = cur_hpv
        mh = cur_mh
        claims = cur_claims
    else:
        mh = float(last_shift.PLANT_s_mh) + cur_mh
        claims = last_shift.claims_s + cur_claims
        hpv = calc_hpv(mh, claims)
    return hpv, mh, claims
