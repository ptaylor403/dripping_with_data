from api.models import HPVATM
from get_data.models import RawPlantActivity
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
    #TODO take out the delta
    with timezone.override("US/Eastern"):
        now = timezone.localtime(PlantSetting.objects.last().dripper_start)
    print("/"*50)
    print("GET NEW HPV DATA")
    print("/"*50)
    print("NOW TIME = ", now)
    print("TZ: ", now.tzinfo)

    # Is there a claim in the database? Errors could be: Server locked, no matching result for the query. Errors cause function escape.
    try:
        last_claim = RawPlantActivity.objects.filter(POOL_CD='03',
                                                     TS_LOAD__lte=now)
        last_claim = last_claim.latest('TS_LOAD')

        print("LAST_CLAIM=", last_claim.VEH_SER_NO, last_claim.TS_LOAD)
    # TODO "server busy" is a placeholder and will need to change when we know the real error message
    # except "ServerBusy":
    #     return print("Server busy. Checking again in 5 minutes.")
    except ObjectDoesNotExist:
        print("No claims in the database.")
        return

    # Check for the last entry to the processed data table. Escape if no new claim since last entry. Errors include: No objects for the query - continues to writing logic.
    try:
        print("GOING TO API TABLE TO GET LATEST API OBJECT")
        last_api_write = HPVATM.objects.filter(timestamp__lte=now)
        last_api_write = last_api_write.latest('timestamp')
        print("THIS IS WHAT WAS FOUND IN API TABLE TIMESTAMP ", last_api_write.timestamp)
        if last_claim.TS_LOAD <= last_api_write.timestamp:
            print("No new data in API TABLE. Checking again in 5 minutes.")
            return
    except Exception as e:
        print("No objects in processed table. Writing.  ", e)

    # Call function to calc hpv by dept for the current shift.
    hpv_dict = get_hpv_snap(now)
    if hpv_dict is None or hpv_dict['claims_for_range'] == 0:
        print('No HPV_DICT or no claims in dict. Exiting without write.')
        return

    print("COMPLETED HPV DICT FROM FORMULAS: ", hpv_dict)
    print("COMPLETED HPV DICT CLAIMS_FOR_RANGE: ", hpv_dict['claims_for_range'])

    hpv_dict_with_day = get_day_hpv_dict(hpv_dict, now)

    write_data(hpv_dict_with_day)

    return "Wrote to API"

"""
Finds the current shift and its start time to pass on to the functions that calculate hpv by department and shift

Returns: Dictionary of department keys containing a dictionary of manhours, number clocked in, and hpv for the current shift.
"""

def get_hpv_snap(now):
    print("/"*50)
    print("GET HPV SNAP")
    print("/"*50)
    plant_settings = PlantSetting.objects.latest('timestamp')
    # print("SETINGS",settings.timestamp)
    print("NOW,",now)
    # preventing processing data before start of defined shift
    start, shift = get_shift_info(plant_settings, now)
    print("Start: ", start)
    print("Shift: ", shift)

    if start > now:
        print("NOT IN SHIFT")
        return
    hpv_dict = main(start, now)
    hpv_dict['shift'] = shift

    return hpv_dict


"""
Gets the current shift and the time it started. Queries the plant settings to decide.

Returns: shift number and start of shift datetime object
"""

@timezone.override("US/Eastern")
def get_shift_info(plant_settings, now):
    #TODO Start of the day is the last time a shift ended yesterday or midnight, > earlier
    print("/"*50)
    print("GET SHIFT INFO")
    print("/"*50)
    print('plant_settings num of shifts: ', plant_settings.num_of_shifts)
    print('now: ', now)
    print("First_shift: ", plant_settings.first_shift)
    print("Second shift: ", plant_settings.second_shift)

    #SHIFT 1 SET UP
    now = timezone.localtime(now)
    shift = 1
    start = dt.datetime.combine(now.date(), plant_settings.first_shift)
    start = timezone.make_aware(start)
    print("MADE LOCAL timezone AWARE START")

    # OT SET UP
    first_shift_date = dt.datetime.combine(now.date(), plant_settings.first_shift)
    first_ot = first_shift_date - dt.timedelta(hours=3, minutes=30)
    first_ot = first_ot.time()

    # Catch time before first shift if there are 3 shifts. Shift will have started the day before.
    if now.time() < plant_settings.first_shift and plant_settings.num_of_shifts == 3:
        print("SHIFTS=3")
        shift = 3
        yesterday = (now.date() - dt.timedelta(days=1))
        start = dt.datetime.combine(yesterday, plant_settings.third_shift)
        start = timezone.make_aware(start)
        print("START TIME FOR 3 SHIFTS = ", start)
    #Catch OT for 2nd shift from the previous day
    elif plant_settings.num_of_shifts == 2 and now.time() < first_ot:
        shift = 2
        yesterday = (now.date() - dt.timedelta(days=1))
        start = dt.datetime.combine(yesterday, plant_settings.second_shift)
        start = timezone.make_aware(start)
    # Catch anything after first shift.
    elif now.time() >= plant_settings.first_shift:
        # If more than 1 shift, check if time is in those shift(s).
        if plant_settings.num_of_shifts >= 2:
            print("2 or MORE SHIFTS ACTIVATED")
            if now.time() >= plant_settings.second_shift:
                print("2nd 3 SHIFT CHECK")
                shift = 2
                start = dt.datetime.combine(now.date(), plant_settings.second_shift)
                start = timezone.make_aware(start)
                # If 3 shifts, check if time is in that shift.
                print("2nd 3 SHIFT CHECK")
                if plant_settings.num_of_shifts == 3:
                    if now.time() >= plant_settings.third_shift:
                        shift = 3
                        start = dt.datetime.combine(now.date(), plant_settings.third_shift)
                        start = timezone.make_aware(start)
    # Catch OT for before 1st shift begins
    else:
        shift = 1
        start = dt.datetime.combine(now.date(), dt.time(0, 0))
        start = timezone.make_aware(start)


    print('START: ', start)
    print('SHIFT: ', shift)

    return start, shift


def get_day_hpv_dict(hpv_dict, now):
    print("/"*50)
    print("GET DAY HPV DICT FUNCTION")
    print("/"*50)

    dept_list = ['CIW', 'FCB', 'PNT', 'PCH', 'FCH', 'DAC', 'MAINT', 'QA', 'MAT', 'OTHER']

    plant_s_hpv = 0
    plant_s_ne = 0
    plant_s_mh = 0

    full_dict = {}

    dept_values = []

    for dept in dept_list:
        plant_s_mh += hpv_dict[dept]['mh']
        plant_s_ne += hpv_dict[dept]['ne']

        dept_values.append(get_dept_day_stats(hpv_dict, now, dept))

    print("DEPT_VALUES ",dept_values)

    if hpv_dict['claims_for_range'] == 0 or hpv_dict is None:
        plant_s_hpv = 0
    else:
        plant_s_hpv = plant_s_mh / hpv_dict['claims_for_range']

    shift_dict = {
        'plant_s_hpv': plant_s_hpv,
        'plant_s_mh': plant_s_mh,
        'plant_s_ne': plant_s_ne,
    }

    hpv_dict.update(shift_dict)
    full_dict.update(shift_dict)
    print('FULL DICT:', full_dict)

    plant_d_hpv, plant_d_mh, claims_d = get_day_stats(hpv_dict, now)
    print("plant_d_hpv, plant_d_mh, claims_d= ", plant_d_hpv, plant_d_mh, claims_d)

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
        'timestamp': now,
    }
    print("FULL DICT ", full_hpv_dict)
    return full_hpv_dict


def get_dept_day_stats(hpv_dict, now, dept):
    plant_settings = PlantSetting.objects.latest('timestamp')
    day_start = get_day_start(plant_settings, now)

    all_since_start = HPVATM.objects.filter(timestamp__gte=day_start)

    cur_hpv = hpv_dict[dept]['hpv']
    cur_mh = hpv_dict[dept]['mh']
    cur_claims = hpv_dict['claims_for_range']
    # print("cur_mh: ", cur_mh)

    if plant_settings.num_of_shifts == 3:
        if hpv_dict['shift'] == 3:
            return cur_hpv, cur_mh
        elif hpv_dict['shift'] == 1:
            last_shift = all_since_start.filter(shift=3).last()
            if last_shift is None:
                mh = cur_mh
                claims = cur_claims
            else:
                mh = getattr(last_shift, '{}_s_mh'.format(dept)) + cur_mh
                claims = last_shift.claims_s + cur_claims
            if claims == 0:
                hpv = 0
            else:
                hpv = mh/claims
            return hpv, mh
        elif hpv_dict['shift'] == 2:
            s3 = all_since_start.filter(shift=3).last()
            s1 = all_since_start.filter(shift=1).last()
            if s3 is None:
                if s1 is None:
                    hpv = cur_hpv
                    mh = cur_mh
                    claims = cur_claims
                else:
                    mh = getattr(s3, '{}_s_mh'.format(dept)) + cur_mh
                    claims = s3.claims_s + cur_claims
            elif s1 is None:
                if s3 is None:
                    mh = cur_mh
                    claims = cur_claims
                else:
                    mh = getattr(s1, '{}_s_mh'.format(dept)) + cur_mh
                    claims = s1.claims_s + cur_claims
            else:
                mh = getattr(s3, '{}_s_mh'.format(dept)) + getattr(s1, '{}_s_mh'.format(dept)) + cur_mh
                claims = s3.claims_s + s1.claims_s + cur_claims
            if claims == 0:
                hpv = 0
            else:
                hpv = mh/claims
            return hpv, mh
    elif plant_settings.num_of_shifts == 2:
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
        if hpv_dict['shift'] == 3:
            return cur_hpv, cur_mh, cur_claims
        elif hpv_dict['shift'] == 1:
            last_shift = all_since_start.filter(shift=3).last()
            if last_shift is None:
                hpv = cur_hpv
                mh = cur_mh
                claims = cur_claims
            else:
                mh = last_shift.PLANT_s_mh + cur_mh
                claims = last_shift.claims_s + cur_claims
                if claims == 0:
                    hpv = 0
                else:
                    hpv = mh/claims
            return hpv, mh, claims
        elif hpv_dict['shift'] == 2:
            s3 = all_since_start.filter(shift=3).last()
            s1 = all_since_start.filter(shift=1).last()
            if s3 is None:
                if s1 is None:
                    mh = cur_mh
                    claims = cur_claims
                else:
                    mh = s1.PLANT_s_mh + cur_mh
                    claims = s1.claims_s + cur_claims
            elif s1 is None:
                if s3 is None:
                    mh = cur_mh
                    claims = cur_claims
                else:
                    mh = s3.PLANT_s_mh + cur_mh
                    claims = s3.claims_s + cur_claims
            else:
                mh = s3.PLANT_s_mh + s1.PLANT_s_mh + cur_mh
                claims = s3.claims_s + s1.claims_s + cur_claims
            if claims == 0:
                hpv = 0
            else:
                hpv = mh/claims
            return hpv, mh, claims
    elif plant_settings.num_of_shifts == 2:
        if hpv_dict['shift'] == 1:
            return cur_hpv, cur_mh, cur_claims
        elif hpv_dict['shift'] == 2:
            last_shift = all_since_start.filter(shift=1).last()
            if last_shift is None or last_shift.PLANT_s_mh is None:
                hpv = cur_hpv
                mh = cur_mh
                claims = cur_claims
            else:
                mh = float(last_shift.PLANT_s_mh) + cur_mh
                claims = last_shift.claims_s + cur_claims
                if claims == 0:
                    hpv = 0
                else:
                    hpv = mh/claims
            return hpv, mh, claims
    else:
        return cur_hpv, cur_mh, cur_claims


def get_day_start(plant_settings, now):
    if plant_settings.num_of_shifts == 3:
        if now.time() >= plant_settings.third_shift:
            day_start = dt.datetime.combine(now.date(), plant_settings.third_shift)
        else:
            yesterday = (now - dt.timedelta(days=1)).date()
            day_start = dt.datetime.combine(yesterday, plant_settings.third_shift)
    else:
        day_start = dt.datetime.combine(now.date(), plant_settings.first_shift)
    return timezone.localtime(timezone.make_aware(day_start))


def write_data(full_hpv_dict):
    new = HPVATM.objects.create(**full_hpv_dict)
