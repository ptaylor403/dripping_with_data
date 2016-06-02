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
