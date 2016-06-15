from api.models import HPVATM
from get_data.models import RawPlantActivity
from plantsettings.models import PlantSetting
import datetime as dt
from django.utils import timezone
from .functions.process_data_main import main
from django.core.exceptions import ObjectDoesNotExist


def get_new_hpv_data():
    """
    Checks the server for new claim data. Checks that claims exist and that there is a new claim since the last api entry. It will still write to the api after X minutes (defined in admin plant settings) even if there is no new data. Additionally, it will write the current HPV statistics if it is within 5 minutes of the end of the hour in order to capture a final snapshot of the shift.

    Both day and shift HPV up to that time are written to the API HPVATM table if those conditions are met.

    :return: True if it writes or None and print the reason why it did not write.
    """
    # Finds the latest plant settings and pulls the time between writing if no
    # entries are found and the simulated time from the data dripper
    plant_settings = PlantSetting.objects.latest('timestamp')
    time_between = plant_settings.TAKT_Time
    now = get_time_with_timezone(plant_settings)

    print("/"*50)
    print("GET NEW HPV DATA")
    print("/"*50)
    print("NOW TIME = ", now)
    print("TZ: ", now.tzinfo)

    # Checks that there was a claim in the database and does not write if not.
    last_claim = get_last_claim(now)
    if last_claim is None:
        return

    # Checks for the last time an HPV snapshot was written
    last_api_write, found_entry = get_last_api_write(now)

    # If an entry is found, should we write again?
    # If no entry, it will need to write.
    if found_entry:
        # Is there a new entry, has enough time passed, or is it close to the
        # end of a shift?
        does_need_to_write = need_to_write(now, plant_settings, last_api_write, last_claim)
        if not does_need_to_write:
            return

    # Call function to calc hpv by dept for the current shift.
    hpv_dict = get_hpv_snap(now)
    # If there is no dictionary returned, or the claims are 0, check other write
    # conditions
    if no_dict_or_no_claims(hpv_dict):
        # if there was a previous API entry and
        if found_entry and not does_need_to_write:
            print('No HPV_DICT or no claims in dict. Exiting without write.')
            return

    print("COMPLETED HPV DICT FROM FORMULAS: ", hpv_dict)
    print("COMPLETED HPV DICT CLAIMS_FOR_RANGE: ", hpv_dict['claims_for_range'])

    # Calls functions to calculate values for the day so far and creates a dict
    hpv_dict_with_day = get_day_hpv_dict(hpv_dict, now)

    # Checks if any entries need to be deleted due to age before writing
    delete_old_entries(plant_settings, now)
    write_data(hpv_dict_with_day)

    return True


def get_time_with_timezone(plant_settings):
    """
    Gets the current time, making it timezone aware and in US/Eastern.

    :param plant_settings: The most recent instance of the plant settings.
    :return: TZ aware datetime object
    """
    with timezone.override("US/Eastern"):
        return timezone.localtime(plant_settings.dripper_start)



def get_last_claim(now):
    """
    Attempts to find the most recent claim in the RawPlantActivity table that exited pool 03 before the simulated time. Will raise an ObjectDoesNotExist exception if no claims exist. Prints a message to alert if there is no claim found.

    :param now: The simulated time
    :return: RawPlantActivity model object (claim) or None if no matching queries.
    """
    try:
        last_claim = RawPlantActivity.objects.filter(POOL_CD='03',
                                                     TS_LOAD__lte=now)
        last_claim = last_claim.latest('TS_LOAD')
        print("LAST_CLAIM=", last_claim.VEH_SER_NO, last_claim.TS_LOAD)
        return last_claim
    except ObjectDoesNotExist:
        print("No claims in the database.")
        last_claim = None
        return last_claim


def get_last_api_write(now):
    """
    Attempts to find the most recent entry in the HPVATM API table before the simulated time. Will raise an ObjectDoesNotExist exception if no claims exist. Prints a message to alert if there is no claim found and sets the last_api_write and found_entry variables.

    :param now: The simulated time
    :return: last_api_write: HPVATM model object or None if no matching queries AND found_entry: Boolean value
    """
    try:
        print("GOING TO API TABLE TO GET LATEST API OBJECT")
        last_api_write = HPVATM.objects.filter(timestamp__lte=now)
        last_api_write = last_api_write.latest('timestamp')
        print("THIS IS WHAT WAS FOUND IN API TABLE TIMESTAMP ", last_api_write.timestamp)
        found_entry = True
    except Exception as e:
        print("No objects in processed table. Writing.  ", e)
        # Set both to true to catch either or in hpv_dict check
        last_api_write = None
        found_entry = False
    return last_api_write, found_entry


def no_dict_or_no_claims(hpv_dict):
    """
    Checks if the dictionary passed was None and that there are claims if there is a dictionary.

    :param hpv_dict: dictionary object from shift calculations.
    :return: Boolean value.
    """
    return hpv_dict is None or hpv_dict['claims_for_range'] == 0


def need_to_write(now, plant_settings, last_api_write, last_claim):
    """
    Checks for write conditions to return a boolean of whether or not a write is needed.

    1) time_to_write - has it been X minutes (defined in the plant settings) since the last write?
    2) near_shift_end - is 'now' within 5 minutes of the end of a shift?
    3)

    :param now: The simulated time
    :return: last_api_write: HPVATM model object or None if no matching queries AND found_entry: Boolean value
    """
    time_between = plant_settings.TAKT_Time

    time_to_write = now - last_api_write.timestamp > dt.timedelta(minutes=time_between)

    near_shift_end = is_near_shift_end(now, plant_settings)

    if last_claim.TS_LOAD <= last_api_write.timestamp:
        if time_to_write or near_shift_end:
            print("It's been a while since an api entry was made or it is near the end of a shift. Recording hpv.")
            return True
        else:
            print("No new data in API TABLE. Checking again in 5 minutes.")
            return False
    # return True



def is_near_shift_end(now, plant_settings):
    end_first = dt.datetime.combine(now.date(), plant_settings.first_shift) + dt.timedelta(hours=8)
    end_first = timezone.make_aware(end_first)

    end_second = dt.datetime.combine(now.date(), plant_settings.second_shift) + dt.timedelta(hours=8)
    end_second = timezone.make_aware(end_second)

    end_third = dt.datetime.combine(now.date(), plant_settings.third_shift) + dt.timedelta(hours=8)
    end_third = timezone.make_aware(end_third)

    within_5 = dt.timedelta(minutes=5)

    return end_first - now < within_5 or end_second - now < within_5 or end_third - now < within_5


def delete_old_entries(plant_settings, now):
    del_after_date = now - dt.timedelta(days=plant_settings.del_after)
    HPVATM.objects.filter(timestamp__lte=del_after_date).delete()


def get_hpv_snap(now):
    """
    Finds the current shift and its start time to pass on to the functions that calculate hpv by department and shift

    Returns: Dictionary of department keys containing a dictionary of manhours, number clocked in, and hpv for the current shift.
    """
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


@timezone.override("US/Eastern")
def get_shift_info(plant_settings, now):
    """
    Gets the current shift and the time it started. Queries the plant settings to decide.

    Returns: shift number and start of shift datetime object
    """
    print("/"*50)
    print("GET SHIFT INFO")
    print("/"*50)
    print('plant_settings num of shifts: ', plant_settings.num_of_shifts)
    print('now: ', now)
    print("First_shift: ", plant_settings.first_shift)
    print("Second shift: ", plant_settings.second_shift)

    #SHIFT 1 SET UP
    shift = 1
    start = dt.datetime.combine(now.date(), plant_settings.first_shift)
    start = timezone.make_aware(start)
    print("MADE LOCAL timezone AWARE START")

    # OT SET UP
    first_ot = get_first_shift_ot(now, plant_settings)

    # Catch time before first shift if there are 3 shifts. Shift will have
    # started the day before.
    if now.time() < plant_settings.first_shift and plant_settings.num_of_shifts == 3:
        print("SHIFTS=3")
        shift, start = get_third_shift_start(now, plant_settings)
    #Catch OT for 2nd shift from the previous day
    elif plant_settings.num_of_shifts == 2 and now.time() < first_ot:
        shift, start = get_second_shift_start(now, plant_settings)
    # Catch anything after first shift.
    elif now.time() >= plant_settings.first_shift:
        # If more than 1 shift, check which of those shifts we are in.
        shift, start = find_shift_after_first(now, plant_settings, shift, start)
    else:
        shift = 1
        start = dt.datetime.combine(now.date(), dt.time(0, 0))
        start = timezone.make_aware(start)


    print('START: ', start)
    print('SHIFT: ', shift)

    return start, shift


def get_first_shift_ot(now, plant_settings):
    first_shift_date = dt.datetime.combine(now.date(), plant_settings.first_shift)
    first_ot = first_shift_date - dt.timedelta(hours=3, minutes=30)
    first_ot = first_ot.time()
    return first_ot


def find_shift_after_first(now, plant_settings, shift, start):
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
                shift, start = check_if_in_third_shift(now, plant_settings, shift, start)

    return shift, start


def check_if_in_third_shift(now, plant_settings, shift, start):
    if now.time() >= plant_settings.third_shift:
        shift = 3
        start = dt.datetime.combine(now.date(), plant_settings.third_shift)
        start = timezone.make_aware(start)
    return shift, start


def get_third_shift_start(now, plant_settings):
    shift = 3
    yesterday = (now.date() - dt.timedelta(days=1))
    start = dt.datetime.combine(yesterday, plant_settings.third_shift)
    start = timezone.make_aware(start)
    print("START TIME FOR 3 SHIFTS = ", start)

    return shift, start


def get_second_shift_start(now, plant_settings):
    shift = 2
    yesterday = (now.date() - dt.timedelta(days=1))
    start = dt.datetime.combine(yesterday, plant_settings.second_shift)
    start = timezone.make_aware(start)

    return shift, start


def get_day_hpv_dict(hpv_dict, now):
    """
    Calculates the day total hpv and manhours based on current values since shift start added to the last recorded value of the any previous shifts if applicable.

    Returns: Dictionary object to be written to the api.
    """
    print("/"*50)
    print("GET DAY HPV DICT FUNCTION")
    print("/"*50)

    dept_list = ['CIW', 'FCB', 'PNT', 'PCH', 'FCH', 'DAC', 'MAINT', 'QA', 'MAT', 'OTHER']
    dept_values = []
    full_dict = {}

    plant_s_mh, plant_s_ne = get_dept_plant_stats(hpv_dict, dept_list)

    for dept in dept_list:
        dept_values.append(get_dept_day_stats(hpv_dict, now, dept))

    print("DEPT_VALUES ",dept_values)

    plant_s_hpv = calc_plant_hpv_for_shift(hpv_dict, plant_s_mh)

    shift_dict = {
        'plant_s_hpv': plant_s_hpv,
        'plant_s_mh': plant_s_mh,
        'plant_s_ne': plant_s_ne,
    }

    hpv_dict.update(shift_dict)
    full_dict.update(shift_dict)
    print('FULL DICT:', full_dict)

    plant_d_hpv, plant_d_mh, claims_d = get_plant_day_hpv(hpv_dict, now)
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
        'timestamp': timezone.localtime(now),
    }

    print("FULL DICT ", full_hpv_dict)
    return full_hpv_dict


def get_dept_plant_stats(hpv_dict, dept_list):
    plant_s_ne = 0
    plant_s_mh = 0
    for dept in dept_list:
        plant_s_mh += hpv_dict[dept]['mh']
        plant_s_ne += hpv_dict[dept]['ne']
    return plant_s_mh, plant_s_ne


def calc_plant_hpv_for_shift(hpv_dict, plant_s_mh):
    if hpv_dict['claims_for_range'] == 0 or hpv_dict is None:
        plant_s_hpv = 0
    else:
        plant_s_hpv = plant_s_mh / hpv_dict['claims_for_range']
    return plant_s_hpv


def get_dept_day_stats(hpv_dict, now, dept):
    plant_settings = PlantSetting.objects.latest('timestamp')
    day_start = get_day_start(plant_settings, now)

    all_since_start = HPVATM.objects.filter(timestamp__gte=day_start)

    cur_hpv = hpv_dict[dept]['hpv']
    cur_mh = hpv_dict[dept]['mh']
    cur_claims = hpv_dict['claims_for_range']
    if plant_settings.num_of_shifts == 3:
        hpv, mh = get_three_shifts_dept_day_hpv(hpv_dict, dept, all_since_start, cur_hpv, cur_mh, cur_claims)
    elif plant_settings.num_of_shifts == 2:
        hpv, mh = get_two_shifts_dept_day_hpv(hpv_dict, dept, all_since_start, cur_hpv, cur_mh, cur_claims)
    else:
        hpv, mh = cur_hpv, cur_mh
    return hpv, mh


def get_three_shifts_dept_day_hpv(hpv_dict, dept, all_since_start, cur_hpv, cur_mh, cur_claims):
    if hpv_dict['shift'] == 3:
        hpv, mh =  cur_hpv, cur_mh
    elif hpv_dict['shift'] == 1:
        last_shift = all_since_start.filter(shift=3).last()
        hpv, mh = get_last_shift_dept_day_hpv(dept, cur_mh, cur_claims, last_shift)
    elif hpv_dict['shift'] == 2:
        hpv, mh = get_last_two_shifts_dept_day_hpv(dept, all_since_start, cur_mh, cur_claims)

    return hpv, mh


def get_last_shift_dept_day_hpv(dept, cur_mh, cur_claims, last_shift):
    if last_shift is None:
        mh = cur_mh
        claims = cur_claims
    else:
        mh = float(getattr(last_shift, '{}_s_mh'.format(dept))) + cur_mh
        claims = last_shift.claims_s + cur_claims
    hpv = calc_hpv(mh, claims)
    return hpv, mh


def get_last_two_shifts_dept_day_hpv(dept, all_since_start, cur_mh, cur_claims):
    s3 = all_since_start.filter(shift=3).last()
    s1 = all_since_start.filter(shift=1).last()
    if s3 is None:
        mh, claims = get_last_two_shifts_dept_day_hpv_missing_shift_three(dept, s1, cur_mh, cur_claims)
    elif s1 is None:
        mh, claims = get_last_two_shifts_dept_day_hpv_missing_shift_one(dept, s3, cur_mh, cur_claims)
    else:
        mh = float(getattr(s3, '{}_s_mh'.format(dept))) + float(getattr(s1, '{}_s_mh'.format(dept))) + cur_mh
        claims = s3.claims_s + s1.claims_s + cur_claims
    hpv = calc_hpv(mh, claims)
    return hpv, mh


def get_last_two_shifts_dept_day_hpv_missing_shift_three(dept, s1, cur_mh, cur_claims):
    if s1 is None:
        mh = cur_mh
        claims = cur_claims
    else:
        mh = float(getattr(s1, '{}_s_mh'.format(dept))) + cur_mh
        claims = s1.claims_s + cur_claims
    return mh, claims


def get_last_two_shifts_dept_day_hpv_missing_shift_one(dept, s3, cur_mh, cur_claims):
    mh = float(getattr(s3, '{}_s_mh'.format(dept))) + cur_mh
    claims = s3.claims_s + cur_claims
    if s3 is None:
        mh = cur_mh
        claims = cur_claims
    return mh, claims


def get_two_shifts_dept_day_hpv(hpv_dict, dept, all_since_start, cur_hpv, cur_mh, cur_claims):
    if hpv_dict['shift'] == 1:
        hpv, mh = cur_hpv, cur_mh
    elif hpv_dict['shift'] == 2:
        last_shift = all_since_start.filter(shift=1).last()
        hpv, mh = get_last_shift_dept_day_hpv(dept, cur_mh, cur_claims, last_shift)
    return hpv, mh


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
        if s3 is None:
            mh = cur_mh
            claims = cur_claims
        else:
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


def calc_hpv(mh, claims):
    if claims == 0:
        hpv = 0
    else:
        hpv = mh/claims
    return hpv


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
