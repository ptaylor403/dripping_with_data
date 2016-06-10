from get_data.models import RawPlantActivity
from datetime import datetime


def get_claimed_objects_in_range(start, stop):
    """
    returns filtered objects within a range of start, stop
    :param start: Datetime object that points to the start of the query
    :param stop: Datetime object to slice the view
    :return: RawPlantActivity, 'claim', objects

    """
    claimed_objects = RawPlantActivity.objects.filter(
        TS_LOAD__gte=start,
        TS_LOAD__lte=stop,
        POOL_CD__exact='03',
    )
    return claimed_objects


def get_range_of_claims(start, stop):
    """
    gets trucks claimed in system from start to stop
    :param start: Datetime object that points to the start of the query
    :param stop: Datetime object or None to slice the view or just get from start to current time
    :return: int of number of trucks produced from start to stop
    """
    num_trucks = get_claimed_objects_in_range(start, stop)
    print('('*50)
    print('NUM TRUCKS FROM CLAIMS', num_trucks.count())
    print('(' * 50)
    # for truck in num_trucks:
    #     print(truck.VEH_SER_NO)

    return num_trucks.count()
