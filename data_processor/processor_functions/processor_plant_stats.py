def get_plant_stats(hpv_dict, dept_list):
    """
    Loops through department info in hpv_dict to get plant totals.

    :param hpv_dict: A dictionary object containing hpv, manhours, number clocked in by department and total for the plant as well as number of claims that shift.
    :param dept_list: Array of strings - department labels.
    :return: Integer values - plant manhours AND plant total clocked in employees.
    """
    plant_s_ne = 0
    plant_s_mh = 0
    for dept in dept_list:
        plant_s_mh += hpv_dict[dept]['mh']
        plant_s_ne += hpv_dict[dept]['ne']
    return plant_s_mh, plant_s_ne


def calc_plant_hpv_for_shift(hpv_dict, plant_s_mh):
    """
    Calculates the HPV for the current shift by dividing shift manhours by the claims. If no claims, HPV is set to 0 to avoid a DivisionByZero error.

    :param hpv_dict: A dictionary object containing hpv, manhours, number clocked in by department and total for the plant as well as number of claims that shift.
    :param plant_s_mh: Integer value - plant manhours for the shift.
    :return: Float value - plant shift HPV.
    """
    if hpv_dict['claims_for_range'] == 0 or hpv_dict is None:
        plant_s_hpv = 0
    else:
        plant_s_hpv = plant_s_mh / hpv_dict['claims_for_range']
    return plant_s_hpv
