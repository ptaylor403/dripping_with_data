from django.shortcuts import render
from django.views.generic.base import TemplateView
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
        first_info = list(Attendance.objects.filter(clock_out_time=None, shift='first'))
        PCH1 = 0
        FCH1 = 0
        CIW1 = 0
        FCB1 = 0
        PNT1 = 0
        plant1 = 0
        if first_info:
            for person in first_info:
                if person.department == 'PCH':
                    PCH1 += 1
                elif person.department == 'FCH':
                    FCH1 += 1
                elif person.department == 'CIW':
                    CIW1 += 1
                elif person.department == 'FCB':
                    FCB1 += 1
                elif person.department == 'PNT':
                    PNT1 += 1
            plant1 = PCH1 + FCH1 + CIW1 + FCB1 + PNT1

        second_info = list(Attendance.objects.filter(clock_out_time=None, shift='second'))
        PCH2 = 0
        FCH2 = 0
        CIW2 = 0
        FCB2 = 0
        PNT2 = 0
        plant2 = 0
        if second_info:
            for person in second_info:
                if person.department == 'PCH':
                    PCH2 += 1
                elif person.department == 'FCH':
                    FCH2 += 1
                elif person.department == 'CIW':
                    CIW2 += 1
                elif person.department == 'FCB':
                    FCB2 += 1
                elif person.department == 'PNT':
                    PNT2 += 1
            plant2 = PCH2 + FCH2 + CIW2 + FCB2 + PNT2

        context = {'PCH1': PCH1, 'PCH2': PCH2, 'FCH1': FCH1, 'FCH2': FCH2,
                   'CIW1': CIW1, 'CIW2': CIW2, 'FCB1': FCB1, 'FCB2': FCB2,
                   'PNT1': PNT1, 'PNT2': PNT2, 'plant1': plant1, 'plant2': plant2}
        return render(request, self.template_name, context)
