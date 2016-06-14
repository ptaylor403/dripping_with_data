from django.shortcuts import render
from django.views.generic.base import TemplateView
import datetime as dt
from .data_sim import *
from .models import Attendance, Complete
from api.models import HPVATM
import random
import pytz
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from get_data.models import RawPlantActivity, RawClockData
from generic_dripper.views import the_dripper
from api.models import HPVATM
import sys
from collections import OrderedDict

# if "runserver" in sys.argv:
#     NOW = the_dripper.simulated_time.replace(tzinfo=None)
# else:
NOW = datetime.now() - dt.timedelta(days=7, hours=0)
today = datetime.now() - dt.timedelta(days=7, hours=0)



class Load(LoginRequiredMixin, TemplateView):
    template_name = "hpv/load.html"
    login_url = '/login/'

    def get(self, request):
        context = {}
        if request.GET.get('grabAttendance'):
            shift_starts = [6, 14]
            for day in range(1, 11):
                for hour in shift_starts:
                    for _ in range(1, 501):
                        emp = get_employee()
                        dept = get_dept()
                        time_in = clock_in(day, hour)
                        if hour == 6:
                            shift = "first"
                        else:
                            shift = "second"

                        if day == 10 and hour == 14:
                            time_out = None
                        else:
                            time_out = clock_out(day, hour)

                        Attendance.objects.create(employee_number=emp,
                                                  department=dept,
                                                  clock_in_time=time_in,
                                                  clock_out_time=time_out,
                                                  shift=shift)

            text = "10 days worth of clockin data added to the database."
            context['text'] = text

        if request.GET.get('grabComplete'):
            serial_number = get_truck_serial()
            completed = get_completed(1, 7, 0)
            Complete.objects.create(serial_number=serial_number, completed=completed)
            for day in range(1, 11):
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
            text2 = "10 days worth of data added to the database."
            context['text2'] = text2

        if request.GET.get('grabAPI'):
            for day in range(1, 11):
                for hour in range(6, 23):
                    for minute in [5, 15, 25, 35, 45, 55]:
                        timestamp = dt.datetime(2016, 6, day, hour, minute)
                        if hour == 6:
                            hpv_plant = random.randint(100, 103)
                            num_clocked_in = random.randint(750, 800)
                        elif hour >= 7 and hour <= 9:
                            hpv_plant = random.randint(97, 100)
                            num_clocked_in = random.randint(750, 800)
                        elif hour >= 10 and hour <= 14:
                            hpv_plant = random.randint(94, 97)
                            num_clocked_in = random.randint(750, 800)
                        elif hour >= 15 and hour <= 17:
                            hpv_plant = random.randint(91, 94)
                            num_clocked_in = random.randint(550, 600)
                        elif hour >= 18:
                            hpv_plant = random.randint(88, 91)
                            num_clocked_in = random.randint(550, 600)
                        hpv_obj = HPVATM.objects.create(hpv_plant=hpv_plant, num_clocked_in=num_clocked_in)
                        hpv_obj.timestamp = timestamp
                        hpv_obj.save()

                    text3 = "10 days worth of data added to the database."
                    context['text3'] = text3

        return render(request, self.template_name, context)


class HPV(LoginRequiredMixin, TemplateView):
    template_name = "hpv/hpv2.html"
    login_url = '/login/'

    def _get_plant_history(shift_start_time, today):
        shift = []
        # for department in departments:
        #     dpt_data = [department]
        for i in range(1,17):
            print('Hour: ', i)
            this_dt = datetime.combine(today, dt.time(shift_start_time + i))
            if this_dt <= NOW:  # datetime.now():
                num_in = RawClockData.get_clocked_in(start=this_dt).filter(PNCHEVNT_IN__gte=this_dt, PNCHEVNT_IN__lt=this_dt + dt.timedelta(i + 1)).count()
                shift.append(num_in)
                print("num_in: ", num_in)
            else:
                shift.append("")

        return shift

    def _get_shift_manhour_history(departments, shift_start_time, today):
        shift = []
        for department in departments:
            dpt_data = [department]
            for i in range(1,9):
                this_dt = datetime.combine(today, dt.time(shift_start_time + i))
                start_dt = datetime.combine(today, dt.time(shift_start_time))
                this_dt = pytz.utc.localize(this_dt)
                start_dt = pytz.utc.localize(start_dt)
                if this_dt <= pytz.utc.localize(NOW):  # datetime.now():
                    dpt_data.append(Attendance.get_manhours_during(start=start_dt, stop=this_dt, department=department))
                else:
                    dpt_data.append("")

            shift.append(dpt_data)
        return shift

    def _get_department_hpv(departments, START_TIME1, START_TIME2, NOW):
        # Get the department
        # Get the plant total manhours for each department from the start of the day to NOW
        # Get the manhours for that department from the start of each shift to NOW or end of shift
        hpv_data = []
        start_times = [START_TIME1, START_TIME1, START_TIME2]
        end_times = [NOW, min(NOW, START_TIME2), min(NOW, (START_TIME2 + dt.timedelta(hours=8)))]
        truck_totals = []
        for start_time, end_time in zip(start_times, end_times):
            truck_totals.append(Complete.claims_by_time(end_time) - Complete.claims_by_time(start_time))
        for department in departments:
            department_hpv = [department]
            for start_time, end_time, truck_total in zip(start_times, end_times, truck_totals):
                this_dt = end_time
                start_dt = start_time
                this_dt = pytz.utc.localize(this_dt)
                start_dt = pytz.utc.localize(start_dt)
                if this_dt <= pytz.utc.localize(end_time):  # datetime.now():
                    dept_manhours = Attendance.get_manhours_during(start=start_dt, stop=this_dt, department=department)
                    try:
                        department_hpv.append(dept_manhours / truck_total)
                    except:
                        department_hpv.append(0)
                else:
                    department_hpv.append('')
            hpv_data.append(department_hpv)
        return hpv_data

    def get_context_data(self, **kwargs):
        # When during the hour should we do the headcount?
        context = super().get_context_data(**kwargs)

        if HPVATM.objects.count() == 0:
            return context

        # All day info
        current = HPVATM.objects.latest('timestamp')
        shift1 = HPVATM.objects.filter(shift=1)
        shift2 = HPVATM.objects.filter(shift=2)
        shift3 = HPVATM.objects.filter(shift=3)

        depts = {
            'CIW': {},
            'FCB': {},
            'PNT': {},
            'PCH': {},
            'FCH': {},
            'DAC': {},
            'MAINT': {},
            'QA': {},
            'MAT': {},
            'PLANT': {},
            'CLAIMS': {}
        }

        self.set_day_data(current, context, depts)
        self.set_shift1_data(current, shift1, context, depts)
        self.set_shift2_data(current, shift2, context, depts)
        self.set_shift3_data(current, shift3, context, depts)

        keyorder = ['CIW', 'FCB', 'PNT', 'PCH', 'FCH', 'DAC', 'MAINT', 'QA', 'MAT', 'PLANT', 'CLAIMS']
        context['depts'] = OrderedDict(sorted(depts.items(), key=lambda i:keyorder.index(i[0])))

        return context

    def set_day_data(self, current, context, depts):
        depts['CIW']['d_hpv'] = current.CIW_d_hpv
        depts['FCB']['d_hpv'] = current.FCB_d_hpv
        depts['PNT']['d_hpv'] = current.PNT_d_hpv
        depts['PCH']['d_hpv'] = current.PCH_d_hpv
        depts['FCH']['d_hpv'] = current.FCH_d_hpv
        depts['DAC']['d_hpv'] = current.DAC_d_hpv
        depts['MAINT']['d_hpv'] = current.MAINT_d_hpv
        depts['QA']['d_hpv'] = current.QA_d_hpv
        depts['MAT']['d_hpv'] = current.MAT_d_hpv
        depts['PLANT']['d_hpv'] = current.PLANT_d_hpv
        depts['CLAIMS']['d_hpv'] = current.claims_d


    def set_shift1_data(self, current, shift1, context, depts):
        if not shift1:
            return

        shift1 = shift1.latest('timestamp')
        if not (shift1.timestamp >= current.timestamp - dt.timedelta(hours=17)):
            return

        depts['CIW']['s1_hpv'] = shift1.CIW_s_hpv
        depts['FCB']['s1_hpv'] = shift1.FCB_s_hpv
        depts['PNT']['s1_hpv'] = shift1.PNT_s_hpv
        depts['PCH']['s1_hpv'] = shift1.PCH_s_hpv
        depts['FCH']['s1_hpv'] = shift1.FCH_s_hpv
        depts['DAC']['s1_hpv'] = shift1.DAC_s_hpv
        depts['MAINT']['s1_hpv'] = shift1.MAINT_s_hpv
        depts['QA']['s1_hpv'] = shift1.QA_s_hpv
        depts['MAT']['s1_hpv'] = shift1.MAT_s_hpv
        depts['PLANT']['s1_hpv'] = shift1.PLANT_s_hpv
        depts['CLAIMS']['s1_hpv'] = shift1.claims_s


    def set_shift2_data(self, current, shift2, context, depts):
        if not shift2:
            return

        shift2 = shift2.latest('timestamp')
        if not (shift2.timestamp >= current.timestamp - dt.timedelta(hours=17)):
            return

        depts['CIW']['s2_hpv'] = shift2.CIW_s_hpv
        depts['FCB']['s2_hpv'] = shift2.FCB_s_hpv
        depts['PNT']['s2_hpv'] = shift2.PNT_s_hpv
        depts['PCH']['s2_hpv'] = shift2.PCH_s_hpv
        depts['FCH']['s2_hpv'] = shift2.FCH_s_hpv
        depts['DAC']['s2_hpv'] = shift2.DAC_s_hpv
        depts['MAINT']['s2_hpv'] = shift2.MAINT_s_hpv
        depts['QA']['s2_hpv'] = shift2.QA_s_hpv
        depts['MAT']['s2_hpv'] = shift2.MAT_s_hpv
        depts['PLANT']['s2_hpv'] = shift2.PLANT_s_hpv
        depts['CLAIMS']['s2_hpv'] = shift2.claims_s


    def set_shift3_data(self, current, shift3, context, depts):
        if not shift3:
            shift_3 = False
            context.update({'shift_3': shift_3})
            return

        shift3 = shift3.latest('timestamp')
        if not (shift3.timestamp >= current.timestamp - dt.timedelta(hours=17)):
            return

        depts['CIW']['s3_hpv'] = shift3.CIW_s_hpv
        depts['FCB']['s3_hpv'] = shift3.FCB_s_hpv
        depts['PNT']['s3_hpv'] = shift3.PNT_s_hpv
        depts['PCH']['s3_hpv'] = shift3.PCH_s_hpv
        depts['FCH']['s3_hpv'] = shift3.FCH_s_hpv
        depts['DAC']['s3_hpv'] = shift3.DAC_s_hpv
        depts['MAINT']['s3_hpv'] = shift3.MAINT_s_hpv
        depts['QA']['s3_hpv'] = shift3.QA_s_hpv
        depts['MAT']['s3_hpv'] = shift3.MAT_s_hpv
        depts['PLANT']['s3_hpv'] = shift3.PLANT_s_hpv
        depts['CLAIMS']['s3_hpv'] = shift3.claims_s

        shift_3 = True

        context.update({ 'shift3_total': shift3_total })


class Drip(LoginRequiredMixin, TemplateView):
    template_name = "hpv/drip.html"
    login_url = '/login/'

    def get(self, request):
        context = {}
        if request.GET.get('dripRate'):
            serial_number = get_truck_serial()
            last_truck = Complete.objects.latest('completed')
            prev_time = last_truck.completed

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


def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')

def heatmap(request):
    return render(request, 'hpv/heatmap.html')
