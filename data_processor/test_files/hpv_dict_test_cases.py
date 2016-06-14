from django.utils import timezone
import datetime as dt


"""
HPV Dictionaries
"""
shift_1_hpv_dict = {'QA': {'ne': 10, 'hpv': 10, 'mh': 10}, 'claims_for_range': 1, 'MAINT': {'ne': 10, 'hpv': 10, 'mh': 10}, 'PNT': {'ne': 10, 'hpv': 10, 'mh': 10}, 'PCH': {'ne': 10, 'hpv': 10, 'mh': 10}, 'PLANT': {'ne': 10, 'hpv': 10, 'mh': 10}, 'shift': 1, 'FCB': {'ne': 10, 'hpv': 10, 'mh': 10}, 'CIW': {'ne': 10, 'hpv': 10, 'mh': 10}, 'DAC': {'ne': 10, 'hpv': 10, 'mh': 10}, 'OTHER': {'ne': 0, 'hpv': 0.0, 'mh': 0}, 'FCH': {'ne': 10, 'hpv': 10, 'mh': 10}, 'MAT': {'ne': 10, 'hpv': 10, 'mh': 10}}

shift_1_hpv_dict_0_hpv = {'QA': {'ne': 0, 'hpv': 0, 'mh': 0}, 'claims_for_range': 0, 'MAINT': {'ne': 0, 'hpv': 0, 'mh': 0}, 'PNT': {'ne': 0, 'hpv': 0, 'mh': 0}, 'PCH': {'ne': 0, 'hpv': 0, 'mh': 0}, 'PLANT': {'ne': 0, 'hpv': 0, 'mh': 0}, 'shift': 1, 'FCB': {'ne': 0, 'hpv': 0, 'mh': 0}, 'CIW': {'ne': 0, 'hpv': 0, 'mh': 0}, 'DAC': {'ne': 0, 'hpv': 0, 'mh': 0}, 'OTHER': {'ne': 0, 'hpv': 0.0, 'mh': 0}, 'FCH': {'ne': 0, 'hpv': 0, 'mh': 0}, 'MAT': {'ne': 0, 'hpv': 0, 'mh': 0}}

shift_1_hpv_dict_with_plant = {'QA': {'ne': 10, 'hpv': 10, 'mh': 10}, 'claims_for_range': 1, 'MAINT': {'ne': 10, 'hpv': 10, 'mh': 10}, 'PNT': {'ne': 10, 'hpv': 10, 'mh': 10}, 'PCH': {'ne': 10, 'hpv': 10, 'mh': 10}, 'PLANT': {'ne': 10, 'hpv': 10, 'mh': 10}, 'shift': 1, 'FCB': {'ne': 10, 'hpv': 10, 'mh': 10}, 'CIW': {'ne': 10, 'hpv': 10, 'mh': 10}, 'DAC': {'ne': 10, 'hpv': 10, 'mh': 10}, 'OTHER': {'ne': 0, 'hpv': 0, 'mh': 0}, 'FCH': {'ne': 10, 'hpv': 10, 'mh': 10}, 'MAT': {'ne': 10, 'hpv': 10, 'mh': 10}, 'plant_s_hpv': 90, 'plant_s_mh': 90, 'plant_s_ne': 90}

shift_1_hpv_dict_with_plant_0_hpv = {'QA': {'ne': 0, 'hpv': 0, 'mh': 0}, 'claims_for_range': 0, 'MAINT': {'ne': 0, 'hpv': 0, 'mh': 0}, 'PNT': {'ne': 0, 'hpv': 0, 'mh': 0}, 'PCH': {'ne': 0, 'hpv': 0, 'mh': 0}, 'PLANT': {'ne': 0, 'hpv': 0, 'mh': 0}, 'shift': 1, 'FCB': {'ne': 0, 'hpv': 0, 'mh': 0}, 'CIW': {'ne': 0, 'hpv': 0, 'mh': 0}, 'DAC': {'ne': 0, 'hpv': 0, 'mh': 0}, 'OTHER': {'ne': 0, 'hpv': 0.0, 'mh': 0}, 'FCH': {'ne': 0, 'hpv': 0, 'mh': 0}, 'MAT': {'ne': 0, 'hpv': 0, 'mh': 0}, 'plant_s_hpv': 0, 'plant_s_mh': 0, 'plant_s_ne': 0}

shift_2_hpv_dict = {'QA': {'ne': 10, 'hpv': 10, 'mh': 10}, 'claims_for_range': 1, 'MAINT': {'ne': 10, 'hpv': 10, 'mh': 10}, 'PNT': {'ne': 10, 'hpv': 10, 'mh': 10}, 'PCH': {'ne': 10, 'hpv': 10, 'mh': 10}, 'PLANT': {'ne': 10, 'hpv': 10, 'mh': 10}, 'shift': 2, 'FCB': {'ne': 10, 'hpv': 10, 'mh': 10}, 'CIW': {'ne': 10, 'hpv': 10, 'mh': 10}, 'DAC': {'ne': 10, 'hpv': 10, 'mh': 10}, 'OTHER': {'ne': 0, 'hpv': 0.0, 'mh': 0}, 'FCH': {'ne': 10, 'hpv': 10, 'mh': 10}, 'MAT': {'ne': 10, 'hpv': 10, 'mh': 10}}

shift_2_hpv_dict_0_hpv = {'QA': {'ne': 0, 'hpv': 0, 'mh': 0}, 'claims_for_range': 0, 'MAINT': {'ne': 0, 'hpv': 0, 'mh': 0}, 'PNT': {'ne': 0, 'hpv': 0, 'mh': 0}, 'PCH': {'ne': 0, 'hpv': 0, 'mh': 0}, 'PLANT': {'ne': 0, 'hpv': 0, 'mh': 0}, 'shift': 2, 'FCB': {'ne': 0, 'hpv': 0, 'mh': 0}, 'CIW': {'ne': 0, 'hpv': 0, 'mh': 0}, 'DAC': {'ne': 0, 'hpv': 0, 'mh': 0}, 'OTHER': {'ne': 0, 'hpv': 0.0, 'mh': 0}, 'FCH': {'ne': 0, 'hpv': 0, 'mh': 0}, 'MAT': {'ne': 0, 'hpv': 0, 'mh': 0}}

shift_2_hpv_dict_with_plant = {'QA': {'ne': 10, 'hpv': 10, 'mh': 10}, 'claims_for_range': 1, 'MAINT': {'ne': 10, 'hpv': 10, 'mh': 10}, 'PNT': {'ne': 10, 'hpv': 10, 'mh': 10}, 'PCH': {'ne': 10, 'hpv': 10, 'mh': 10}, 'PLANT': {'ne': 10, 'hpv': 10, 'mh': 10}, 'shift': 2, 'FCB': {'ne': 10, 'hpv': 10, 'mh': 10}, 'CIW': {'ne': 10, 'hpv': 10, 'mh': 10}, 'DAC': {'ne': 10, 'hpv': 10, 'mh': 10}, 'OTHER': {'ne': 0, 'hpv': 0, 'mh': 0}, 'FCH': {'ne': 10, 'hpv': 10, 'mh': 10}, 'MAT': {'ne': 10, 'hpv': 10, 'mh': 10}, 'plant_s_hpv': 90, 'plant_s_mh': 90,'plant_s_ne': 90,}

shift_2_hpv_dict_with_plant_0_hpv = {'QA': {'ne': 0, 'hpv': 0, 'mh': 0}, 'claims_for_range': 0, 'MAINT': {'ne': 0, 'hpv': 0, 'mh': 0}, 'PNT': {'ne': 0, 'hpv': 0, 'mh': 0}, 'PCH': {'ne': 0, 'hpv': 0, 'mh': 0}, 'PLANT': {'ne': 0, 'hpv': 0, 'mh': 0}, 'shift': 2, 'FCB': {'ne': 0, 'hpv': 0, 'mh': 0}, 'CIW': {'ne': 0, 'hpv': 0, 'mh': 0}, 'DAC': {'ne': 0, 'hpv': 0, 'mh': 0}, 'OTHER': {'ne': 0, 'hpv': 0.0, 'mh': 0}, 'FCH': {'ne': 0, 'hpv': 0, 'mh': 0}, 'MAT': {'ne': 0, 'hpv': 0, 'mh': 0}, 'plant_s_hpv': 0, 'plant_s_mh': 0, 'plant_s_ne': 0}

shift_3_hpv_dict = {'QA': {'ne': 10, 'hpv': 10, 'mh': 10}, 'claims_for_range': 1, 'MAINT': {'ne': 10, 'hpv': 10, 'mh': 10}, 'PNT': {'ne': 10, 'hpv': 10, 'mh': 10}, 'PCH': {'ne': 10, 'hpv': 10, 'mh': 10}, 'PLANT': {'ne': 10, 'hpv': 10, 'mh': 10}, 'shift': 3, 'FCB': {'ne': 10, 'hpv': 10, 'mh': 10}, 'CIW': {'ne': 10, 'hpv': 10, 'mh': 10}, 'DAC': {'ne': 10, 'hpv': 10, 'mh': 10}, 'OTHER': {'ne': 0, 'hpv': 0.0, 'mh': 0}, 'FCH': {'ne': 10, 'hpv': 10, 'mh': 10}, 'MAT': {'ne': 10, 'hpv': 10, 'mh': 10}}

shift_3_hpv_dict_0_hpv = {'QA': {'ne': 0, 'hpv': 0, 'mh': 0}, 'claims_for_range': 0, 'MAINT': {'ne': 0, 'hpv': 0, 'mh': 0}, 'PNT': {'ne': 0, 'hpv': 0, 'mh': 0}, 'PCH': {'ne': 0, 'hpv': 0, 'mh': 0}, 'PLANT': {'ne': 0, 'hpv': 0, 'mh': 0}, 'shift': 3, 'FCB': {'ne': 0, 'hpv': 0, 'mh': 0}, 'CIW': {'ne': 0, 'hpv': 0, 'mh': 0}, 'DAC': {'ne': 0, 'hpv': 0, 'mh': 0}, 'OTHER': {'ne': 0, 'hpv': 0.0, 'mh': 0}, 'FCH': {'ne': 0, 'hpv': 0, 'mh': 0}, 'MAT': {'ne': 0, 'hpv': 0, 'mh': 0}}

shift_3_hpv_dict_with_plant = {'QA': {'ne': 10, 'hpv': 10, 'mh': 10}, 'claims_for_range': 1, 'MAINT': {'ne': 10, 'hpv': 10, 'mh': 10}, 'PNT': {'ne': 10, 'hpv': 10, 'mh': 10}, 'PCH': {'ne': 10, 'hpv': 10, 'mh': 10}, 'PLANT': {'ne': 10, 'hpv': 10, 'mh': 10}, 'shift': 3, 'FCB': {'ne': 10, 'hpv': 10, 'mh': 10}, 'CIW': {'ne': 10, 'hpv': 10, 'mh': 10}, 'DAC': {'ne': 10, 'hpv': 10, 'mh': 10}, 'OTHER': {'ne': 0, 'hpv': 0, 'mh': 0}, 'FCH': {'ne': 10, 'hpv': 10, 'mh': 10}, 'MAT': {'ne': 10, 'hpv': 10, 'mh': 10}, 'plant_s_hpv': 90, 'plant_s_mh': 90, 'plant_s_ne': 90}

shift_3_hpv_dict_with_plant_0_hpv = {'QA': {'ne': 0, 'hpv': 0, 'mh': 0}, 'claims_for_range': 0, 'MAINT': {'ne': 0, 'hpv': 0, 'mh': 0}, 'PNT': {'ne': 0, 'hpv': 0, 'mh': 0}, 'PCH': {'ne': 0, 'hpv': 0, 'mh': 0}, 'PLANT': {'ne': 0, 'hpv': 0, 'mh': 0}, 'shift': 3, 'FCB': {'ne': 0, 'hpv': 0, 'mh': 0}, 'CIW': {'ne': 0, 'hpv': 0, 'mh': 0}, 'DAC': {'ne': 0, 'hpv': 0, 'mh': 0}, 'OTHER': {'ne': 0, 'hpv': 0.0, 'mh': 0}, 'FCH': {'ne': 0, 'hpv': 0, 'mh': 0}, 'MAT': {'ne': 0, 'hpv': 0, 'mh': 0}, 'plant_s_hpv': 0, 'plant_s_mh': 0, 'plant_s_ne': 0}


expected_full_hpv_dict = {
    'CIW_s_hpv': 10,
    'CIW_s_mh': 10,
    'CIW_s_ne': 10,
    'CIW_d_hpv': 10.0,
    'CIW_d_mh': 90.0,
    'FCB_s_hpv': 10.0,
    'FCB_s_mh': 10,
    'FCB_s_ne': 10,
    'FCB_d_hpv': 10.0,
    'FCB_d_mh': 90.0,
    'PNT_s_hpv': 10,
    'PNT_s_mh': 10,
    'PNT_s_ne': 10,
    'PNT_d_hpv': 10.0,
    'PNT_d_mh': 90.0,
    'PCH_s_hpv': 10,
    'PCH_s_mh': 10,
    'PCH_s_ne': 10,
    'PCH_d_hpv': 10.0,
    'PCH_d_mh': 90.0,
    'FCH_s_hpv': 10,
    'FCH_s_mh': 10,
    'FCH_s_ne': 10,
    'FCH_d_hpv': 10.0,
    'FCH_d_mh': 90.0,
    'DAC_s_hpv': 10,
    'DAC_s_mh': 10,
    'DAC_s_ne': 10,
    'DAC_d_hpv': 10.0,
    'DAC_d_mh': 90.0,
    'MAINT_s_hpv': 10,
    'MAINT_s_mh': 10,
    'MAINT_s_ne': 10,
    'MAINT_d_hpv': 10.0,
    'MAINT_d_mh': 90.0,
    'QA_s_hpv': 10,
    'QA_s_mh': 10,
    'QA_s_ne': 10,
    'QA_d_hpv': 10.0,
    'QA_d_mh': 90.0,
    'MAT_s_hpv': 10,
    'MAT_s_mh': 10,
    'MAT_s_ne': 10,
    'MAT_d_hpv': 10.0,
    'MAT_d_mh': 90.0,
    'OTHER_s_hpv': 0,
    'OTHER_s_mh': 0,
    'OTHER_s_ne': 0,
    'OTHER_d_hpv': 0,
    'OTHER_d_mh': 0,

    'PLANT_d_hpv': 90.0,
    'PLANT_d_mh': 810.0,
    'PLANT_s_hpv': 90.0,
    'PLANT_s_ne': 90.0,
    'PLANT_s_mh': 90.0,

    'claims_s': 1,
    'claims_d': 9,

    'shift': 2,
    'timestamp': timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
}
