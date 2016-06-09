from api.models import HPVATM
from get_data.models import RawDirectRunData
from plantsettings.models import PlantSetting
import datetime as dt
from django.utils import timezone
from .functions.process_data_main import main
from django.core.exceptions import ObjectDoesNotExist
import pytz


"""
Checks the server for new data and writes a snapshot of current hpv and other key statistics to the processed data table (api app).

Returns: Nothing
"""

def get_new_hpv_data():
    # Is there a claim in the database? Errors could be: Server locked, no matching result for the query. Errors cause function escape.
    try:
        last_claim = RawDirectRunData.objects.latest('TS_LOAD')
    # TODO "server busy" is a placeholder and will need to change when we know the real error message
    # except "ServerBusy":
    #     return print("Server busy. Checking again in 5 minutes.")
    except ObjectDoesNotExist:
        return print("No claims in the database.")

    # Check for the last entry to the processed data table. Escape if no new claim since last entry. Errors include: No objects for the query - continues to writing logic.
    try:
        last_api_write = HPVATM.objects.latest('timestamp')
        if last_claim <= last_api_write:
            return print("No new data at this time. Checking again in 5 minutes.")
    except:
        print("No objects in processed table. Writing.")

    #TODO take out the delta
    with timezone.override("US/Eastern"):
        now = timezone.localtime(PlantSetting.objects.last().dripper_start)
    print("TZ: ", now.tzinfo)

    # Call function to calc hpv by dept for the current shift.
    hpv_dict = get_hpv_snap(now)
    print("-" * 50)
    print("HPV Dict: ", hpv_dict)
    print("-" * 50)

    hpv_dict_with_day = get_day_hpv_dict(hpv_dict, now)

    write_data(hpv_dict_with_day, now)


def get_shift_end(shift):
    dummy_date = dt.combine(dt.date.today(), shift)
    shift_len = dt.timedelta(hours=8)
    shift_end = dummy_date + shift_len
    return shift_end.time()


"""
Finds the current shift and its start time to pass on to the functions that calculate hpv by department and shift

Returns: Dictionary of department keys containing a dictionary of manhours, number clocked in, and hpv for the current shift.
"""

def get_hpv_snap(now):
    settings = PlantSetting.objects.latest('timestamp')

    start, shift = get_shift_info(settings, now)

    print("Start: ", start)
    print("Shift: ", shift)
    print("-" * 50)



    hpv_dict = main(start)
    hpv_dict['shift'] = shift

    return hpv_dict


"""
Gets the current shift and the time it started. Queries the plant settings to decide.

Returns: shift number and start of shift datetime object
"""

@timezone.override("US/Eastern")
def get_shift_info(settings, now):
    print("-" * 50)
    print('settings num of shifts: ', settings.num_of_shifts)
    print('now: ', now)
    print("First_shift: ", settings.first_shift)
    print("Second shift: ", settings.second_shift)

    now = timezone.localtime(now)
    # Catch time before first shift if there are 3 shifts. Shift will have started the day before.
    if now.time() < settings.first_shift and settings.num_of_shifts == 3:
        shift = 3
        yesterday = (now.date() - dt.timedelta(days=1)).date()
        start = dt.datetime.combine(yesterday, settings.third_shift)
        start = timezone.make_aware(start)
    # Catch anything after first shift.
    elif now.time() >= settings.first_shift:
        # If more than 1 shift, check if time is in those shift(s).
        if settings.num_of_shifts >= 2:
            if now.time() >= settings.second_shift:
                # If 3 shifts, check if time is in that shift.
                if settings.num_of_shifts == 3:
                    if now.time() >= settings.third_shift:
                        shift = 3
                        start = dt.datetime.combine(now.date, settings.third_shift)
                        start = timezone.make_aware(start)
                        return start, shift
                shift = 2
                start = dt.datetime.combine(now.date(), settings.second_shift)
                start = timezone.make_aware(start)
                return start, shift
        shift = 1
        start = dt.datetime.combine(now.date(), settings.first_shift)
        start = timezone.make_aware(start)
        return start, shift


def get_day_hpv_dict(hpv_dict, now):
    dept_list = ['CIW', 'FCB', 'PNT', 'PCH', 'FCH', 'DAC', 'MAINT', 'QA', 'MAT', 'OTHER']

    plant_s_hpv = 0
    plant_s_ne = 0
    plant_s_mh = 0

    full_dict = {}

    dept_values = []

    for dept in dept_list:
        plant_s_hpv += hpv_dict[dept]['hpv']
        plant_s_mh += hpv_dict[dept]['mh']
        plant_s_ne += hpv_dict[dept]['ne']

        dept_values.append(get_dept_day_stats(hpv_dict, now, dept))

    print(dept_values)
    shift_dict = {
        'plant_hpv': plant_s_hpv,
        'plant_mh': plant_s_mh,
        'plant_ne': plant_s_ne,
    }


    hpv_dict.update(shift_dict)
    full_dict.update(shift_dict)
    print('Full dict:', full_dict)
    plant_d_hpv, plant_d_mh, claims_d = get_day_stats(hpv_dict, now)


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

        'claims_s': hpv_dict['claims_for_range'],
        'claims_d': claims_d,

        'shift': hpv_dict['shift'],
        'timestamp': now,
    }

    return full_hpv_dict


def get_dept_day_stats(hpv_dict, now, dept):
    settings = PlantSetting.objects.latest('timestamp')
    day_start = get_day_start(settings, now)

    all_since_start = HPVATM.objects.filter(timestamp__gte=day_start)

    cur_hpv = hpv_dict[dept]['hpv']
    cur_mh = hpv_dict[dept]['mh']
    cur_claims = hpv_dict['claims_for_range']

    if settings.num_of_shifts == 3:
        if hpv_dict['shift'] == 3:
            return cur_hpv, cur_mh
        elif hpv_dict['shift'] == 1:
            last_shift = all_since_start.filter(shift=3).last()
            mh = getattr(last_shift, '{}_s_mh'.format(dept)) + cur_mh
            claims = last_shift.claims_s + cur_claims
            hpv = mh/claims
            return hpv, mh
        elif hpv_dict['shift'] == 2:
            s3 = all_since_start.filter(shift=3).last()
            s1 = all_since_start.filter(shift=1).last()
            mh = getattr(s3, '{}_s_mh'.format(dept)) + getattr(s1, '{}_s_mh'.format(dept)) + cur_mh
            claims = s3.claims_s + s2.claims_s + cur_claims
            hpv = mh/claims
            return hpv, mh
    elif settings.num_of_shifts == 2:
        if hpv_dict['shift'] == 1:
            return cur_hpv, cur_mh
        elif hpv_dict['shift'] == 2:
            last_shift = all_since_start.filter(shift=1).last()
            if last_shift is None:
                hpv = cur_hpv
                mh = cur_mh
                claims = cur_claims
            else:
                mh = float(getattr(last_shift, '{}_s_mh'.format(dept))) + cur_mh
                claims = last_shift.claims_s + cur_claims
                try:
                    hpv = mh/claims
                except:
                    hpv = 0
            return hpv, mh
    else:
        return cur_hpv, cur_mh


def get_day_stats(hpv_dict, now):
    settings = PlantSetting.objects.latest('timestamp')
    day_start = get_day_start(settings, now)

    all_since_start = HPVATM.objects.filter(timestamp__gte=day_start)

    cur_hpv = hpv_dict['plant_hpv']
    cur_mh = hpv_dict['plant_mh']
    cur_claims = hpv_dict['claims_for_range']

    if settings.num_of_shifts == 3:
        if hpv_dict['shift'] == 3:
            return cur_hpv, cur_mh, cur_claims
        elif hpv_dict['shift'] == 1:
            last_shift = all_since_start.filter(shift=3).last()
            mh = last_shift.plant_s_mh + cur_mh
            claims = last_shift.claims + cur_claims
            hpv = mh/claims
            return hpv, mh, claims
        elif hpv_dict['shift'] == 2:
            s3 = all_since_start.filter(shift=3).last()
            s1 = all_since_start.filter(shift=1).last()
            mh = s3.plant_s_mh + s1.plant_s_mh + cur_mh
            claims = s3.claims_s + s2.claims_s + cur_claims
            hpv = mh/claims
            return hpv, mh, claims
    elif settings.num_of_shifts == 2:
        if hpv_dict['shift'] == 1:
            return cur_hpv, cur_mh, cur_claims
        elif hpv_dict['shift'] == 2:
            last_shift = all_since_start.filter(shift=1).last()
            if last_shift is None or last_shift.PLANT_s_mh is None:
                hpv = cur_hpv
                mh = cur_mh
                claims = cur_claims
            else:
                mh = last_shift.PLANT_s_mh + cur_mh
                claims = last_shift.claims_s + cur_claims
                hpv = mh/claims
            return hpv, mh, claims
    else:
        return cur_hpv, cur_mh, cur_claims


def get_day_start(settings, now):
    if settings.num_of_shifts == 3:
        yesterday = (now - dt.timedelta(days=1)).date()
        return dt.datetime.combine(yesterday, settings.third_shift)
    else:
        return dt.datetime.combine(now.date(), settings.first_shift)


def write_data(full_hpv_dict, now):
    new = HPVATM.objects.create(**full_hpv_dict)
