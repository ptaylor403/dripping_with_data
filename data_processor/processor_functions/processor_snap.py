from data_processor.functions.process_data_main import main
from processor.shift import get_shift_info
from plantsettings.models import PlantSetting

def get_hpv_snap(now):
    """
    Finds the current shift and its start time to pass on to the functions that calculate hpv by department and shift.

    :param now: The simulated time - datetime object.
    :return: Dictionary of department keys each containing a dictionary of manhours, number clocked in, and hpv for the current shift.
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
