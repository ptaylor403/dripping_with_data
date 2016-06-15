from get_data.models import RawPlantActivity
from api.models import HPVATM
from django.core.exceptions import ObjectDoesNotExist


def get_last_claim(now):
    """
    Attempts to find the most recent claim in the RawPlantActivity table that exited pool 03 before the simulated time. Will raise an ObjectDoesNotExist exception if no claims exist. Prints a message to alert if there is no claim found.

    :param now: The simulated time - datetime object.
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

    :param now: The simulated time - datetime object.
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
