from django.utils import timezone
import datetime as dt

"""
API entries
"""
#First shift at 7:45 with normal data.
reg_first_shift_api_entry = {
    'CIW_s_hpv': 7.3,
    'CIW_s_mh': 101.5,
    'CIW_s_ne': 71,
    'CIW_d_hpv': 7.3,
    'CIW_d_mh': 101.5,
    'FCB_s_hpv': 5,
    'FCB_s_mh': 93,
    'FCB_s_ne': 62,
    'FCB_d_hpv': 5,
    'FCB_d_mh': 93,
    'PNT_s_hpv': 6.6,
    'PNT_s_mh': 63,
    'PNT_s_ne': 42,
    'PNT_d_hpv': 6.6,
    'PNT_d_mh': 63,
    'PCH_s_hpv': 14.1,
    'PCH_s_mh': 198,
    'PCH_s_ne': 132,
    'PCH_d_hpv': 14.1,
    'PCH_d_mh': 198,
    'FCH_s_hpv':  10.1,
    'FCH_s_mh': 66,
    'FCH_s_ne': 30,
    'FCH_d_hpv': 10.1,
    'FCH_d_mh': 66,
    'DAC_s_hpv': 12.3,
    'DAC_s_mh': 50,
    'DAC_s_ne': 33,
    'DAC_d_hpv': 12.3,
    'DAC_d_mh': 50,
    'MAINT_s_hpv': 9,
    'MAINT_s_mh': 101,
    'MAINT_s_ne': 66,
    'MAINT_d_hpv': 9,
    'MAINT_d_mh': 101,
    'QA_s_hpv': 12.6,
    'QA_s_mh': 78,
    'QA_s_ne': 51,
    'QA_d_hpv': 12.6,
    'QA_d_mh': 78,
    'MAT_s_hpv': 7.1,
    'MAT_s_mh': 176,
    'MAT_s_ne': 118,
    'MAT_d_hpv': 7.1,
    'MAT_d_mh': 176,
    'OTHER_s_hpv': 0,
    'OTHER_s_mh': 0,
    'OTHER_s_ne': 0,
    'OTHER_d_hpv': 0,
    'OTHER_d_mh': 0,

    'PLANT_d_hpv': 84.1,
    'PLANT_d_mh': 926.5,
    'PLANT_s_hpv': 84.1,
    'PLANT_s_ne': 641,
    'PLANT_s_mh': 926.5,

    'claims_s': 14,
    'claims_d': 14,

    'shift': 1,
    'timestamp': timezone.make_aware(dt.datetime(2016, 6, 2, 7, 45)),
}


"""
Plant Settings
"""
default_plant_settings = {
    'timestamp': timezone.make_aware(dt.datetime(2016, 6, 2, 7, 0)),
    'plant_code': '017',
    'plant_target': 55,
    'num_of_shifts': 2,
    'first_shift': dt.time(6,30),
    'second_shift': dt.time(14,30),
    'third_shift': dt.time(22,30),
    'dripper_start': timezone.make_aware(dt.datetime(2016, 6, 2, 8, 0))
}

three_shift_8_am_plant_settings = {
    'timestamp': timezone.make_aware(dt.datetime(2016, 6, 2, 7, 0)),
    'plant_code': '017',
    'plant_target': 55,
    'num_of_shifts': 3,
    'first_shift': dt.time(6,30),
    'second_shift': dt.time(14,30),
    'third_shift': dt.time(22,30),
    'dripper_start': timezone.make_aware(dt.datetime(2016, 6, 2, 8, 0))
}

two_shift_8_am_plant_settings = {
    'timestamp': timezone.make_aware(dt.datetime(2016, 6, 2, 7, 0)),
    'plant_code': '017',
    'plant_target': 55,
    'num_of_shifts': 2,
    'first_shift': dt.time(6,30),
    'second_shift': dt.time(14,30),
    'third_shift': dt.time(22,30),
    'dripper_start': timezone.make_aware(dt.datetime(2016, 6, 2, 8, 0))
}

one_shift_8_am_plant_settings = {
    'timestamp': timezone.make_aware(dt.datetime(2016, 6, 2, 7, 0)),
    'plant_code': '017',
    'plant_target': 55,
    'num_of_shifts': 1,
    'first_shift': dt.time(6,30),
    'second_shift': dt.time(14,30),
    'third_shift': dt.time(22,30),
    'dripper_start': timezone.make_aware(dt.datetime(2016, 6, 2, 8, 0))
}


"""
HPV Dictionaries
"""
shift_1_hpv_dict = {'QA': {'ne': 10, 'hpv': 10, 'mh': 10}, 'claims_for_range': 10, 'MAINT': {'ne': 10, 'hpv': 10, 'mh': 10}, 'PNT': {'ne': 10, 'hpv': 10, 'mh': 10}, 'PCH': {'ne': 10, 'hpv': 10, 'mh': 10}, 'PLANT': {'ne': 10, 'hpv': 10, 'mh': 10}, 'shift': 10, 'FCB': {'ne': 10, 'hpv': 10, 'mh': 10}, 'CIW': {'ne': 10, 'hpv': 10, 'mh': 10}, 'DAC': {'ne': 10, 'hpv': 10, 'mh': 10}, 'OTHER': {'ne': 0, 'hpv': 0.0, 'mh': 0}, 'FCH': {'ne': 10, 'hpv': 10, 'mh': 10}, 'MAT': {'ne': 10, 'hpv': 10, 'mh': 10}}

shift_2_hpv_dict = {'QA': {'ne': 100, 'hpv': 100, 'mh': 100}, 'claims_for_range': 100, 'MAINT': {'ne': 100, 'hpv': 100, 'mh': 100}, 'PNT': {'ne': 100, 'hpv': 100, 'mh': 100}, 'PCH': {'ne': 100, 'hpv': 100, 'mh': 100}, 'PLANT': {'ne': 100, 'hpv': 100, 'mh': 100}, 'shift': 100, 'FCB': {'ne': 100, 'hpv': 100, 'mh': 100}, 'CIW': {'ne': 100, 'hpv': 100, 'mh': 100}, 'DAC': {'ne': 100, 'hpv': 100, 'mh': 100}, 'OTHER': {'ne': 0, 'hpv': 0.0, 'mh': 0}, 'FCH': {'ne': 100, 'hpv': 100, 'mh': 100}, 'MAT': {'ne': 100, 'hpv': 100, 'mh': 100}}

shift_3_hpv_dict = {'QA': {'ne': 1, 'hpv': 1, 'mh': 1}, 'claims_for_range': 1, 'MAINT': {'ne': 1, 'hpv': 1, 'mh': 1}, 'PNT': {'ne': 1, 'hpv': 1, 'mh': 1}, 'PCH': {'ne': 1, 'hpv': 1, 'mh': 1}, 'PLANT': {'ne': 1, 'hpv': 1, 'mh': 1}, 'shift': 1, 'FCB': {'ne': 1, 'hpv': 1, 'mh': 1}, 'CIW': {'ne': 1, 'hpv': 1, 'mh': 1}, 'DAC': {'ne': 1, 'hpv': 1, 'mh': 1}, 'OTHER': {'ne': 0, 'hpv': 0.0, 'mh': 0}, 'FCH': {'ne': 1, 'hpv': 1, 'mh': 1}, 'MAT': {'ne': 1, 'hpv': 1, 'mh': 1}}
