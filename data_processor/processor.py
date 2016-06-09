from api.models import HPVATM
from get_data.models import RawDirectRunData
from plantsettings.models import PlantSetting
import datetime as dt
from django.utils import timezone
from .functions.process_data_main import main
from django.core.exceptions import ObjectDoesNotExist


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

    # Call function to calc hpv by dept for the current shift.
    hpv_dict = get_hpv_snap()
    print("-" * 50)
    print("HPV Dict: ", hpv_dict)

    hpv_dict_with_day = get_day_hpv(hpv_dict)

    write_data(hpv_dict_with_day)


def get_shift_end(shift):
    dummy_date = datetime.combine(datetime.date.today(), shift)
    shift_len = dt.timedelta(hours=8)
    shift_end = dummy_date + shift_len
    return shift_end.time()


"""
Finds the current shift and its start time to pass on to the functions that calculate hpv by department and shift

Returns: Dictionary of department keys containing a dictionary of manhours, number clocked in, and hpv for the current shift.
"""

def get_hpv_snap():
    settings = PlantSetting.objects.latest('timestamp')
    now = timezone.now() - dt.timedelta(hours=9)

    start, shift = get_shift_info(settings, now)

    print("Start: ", start)
    print("Shift: ", shift)
    hpv_dict = main(start)

    return hpv_dict


"""
Gets the current shift and the time it started. Queries the plant settings to decide.

Returns: shift number and start of shift datetime object
"""

def get_shift_info(settings, now):
    print("-" * 50)
    print('settings num of shifts: ', settings.num_of_shifts)
    print('now: ', now)
    print('now.time: ', now.time())
    print("First_shift: ", settings.first_shift)
    print("Second shift: ", settings.second_shift)
    print("Now > first: ", now.time() >= settings.first_shift)
    print("Now > second: ", now.time() >= settings.second_shift)
    print("shifts >= two: ", settings.num_of_shifts >= 2)
    print("shifts >= three: ", settings.num_of_shifts >= 3)

    # Catch time before first shift if there are 3 shifts. Shift will have started the day before.
    if now.time() < settings.first_shift and setting.num_of_shifts == 3:
        shift = 3
        yesterday = (dt.now() - dt.timedelta(days=1)).date()
        start = dt.datetime.combine(yesterday, settings.third_shift)
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
                        return start, shift
                shift = 2
                start = dt.datetime.combine(now.date(), settings.second_shift)
                return start, shift
        shift = 1
        start = dt.datetime.combine(now.date(), settings.first_shift)

        return start, shift


def write_data(hpv):
    pass
