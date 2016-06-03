from django.shortcuts import render
from django.views.generic.base import TemplateView
import datetime as dt
from .data_sim import *
from .models import Attendance, Complete
import random

NOW = datetime.now() + dt.timedelta(hours=0)

class Load(TemplateView):
    template_name = "hpv/load.html"

    def get(self, request):
        context = {}
        if request.GET.get('grabAttendance'):
            shift_starts = [6, 14]
            for day in range(1, 6):
                for hour in shift_starts:
                    for _ in range(1, 501):
                        emp = get_employee()
                        dept = get_dept()
                        time_in = clock_in(day, hour)
                        if hour == 6:
                            shift = "first"
                        else:
                            shift = "second"

                        if day == 5 and hour == 14:
                            time_out = None
                        else:
                            time_out = clock_out(day, hour)

                        Attendance.objects.create(employee_number=emp,
                                                  department=dept,
                                                  clock_in_time=time_in,
                                                  clock_out_time=time_out,
                                                  shift=shift)

            text = "5 days worth of clockin data added to the database."
            context['text'] = text

        if request.GET.get('grabComplete'):
            serial_number = get_truck_serial()
            completed = get_completed(1, 7, 0)
            Complete.objects.create(serial_number=serial_number, completed=completed)
            for day in range(1, 6):
                for hour in range(7, 23):
                    while True:
                        last_truck = Complete.objects.latest('completed')
                        prev_time = last_truck.completed
                        if prev_time.hour == hour and prev_time.minute >= 48:
                            break
                        serial_number = get_truck_serial()
                        if prev_time.hour != hour:
                            minute = random.randint(2, 8)
                        else:
                            minute = prev_time.minute + random.randint(7, 12)
                        completed = get_completed(day, hour, minute)
                        Complete.objects.create(serial_number=serial_number, completed=completed)
            text2 = "5 days worth of data added to the database."
            context['text2'] = text2

        return render(request, self.template_name, context)

class HPV(TemplateView):
    template_name = "hpv/hpv2.html"

    def get_context_data(self, **kwargs):
        # When during the hour should we do the headcount?
        context = super().get_context_data(**kwargs)
        departments = ['FCH', 'CIW', 'FCB', 'PNT', 'PCH', 'plant']
        today = datetime.today().date()
        START_TIME1 = 6
        START_TIME2 = 14
        shift_1 = []
        for department in departments:
            dpt_data = [department]
            for i in range(1,9):
                this_dt = datetime.combine(today, dt.time(START_TIME1 + i))
                if this_dt <= NOW:  # datetime.now():
                    dpt_data.append(Attendance.get_active_at(active_time=this_dt,
                                                             department=department)
                                    )
                else:
                    dpt_data.append("")

            shift_1.append(dpt_data)
        shift_2 = []
        for department in departments:
            dpt_data = [department]
            for i in range(1,9):
                this_dt = datetime.combine(today, dt.time(START_TIME2 + i))
                if this_dt <= NOW:  # datetime.now():
                    dpt_data.append(Attendance.get_active_at(active_time=this_dt,
                                                             department=department)
                                    )
                else:
                    dpt_data.append("")
            shift_2.append(dpt_data)

        day_total = Complete.claims_by_time(NOW)  # datetime.now())
        hour_delta = dt.timedelta(hours=1)
        hour_ago = NOW - hour_delta  # datetime.now() - hour_delta
        hour_total = day_total - Complete.claims_by_time(hour_ago)
        context.update({'shift_1': shift_1, 'shift_2': shift_2,
                        'hour_total': hour_total, 'day_total': day_total})

        return context

class Drip(TemplateView):
    template_name = "hpv/drip.html"

    def get(self, request):
        context = {}
        if request.GET.get('dripRate'):
            serial_number = get_truck_serial()
            last_truck = Complete.objects.latest('completed')
            prev_time = last_truck.completed
            print("prev_time.day: ", prev_time.day)
            print("prev_time.hour: ", prev_time.hour)
            print("prev_time.minute: ", prev_time.minute)

            day = prev_time.day
            hour = prev_time.hour
            minute = prev_time.minute + random.randint(7, 12)

            if prev_time.hour >= 22 and prev_time.minute >= 48:
                day += 1
                hour = 7
                minute = random.randint(0, 6)
            elif prev_time.minute >= 48:
                hour = prev_time.hour + 1
                minute = random.randint(0, 6)

            completed = get_completed(day, hour, minute)

            Complete.objects.create(serial_number=serial_number, completed=completed)

            context['lastTruck'] = "The last truck completed and added to the database was {} at {}".format(serial_number, completed)
        return render(request, self.template_name, context)
