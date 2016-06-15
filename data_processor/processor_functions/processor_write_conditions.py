import datetime as dt
from django.utils import timezone

def no_dict_or_no_claims(hpv_dict):
    """
    Checks if the dictionary passed was None and that there are claims if there is a dictionary.

    :param hpv_dict: dictionary object from shift calculations or None.
    :return: Boolean value.
    """
    return hpv_dict is None or hpv_dict['claims_for_range'] == 0


def need_to_write(now, plant_settings, last_api_write, last_claim):
    """
    Checks for write conditions to return a boolean of whether or not a write is needed. Returns True if any of the following conditions are True.

    1) The last claim was not before the last API entry was written. If it was, check 2) and 3).
    2) time_to_write - has it been X minutes (defined in the plant settings) since the last write?
    3) near_shift_end - is 'now' within 5 minutes of the end of a shift?


    :param now: The simulated time - datetime object.
    :param plant_settings: The latest settings - PlantSetting object.
    :param last_api_write: The last entry in the API table - HPVATM object.
    :param last_claim: The last entry in the claims table - RawPlantActivity object.
    :return: Boolean value.
    """
    # Gets the setting for max length between write times and checks if it has
    # been over that time since the last API entry was made.
    time_between = plant_settings.TAKT_Time
    time_to_write = now - last_api_write.timestamp > dt.timedelta(minutes=time_between)

    # Checks if "now" is within 5 minutes of the end of a shift
    near_shift_end = is_near_shift_end(now, plant_settings)
    print("LAST CLAIM TSLOAD ", last_claim.TS_LOAD)
    print("LAST API WRITE ",  last_api_write.timestamp)

    # Checks if the last API entry was after the last claim
    if last_claim.TS_LOAD <= last_api_write.timestamp:
        # If the claims up to now have been captured already, check the other
        # conditions for writing.
        if time_to_write or near_shift_end:
            print("It's been a while since an api entry was made or it is near the end of a shift. Recording hpv.")
            return True
        else:
            print("No new data in API TABLE. Checking again in 5 minutes.")
            return False
    return True


def is_near_shift_end(now, plant_settings):
    """
    Checks settings for the shift times and compares them to "now". If "now" is within 5 minutes of the end of any shift (8 hours after start), returns true.

    :param now: The simulated time - datetime object.
    :param plant_settings: The most recent instance of the plant settings.
    :return: Boolean value.
    """

    # Gets a datetime object for each shift end time to compare.
    end_first, end_second, end_third = get_shift_ends(now, plant_settings)

    # Sets the time delta for how far from the shift end is checked.
    within_5 = dt.timedelta(minutes=5)
    delta_0 = dt.timedelta(minutes=0)

    # Checks that now is 5 min before a shift end
    # If plant settings do not show that shift is activated, it is False.
    near_first = end_first - now < within_5 and end_first - now > delta_0
    if plant_settings.num_of_shifts == 2:
        near_second = end_second - now < within_5 and end_second - now > delta_0
    else:
        near_second = False
    if plant_settings.num_of_shifts == 3:
        near_third = end_third - now < within_5 and end_third - now > delta_0
    else:
        near_third = False
    return near_first or near_second or near_third


def get_shift_ends(now, plant_settings):
    """
    Checks plant settings for start of each shift then calc the end of the shift by adding 8 hours to the start time. Times must be converted to datetime for comparisons. Because third shift starts the day before and adding 8 hours would mean the shift end time being compared is the next day and would never return True, 16 hours are subracted instead.

    :param now: The simulated time - datetime object.
    :param plant_settings: The most recent instance of the plant settings.
    :return: A datetime object for the end of the first, second, and third shifts.
    """

    # Makes the time object from settings a datetime for comparing to 'now'
    # End is 8 hours after start.
    end_first = dt.datetime.combine(now.date(), plant_settings.first_shift) + dt.timedelta(hours=8)
    end_first = timezone.make_aware(end_first)

    # Same logic as first
    end_second = dt.datetime.combine(now.date(), plant_settings.second_shift) + dt.timedelta(hours=8)
    end_second = timezone.make_aware(end_second)

    # Third shift starts the day before and ends the morning of the current day.
    # Subtracting 16 hours gets the end of the shift that started the day before.
    end_third = dt.datetime.combine(now.date(), plant_settings.third_shift) - dt.timedelta(hours=16)
    end_third = timezone.make_aware(end_third)

    return end_first, end_second, end_third
