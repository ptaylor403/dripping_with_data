from django.db import models


class Attendance(models.Model):
    employee_number = models.IntegerField()
    department = models.CharField(max_length=16)
    clock_in_time = models.DateTimeField()
    clock_out_time = models.DateTimeField(null=True, blank=True)
    shift = models.CharField(max_length=16)


class Complete(models.Model):
    serial_number = models.CharField(max_length=10)
    completed = models.DateTimeField()
