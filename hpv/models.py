from django.db import models
import datetime

class Attendance(models.Model):
    employee_number = models.IntegerField()
    department = models.CharField(max_length=16)
    clock_in_time = models.DateTimeField()
    clock_out_time = models.DateTimeField(null=True, blank=True)
    shift = models.CharField(max_length=16)


    # @staticmethod
    # def get_clocked_in():
    #     clocked_in = Employees.objects.order_by('clock_in_time')
    #     clocked_out = Employees.objects.order_by('clock_out_time').distinct('clock_out_time')
    #     num_clocked_in = len(clocked_in) - len(clocked_out)+1
    #
    #     Tracking.objects.create(num_clocked_in=num_clocked_in)
    #
    # def __str__(self):
    #     return "I'm Employee # {}".format(self.employee_num)

    @staticmethod
    def get_active_at(active_time=None, department='all'):
        if active_time is None:
            active_time = datetime.datetime.now()
            print("was none")
        if department == 'all':
            in_department = Attendance.objects.all()
        else:
            in_department = Attendance.objects.filter(department=department)
        print(active_time)
        print("in dept: ", in_department.count())
        have_clocked_in = in_department.filter(clock_in_time__lt=active_time)
        print("clocked in: ", have_clocked_in.count())
        not_clocked_out_yet = have_clocked_in.filter(clock_out_time__gt=active_time)
        print("not clocked out: ", not_clocked_out_yet.count())
        never_clocked_out = have_clocked_in.filter(clock_out_time=None)
        not_clocked_out = not_clocked_out_yet | never_clocked_out
        return not_clocked_out.count()

    def is_ot(self, time_in_question=None):
        if time_in_question is None:
            time_in_question = datetime.datetime.now().time()
        if self.shift == 0:
            if not self.clock_out_time and time_in_question > datetime.time(14, 30):
                return True
            else:
                return False
        else:
            if not self.clock_out_time and time_in_question > datetime.time(22, 30):
                return True
            else:
                return False
