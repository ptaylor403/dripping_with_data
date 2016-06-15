from .processor_plant_stats import get_plant_stats, calc_plant_hpv_for_shift
from .processor_dept_day_stats import get_dept_day_stats
from .processor_plant_day_stats import get_plant_day_hpv

from django.utils import timezone


def get_day_hpv_dict(hpv_dict, now):
    """
    Calculates the day total hpv and manhours based on current values since shift start and adding these to the last recorded value of the any previous shifts if applicable.

    :param hpv_dict: A dictionary object containing hpv, manhours, number clocked in by department as well as number of claims that shift.
    :param now: The simulated time - datetime object.
    :return: Dictionary object to be written to the api.
    """
    print("/"*50)
    print("GET DAY HPV DICT FUNCTION")
    print("/"*50)

    # Department list to loop through
    dept_list = ['CIW', 'FCB', 'PNT', 'PCH', 'FCH', 'DAC', 'MAINT', 'QA', 'MAT', 'OTHER']
    dept_values = []
    full_dict = {}

    # Adds dept shift values for manhours and number in to get plant shift info
    plant_s_mh, plant_s_ne = get_plant_stats(hpv_dict, dept_list)
    # HPV calculated based on manhours/claims
    plant_s_hpv = calc_plant_hpv_for_shift(hpv_dict, plant_s_mh)


    # Calculates the stats for the day by department.
    for dept in dept_list:
        dept_values.append(get_dept_day_stats(hpv_dict, now, dept))

    print("DEPT_VALUES ",dept_values)

    # Dictionary to update 2 others with plant data.
    shift_dict = {
        'plant_s_hpv': plant_s_hpv,
        'plant_s_mh': plant_s_mh,
        'plant_s_ne': plant_s_ne,
    }

    # HPV dict updated to calc plant day totals further on.
    hpv_dict.update(shift_dict)
    # Adds to dictionary that will be returned
    full_dict.update(shift_dict)
    print('FULL DICT:', full_dict)

    #Calculates the day totals for the plant
    plant_d_hpv, plant_d_mh, claims_d = get_plant_day_hpv(hpv_dict, now)
    print("plant_d_hpv, plant_d_mh, claims_d= ", plant_d_hpv, plant_d_mh, claims_d)

    # Fills the dictionary that will be written to API
    full_hpv_dict = {
        'CIW_s_hpv': hpv_dict['CIW']['hpv'],
        'CIW_s_mh': hpv_dict['CIW']['mh'],
        'CIW_s_ne': hpv_dict['CIW']['ne'],
        'CIW_d_hpv': dept_values[0][0],
        'CIW_d_mh': dept_values[0][1],
        'FCB_s_hpv': hpv_dict['FCB']['hpv'],
        'FCB_s_mh': hpv_dict['FCB']['mh'],
        'FCB_s_ne': hpv_dict['FCB']['ne'],
        'FCB_d_hpv': dept_values[1][0],
        'FCB_d_mh': dept_values[1][1],
        'PNT_s_hpv': hpv_dict['PNT']['hpv'],
        'PNT_s_mh': hpv_dict['PNT']['mh'],
        'PNT_s_ne': hpv_dict['PNT']['ne'],
        'PNT_d_hpv': dept_values[2][0],
        'PNT_d_mh': dept_values[2][1],
        'PCH_s_hpv': hpv_dict['PCH']['hpv'],
        'PCH_s_mh': hpv_dict['PCH']['mh'],
        'PCH_s_ne': hpv_dict['PCH']['ne'],
        'PCH_d_hpv': dept_values[3][0],
        'PCH_d_mh': dept_values[3][1],
        'FCH_s_hpv': hpv_dict['FCH']['hpv'],
        'FCH_s_mh': hpv_dict['FCH']['mh'],
        'FCH_s_ne': hpv_dict['FCH']['ne'],
        'FCH_d_hpv': dept_values[4][0],
        'FCH_d_mh': dept_values[4][1],
        'DAC_s_hpv': hpv_dict['DAC']['hpv'],
        'DAC_s_mh': hpv_dict['DAC']['mh'],
        'DAC_s_ne': hpv_dict['DAC']['ne'],
        'DAC_d_hpv': dept_values[5][0],
        'DAC_d_mh': dept_values[5][1],
        'MAINT_s_hpv': hpv_dict['MAINT']['hpv'],
        'MAINT_s_mh': hpv_dict['MAINT']['mh'],
        'MAINT_s_ne': hpv_dict['MAINT']['ne'],
        'MAINT_d_hpv': dept_values[6][0],
        'MAINT_d_mh': dept_values[6][1],
        'QA_s_hpv': hpv_dict['QA']['hpv'],
        'QA_s_mh': hpv_dict['QA']['mh'],
        'QA_s_ne': hpv_dict['QA']['ne'],
        'QA_d_hpv': dept_values[7][0],
        'QA_d_mh': dept_values[7][1],
        'MAT_s_hpv': hpv_dict['MAT']['hpv'],
        'MAT_s_mh': hpv_dict['MAT']['mh'],
        'MAT_s_ne': hpv_dict['MAT']['ne'],
        'MAT_d_hpv': dept_values[8][0],
        'MAT_d_mh': dept_values[8][1],
        'OTHER_s_hpv': hpv_dict['OTHER']['hpv'],
        'OTHER_s_mh': hpv_dict['OTHER']['mh'],
        'OTHER_s_ne': hpv_dict['OTHER']['ne'],
        'OTHER_d_hpv': dept_values[9][0],
        'OTHER_d_mh': dept_values[9][1],

        'PLANT_d_hpv': plant_d_hpv,
        'PLANT_d_mh': plant_d_mh,
        'PLANT_s_hpv': plant_s_hpv,
        'PLANT_s_ne': plant_s_ne,
        'PLANT_s_mh': plant_s_mh,

        'claims_s': hpv_dict['claims_for_range'],
        'claims_d': claims_d,

        'shift': hpv_dict['shift'],
        'timestamp': timezone.localtime(now),
    }

    print("FULL DICT ", full_hpv_dict)
    return full_hpv_dict
