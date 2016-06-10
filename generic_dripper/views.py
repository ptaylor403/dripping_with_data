from django.shortcuts import render, redirect
from .models import RawClockDataDripper
from .models import RawPlantActivityDripper, CombinedDripper
from get_data.models import RawClockData, RawPlantActivity
from api.models import HPVATM
from plantsettings.models import PlantSetting
import datetime as dt
import sys
from django.utils import timezone

if "runserver" in sys.argv:
    all_data_tables = [RawClockData, RawPlantActivity]
    all_drippers = [RawClockDataDripper, RawPlantActivityDripper]
    if not PlantSetting.objects.exists():
        PlantSetting().save()
    the_dripper = CombinedDripper(PlantSetting.objects.last().dripper_start,
                                  dt.timedelta(minutes=15))
    the_dripper.add_dripper(*all_drippers)
else:
    the_dripper = None


def status(request):
    context = {}
    status_list = []
    for table in all_data_tables:
        status_list.append((table.__name__, table.objects.count()))
    for dripper in the_dripper.drippers:
        status_list.append((dripper.__name__, dripper.objects.count()))
    context['status'] = status_list
    context['time'] = the_dripper.simulated_time
    context['running'] = False
    return render(request, 'status.html', context)


def load(request):
    the_dripper.load_drippers()
    return redirect('dripper:status')


def run(request):
    the_dripper.update()
    dripper_time = PlantSetting.objects.last()
    dripper_time.dripper_start = the_dripper.simulated_time
    dripper_time.save()
    context = {}
    status_list = []
    for table in all_data_tables:
        status_list.append((table.__name__, table.objects.count()))
    for dripper in the_dripper.drippers:
        status_list.append((dripper.__name__, dripper.objects.count()))
    context['status'] = status_list
    context['time'] = the_dripper.simulated_time
    context['running'] = True
    return render(request, 'status.html', context)


def reset(request):
    with timezone.override("US/Eastern"):
        the_dripper.simulated_time = timezone.make_aware(dt.datetime(2016, 6, 1, 0, 0))
    dripper_time = PlantSetting.objects.last()
    dripper_time.dripper_start = the_dripper.simulated_time
    dripper_time.save()
    the_dripper.clear_targets()
    HPVATM.objects.all().delete()
    return redirect('dripper:status')


def flush_targets(request):
    the_dripper.clear_targets()
    return redirect('dripper:status')


def flush_drippers(request):
    the_dripper.clear_drippers()
    return redirect('dripper:status')
