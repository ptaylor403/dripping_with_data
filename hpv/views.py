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
import sys

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
        # departments = ['CIW', 'FCB', 'PNT', 'PCH', 'FCH', 'DAC', 'MAINT', 'QA', 'MAT']
        # # NOW = the_dripper.simulated_time.replace(tzinfo=None)
        # print("NOW: ", NOW)
        # today = NOW.date()
        # START_TIME1 = 6
        # START_TIME2 = 14
        # # Attendance - by shift and department
        # plant_attendance = HPV._get_plant_history(START_TIME1, today)
        # shift1_attendance = []
        # shift2_attendance = []
        # # HPV - by department and plant wide, by day and shift
        # plant_hpv = RawPlantActivity.get_hpv_at_slice(datetime.combine(today, dt.time(0)), NOW)[0]
        # # Claims - by day and shift
        #
        #
        # context.update({'plant_attendance': plant_attendance, 'plant_hpv':plant_hpv, 'NOW': NOW})



        # if shift == 1:
        #     shift1_total = claims
        #     CIW_s1_hpv = CIW_s_hpv
        #     FCB_s1_hpv = FCB_s_hpv
        #     PNT_s1_hpv = PNT_s_hpv
        #     PCH_s1_hpv = PCH_s_hpv
        #     FCH_s1_hpv = FCH_s_hpv
        #     DAC_s1_hpv = DAC_s_hpv
        #     MAINT_s1_hpv = MAINT_s_hpv
        #     QA_s1_hpv = QA_s_hpv
        #     MAT_s1_hpv = MAT_s_hpv
        #     PLANT_s1_hpv = PLANT_s_hpv
        # if shift == 2:
        #     shift2_total = claims
        #     CIW_s2_hpv = CIW_s_hpv
        #     FCB_s2_hpv = FCB_s_hpv
        #     PNT_s2_hpv = PNT_s_hpv
        #     PCH_s2_hpv = PCH_s_hpv
        #     FCH_s2_hpv = FCH_s_hpv
        #     DAC_s2_hpv = DAC_s_hpv
        #     MAINT_s2_hpv = MAINT_s_hpv
        #     QA_s2_hpv = QA_s_hpv
        #     MAT_s2_hpv = MAT_s_hpv
        #     PLANT_s2_hpv = PLANT_s_hpv
        # if shift == 3:
        #     shift_3 = True
        #     shift3_total = claims
        #     CIW_s3_hpv = CIW_s_hpv
        #     FCB_s3_hpv = FCB_s_hpv
        #     PNT_s3_hpv = PNT_s_hpv
        #     PCH_s3_hpv = PCH_s_hpv
        #     FCH_s3_hpv = FCH_s_hpv
        #     DAC_s3_hpv = DAC_s_hpv
        #     MAINT_s3_hpv = MAINT_s_hpv
        #     QA_s3_hpv = QA_s_hpv
        #     MAT_s3_hpv = MAT_s_hpv
        #     PLANT_s3_hpv = PLANT_s_hpv
        # else:
        #     shift_3 = False
        #
        # context.update({'shift1_total': shift1_total, 'shift2_total': shift2_total, 'shift3_total': shift3_total,
        #                 'CIW_s1_hpv': CIW_s1_hpv, 'CIW_s2_hpv': CIW_s2_hpv, 'CIW_s3_hpv': CIW_s3_hpv,
        #                 'FCB_s1_hpv': FCB_s1_hpv, 'FCB_s2_hpv': FCB_s2_hpv, 'FCB_s3_hpv': FCB_s3_hpv,
        #                 'PNT_s1_hpv': PNT_s1_hpv, 'PNT_s2_hpv': PNT_s2_hpv, 'PNT_s3_hpv': PNT_s3_hpv,
        #                 'PCH_s1_hpv': PCH_s1_hpv, 'PCH_s2_hpv': PCH_s2_hpv, 'PCH_s3_hpv': PCH_s3_hpv,
        #                 'FCH_s1_hpv': FCH_s1_hpv, 'FCH_s2_hpv': FCH_s2_hpv, 'FCH_s3_hpv': FCH_s3_hpv,
        #                 'DAC_s1_hpv': DAC_s1_hpv, 'DAC_s2_hpv': DAC_s2_hpv, 'DAC_s3_hpv': DAC_s3_hpv,
        #                 'MAINT_s1_hpv': MAINT_s1_hpv, 'MAINT_s2_hpv': MAINT_s2_hpv, 'MAINT_s3_hpv': MAINT_s3_hpv,
        #                 'QA_s1_hpv': QA_s1_hpv, 'QA_s2_hpv': QA_s2_hpv, 'QA_s3_hpv': QA_s3_hpv,
        #                 'MAT_s1_hpv': MAT_s1_hpv, 'MAT_s2_hpv': MAT_s2_hpv, 'MAT_s3_hpv': MAT_s3_hpv,
        #                 'PLANT_s1_hpv': PLANT_s1_hpv, 'PLANT_s2_hpv': PLANT_s2_hpv, 'PLANT_s3_hpv': PLANT_s3_hpv,
        #                 'shift_3': shift_3})




        # today = datetime.today().date()
        # START_TIME1 = 6
        # START_TIME2 = 14
        # shift_1 = HPV._get_shift_history(departments, START_TIME1, today)
        # shift_2 = HPV._get_shift_history(departments, START_TIME2, today)
        # shift1_manhours = HPV._get_shift_manhour_history(departments, START_TIME1, today)
        # shift2_manhours = HPV._get_shift_manhour_history(departments, START_TIME2, today)
        # day_total = Complete.claims_by_time(NOW)  # datetime.now())
        # shift_1_time = dt.datetime.combine(NOW.date(), dt.time(START_TIME2 + 1, 30))
        # shift_1_total = Complete.claims_by_time(shift_1_time)
        # print("Shift 1 total: ", shift_1_total)
        # hour_delta = dt.timedelta(hours=1)
        # hour_ago = NOW - hour_delta  # datetime.now() - hour_delta
        # hour_total = day_total - Complete.claims_by_time(hour_ago)
        # shift1_time = dt.datetime.combine(NOW.date(), dt.time(START_TIME2 + 1, 30))
        # shift1_total = Complete.claims_by_time(shift1_time)
        # shift2_total = day_total - shift1_total
        # day_start = datetime.combine(today, dt.time(START_TIME1))
        # day_start = pytz.utc.localize(day_start)
        # day_man_hours = Attendance.get_manhours_during(start=day_start, stop=pytz.utc.localize(NOW))
        # try:
        #     day_HPV = day_man_hours / day_total
        # except:
        #     day_HPV = 0
        # start_time1 = datetime.combine(today, dt.time(START_TIME1))
        # start_time2 = datetime.combine(today, dt.time(START_TIME2))
        # hpv_data = HPV._get_department_hpv(departments, start_time1, start_time2, NOW)


        # last_hpv = 0
        # try:
        #     last_hpv = HPVATM.objects.latest('timestamp')
        # except:
        #     HPVATM.objects.create(hpv_plant=day_HPV)
        #     last_hpv = HPVATM.objects.latest('timestamp')
        # if (pytz.utc.localize(dt.datetime.now()) - last_hpv.timestamp) > dt.timedelta(minutes=5):
        #     HPVATM.objects.create(hpv_plant=day_HPV)


        # context.update({'shift_1': shift_1, 'shift_2': shift_2,
        #                 "manhours_1": shift1_manhours, "manhours_2": shift2_manhours,
        #                 'hour_total': hour_total, 'day_total': day_total, 'time': NOW,
        #                 "day_HPV": day_HPV, 'hpv_data': hpv_data})
        return context


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
