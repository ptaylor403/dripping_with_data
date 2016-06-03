from django.shortcuts import render
from django.views.generic.base import TemplateView
import datetime
from .data_sim import *
from .models import Attendance, Complete
import random


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
            for day in range(1, 6):
                for hour in range(7, 23):
                    for _ in range(1, random.randint(6, 10)):
                        serial_number = get_truck_serial()
                        completed = get_completed(day, hour)

                        Complete.objects.create(serial_number=serial_number, completed=completed)
            text2 = "5 days worth of data added to the database."
            context['text2'] = text2

        return render(request, self.template_name, context)

class HPV(TemplateView):
    template_name = "hpv/hpv.html"
    # print('object{}'.format(Attendance.objects.filter(clock_out_time=None)))
    # print('PCH{}'.format(Attendance.objects.filter(department='PCH')))

    def get(self, request):
        PCH = Attendance.get_active_at(active_time=datetime.utcnow(), department='PCH')
        FCH = Attendance.get_active_at(department='FCH')
        CIW = Attendance.get_active_at(department='CIW')
        FCB = Attendance.get_active_at(department='FCB')
        PNT = Attendance.get_active_at(department='PNT')
        plant = Attendance.get_active_at()
        context = {'PCH1': PCH, 'PCH2': PCH, 'FCH1': FCH, 'FCH2': FCH,
                   'CIW1': CIW, 'CIW2': CIW, 'FCB1': FCB, 'FCB2': FCB,
                   'PNT1': PNT, 'PNT2': PNT, 'plant1': plant, 'plant2': plant}
        return render(request, self.template_name, context)
