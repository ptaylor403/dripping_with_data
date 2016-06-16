from api.models import HPVATM
from get_data.models import RawClockData, RawPlantActivity
from plantsettings.models import PlantSetting
from django.utils import timezone
import datetime as dt


@timezone.override('US/Eastern')
def turn_back(*args, **kwargs):
    last_time = timezone.make_aware(dt.datetime(*args, **kwargs))
    HPVATM.objects.filter(timestamp__gt=last_time).delete()
    RawPlantActivity.objects.filter(TS_LOAD__gt=last_time).delete()
    for i in RawClockData.objects.filter(PNCHEVNT_OUT__gt=last_time):
        i.PNCHEVNT_OUT = None
        i.end_rsn_txt = "&missedOut"
        i.save()
    for i in RawClockData.objects.filter(PNCHEVNT_IN__gt=last_time):
        i.PNCHEVNT_IN = None
        i.start_rsn_txt = None
        i.PNCHEVNT_OUT = None
        i.end_rsn_txt = None
        i.save()
    i = PlantSetting.objects.first()
    i.dripper_start = last_time
    i.save()
