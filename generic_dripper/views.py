from django.shortcuts import render, redirect
from .models import RawClockDataDripper, RawDirectRunDataDripper
from .models import RawCrysDataDripper, RawPlantActivityDripper, CombinedDripper
from get_data.models import RawClockData, RawDirectRunData, RawCrysData, RawPlantActivity
from plantsettings.models import PlantSetting
import datetime as dt
import sys

if "runserver" in sys.argv:
    all_data_tables = [RawClockData, RawDirectRunData,
                       RawCrysData, RawPlantActivity]
    all_drippers = [RawClockDataDripper, RawDirectRunDataDripper,
                    RawCrysDataDripper, RawPlantActivityDripper]
    if not PlantSetting.objects.exists():
        PlantSetting().save()
    the_dripper = CombinedDripper(PlantSetting.objects.last().dripper_start,
                                  dt.timedelta(minutes=240))
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


def restart(request):
    pass


def flush_targets(request):
    the_dripper.clear_targets()
    return redirect('dripper:status')


def flush_drippers(request):
    the_dripper.clear_drippers()
    return redirect('dripper:status')
