from django.shortcuts import render
from django.views.generic.base import TemplateView
from .attendance_sim import *
from .models import Attendance


class Load(TemplateView):
    template_name = "hpv/load.html"

    def get(self, request):
        shift_starts = [6, 2]
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

                    if day == 5 and hour == 2:
                        time_out = None
                    else:
                        time_out = clock_out(day, hour)

                    Attendance.objects.create(employee_number=emp,
                                              department=dept,
                                              clock_in_time=time_in,
                                              clock_out_time=time_out,
                                              shift=shift)

        text = "5 days worth of data added to the database. Refreshing the page will add more data."
        context = {'text': text}

        return render(request, self.template_name, context)

class HPV(TemplateView):
    template_name = "hpv/hpv.html"
    # print('object{}'.format(Attendance.objects.filter(clock_out_time=None)))
    # print('PCH{}'.format(Attendance.objects.filter(department='PCH')))

    def get(self, request):
        info = list(Attendance.objects.filter(clock_out_time=None))
        if info:
            PCH = 0
            FCH = 0
            CIW = 0
            FCB = 0
            for person in info:
                if person.department == 'PCH':
                    PCH += 1
                elif person.department == 'FCH':
                    FCH += 1
                elif person.department == 'CIW':
                    CIW += 1
                elif person.department == 'FCB':
                    FCB += 1

        context = {'PCH': PCH, 'FCH': FCH, 'CIW': CIW, 'FCB': FCB}
        return render(request, self.template_name, context)
