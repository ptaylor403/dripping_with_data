from plantsettings.models import PlantSetting
from api.models import HPVATM
from .processor_shift import get_day_start
from .processor_get_new_hpv import *


def get_plant_day_hpv(hpv_dict, now):
    print("/"*50)
    print("GET DAY STATS FUNCTION")
    print("/"*50)
    print("NOW ", now)

    plant_settings = PlantSetting.objects.latest('timestamp')
    day_start = get_day_start(plant_settings, now)

    all_since_start = HPVATM.objects.filter(timestamp__gte=day_start)

    cur_hpv = hpv_dict['plant_s_hpv']
    cur_mh = hpv_dict['plant_s_mh']
    cur_claims = hpv_dict['claims_for_range']

    if plant_settings.num_of_shifts == 3:
        hpv, mh, claims = get_three_shifts_plant_day_hpv(hpv_dict, all_since_start, cur_hpv, cur_mh, cur_claims)
    elif plant_settings.num_of_shifts == 2:
        hpv, mh, claims = get_two_shifts_plant_day_hpv(hpv_dict, all_since_start, cur_hpv, cur_mh, cur_claims)
    else:
        hpv, mh, claims = cur_hpv, cur_mh, cur_claims
    return hpv, mh, claims


def get_three_shifts_plant_day_hpv(hpv_dict, all_since_start, cur_hpv, cur_mh, cur_claims):
    if hpv_dict['shift'] == 3:
        return cur_hpv, cur_mh, cur_claims
    elif hpv_dict['shift'] == 1:
        last_shift = all_since_start.filter(shift=3).last()
        hpv, mh, claims = get_last_shift_plant_day_hpv(cur_hpv, cur_mh, cur_claims, last_shift)
    elif hpv_dict['shift'] == 2:
        s3 = all_since_start.filter(shift=3).last()
        s1 = all_since_start.filter(shift=1).last()
        hpv, mh, claims = get_three_shifts_plant_day_hpv_2nd_shift(s3, s1, cur_mh, cur_claims)

    return hpv, mh, claims


def get_three_shifts_plant_day_hpv_2nd_shift(s3, s1, cur_mh, cur_claims):
    if s3 is None:
        if s1 is None:
            mh = cur_mh
            claims = cur_claims
        else:
            mh = s1.PLANT_s_mh + cur_mh
            claims = s1.claims_s + cur_claims
    elif s1 is None:
        mh = s3.PLANT_s_mh + cur_mh
        claims = s3.claims_s + cur_claims
    else:
        mh = s3.PLANT_s_mh + s1.PLANT_s_mh + cur_mh
        claims = s3.claims_s + s1.claims_s + cur_claims
    hpv = calc_hpv(mh, claims)

    return hpv, mh, claims


def get_two_shifts_plant_day_hpv(hpv_dict, all_since_start, cur_hpv, cur_mh, cur_claims):
    if hpv_dict['shift'] == 1:
        hpv, mh, claims = cur_hpv, cur_mh, cur_claims
    elif hpv_dict['shift'] == 2:
        last_shift = all_since_start.filter(shift=1).last()
        hpv, mh, claims = get_last_shift_plant_day_hpv(cur_hpv, cur_mh, cur_claims, last_shift)
    return hpv, mh, claims


def get_last_shift_plant_day_hpv(cur_hpv, cur_mh, cur_claims, last_shift):
    if last_shift is None or last_shift.PLANT_s_mh is None:
        hpv = cur_hpv
        mh = cur_mh
        claims = cur_claims
    else:
        mh = float(last_shift.PLANT_s_mh) + cur_mh
        claims = last_shift.claims_s + cur_claims
        hpv = calc_hpv(mh, claims)
    return hpv, mh, claims
