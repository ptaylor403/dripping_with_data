from django.db import models
from hpv.models import Attendance, Complete
# from crys.models import
# Create your models here.

# class AttendanceDripper(models.Model):
#     """docstring for GenericModel"""
#     employee_number = models.IntegerField()
#     department = models.CharField(max_length=16)
#     clock_in_time = models.DateTimeField()
#     clock_out_time = models.DateTimeField(null=True, blank=True)
#     shift = models.CharField(max_length=16)
#     create_at = models.DateTimeField()
#
#     @staticmethod
#     def copy_to_attendance(time)


class CompleteDripper(models.Model):
    serial_number = models.CharField(max_length=10)
    completed = models.DateTimeField()
    create_at = models.DateTimeField()

    @staticmethod
    def create_on_Complete(start, stop):
        relevant = CompleteDripper.objects.filter(create_at__gt=start)
        relevant = relevant.filter(create_at__lte=stop)
        for entry in relevant:
            Complete.objects.create(serial_number=entry.serial_number,
                                    completed=entry.completed)

    @staticmethod
    def load_from_Complete():
        for entry in Complete.objects.all():
            CompleteDripper.objects.create(serial_number=entry.serial_number,
                                           completed=entry.completed,
                                           create_at=entry.completed)
