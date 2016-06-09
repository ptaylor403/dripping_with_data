from get_data.models import RawPlantActivity, RawClockData
from .claims_calculations import *
from .man_hours_calculations import *


def get_hpv(by_dept_dict):
    """

    :param by_dept_dict: An instance of the master_by_dept_dictionary populated with mh, ne, and claim data
    :return:
    """

    #list to be used for key comparison to generate hpv only for these dept.
    dept_list = ['CIW', 'FCB', 'PNT', 'PCH', 'FCH', 'DAC', 'MAINT', 'QA', 'MAT', 'OTHER']

    plant_mh = 0
    plant_ne = 0
    plant_hpv = 0

    # calculating the HPV
    for key in by_dept_dict:
        if key in dept_list:
            if by_dept_dict['claims_for_range']:
                by_dept_dict[key]['hpv'] = by_dept_dict[key]['mh']/by_dept_dict['claims_for_range']
                plant_mh += by_dept_dict[key]['mh']
                plant_ne += by_dept_dict[key]['ne']
                plant_hpv += by_dept_dict[key]['hpv']
            else:
                by_dept_dict[key]['hpv'] = 0

    by_dept_dict['PLANT']['mh'] = plant_mh
    by_dept_dict['PLANT']['ne'] = plant_ne
    by_dept_dict['PLANT']['hpv'] = plant_hpv

    return by_dept_dict

