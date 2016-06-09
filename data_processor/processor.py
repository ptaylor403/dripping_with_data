from api.models import HPVATM
from get_data.models import RawDirectRunData
from plantsettings.models import PlantSetting
import datetime as dt
from django.utils import timezone
# from get_data.models import

"""
Checks the server for new data and writes a snapshot of current hpv and other key statistics to the processed data table (api app).
"""

def get_new_hpv_data():
    last_api_write = HPVATM.objects.latest('timestamp')
    try:
        last_claim = RawDirectRunData.latest('TS_LOAD')
    # TODO "server busy" is a placeholder and will need to change when we know the real error message
    except "Server Busy":
        return print("Server busy. Checking again in 5 minutes.")

    settings = PlantSetting.last()

    if last_claim <= last_api_write:
        return print("No new data at this time. Checking again in 5 minutes.")

    # Get list of trucks created in that period and do snap logic on each event using the timestamp on the claim

    # Get shift start time based on last_claim and plant settings

    # Get shift # based on last_claim and plant settings

    get_data()
    write_data()


def get_hpv_snap():
    settings = PlantSetting.latest('timestamp')
    now = timezone.now()

    if now.time() >= settings.first_shift and now.time() < settings.second_shift:
        shift = 1
        start = datetime.combine(now.date(), settings.first_shift)
    elif now.time() >= settings.second_shift and now.time() < settings.third_shift:
        shift = 2
        start = datetime.combine(now.date(), settings.second_shift)

    if settings.num_of_shifts == 3:
        end_third = settings.third_shift + dt.timedelta(hours=8)
        yesterday = now.date() - dt.timedelta(days=1)
        if now.time() >= settings.third_shift and now.time() < (end_third):
            shift = 3
            start = datetime.combine(yesterday, settings.third_shift)

    hpv_dict = main(start)


def write_data(hpv):
    pass
