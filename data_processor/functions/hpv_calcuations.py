from get_data.models import RawPlantActivity, RawClockData
from .claims_calculations import *
from .man_hours_calculations import *


def get_hpv(by_dept_dict):
    """
    :param by_dept_dict: An instance of the master_by_dept_dictionary populated with mh, ne, and claim data
    :return:
    """
    print("/"*50)
    print("GET HPV IN HPV CALC")
    print("/"*50)
    # list to be used for key comparison to generate hpv only for these dept.
    dept_list = ['CIW', 'FCB', 'PNT', 'PCH', 'FCH', 'DAC', 'MAINT', 'QA', 'MAT', 'OTHER']

    plant_mh = 0
    plant_ne = 0
    plant_hpv = 0

    # calculating the HPV
    for key in by_dept_dict:
        plant_hpv, plant_mh, plant_ne = update_dept_vars(by_dept_dict, dept_list, key, plant_hpv, plant_mh, plant_ne)

    plant = by_dept_dict['PLANT']
    plant['mh'] = plant_mh
    plant['ne'] = plant_ne
    plant['hpv'] = plant_hpv

    return by_dept_dict


def update_dept_vars(by_dept_dict, dept_list, key, plant_hpv, plant_mh, plant_ne):
    if key in dept_list:
        dept = by_dept_dict[key]
        plant_mh += dept['mh']
        plant_ne += dept['ne']

        # If claims is not 0, do some division, else hpv = 0
        claims = by_dept_dict['claims_for_range']
        if claims:
            dept['hpv'] = dept['mh'] / claims
            plant_hpv += dept['hpv']
        else:
            dept['hpv'] = 0
    return plant_hpv, plant_mh, plant_ne
