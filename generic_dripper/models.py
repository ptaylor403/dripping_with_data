from django.db import models
from hpv.models import Attendance, Complete
# from crys.models import


class AttendanceDripper(models.Model):
    employee_number = models.IntegerField()
    department = models.CharField(max_length=16)
    clock_in_time = models.DateTimeField()
    clock_out_time = models.DateTimeField(null=True, blank=True)
    shift = models.CharField(max_length=16)
    create_at = models.DateTimeField()
    edit_1_at = models.DateTimeField(null=True)
    target = Attendance

# Model._meta.get_all_field_names()

    @classmethod
    def load_from_target(cls):
        for entry in cls.target.objects.all():
            AttendanceDripper.objects.create(employee_number=entry.employee_number,
                                             department=entry.department,
                                             clock_in_time=entry.clock_in_time,
                                             clock_out_time=entry.clock_out_time,
                                             shift=entry.shift,
                                             create_at=entry.clock_in_time,
                                             edit_1_at=entry.clock_out_time)

    @classmethod
    def create_on_target(cls, start, stop):
        relevant = cls.objects.filter(create_at__gt=start)
        relevant = relevant.filter(create_at__lte=stop)
        for entry in relevant.order_by('pk'):
            cls.target.objects.create(employee_number=entry.employee_number,
                                      department=entry.department,
                                      clock_in_time=entry.clock_in_time,
                                      clock_out_time=None,
                                      shift=entry.shift,)

    @classmethod
    def edit_1_on_target(cls, start, stop):
        relevant = cls.objects.filter(edit_1_at__gt=start)
        relevant = relevant.filter(edit_1_at__lte=stop)
        for entry in relevant.order_by('pk'):
            cls.target.objects.filter(employee_number=entry.employee_number,
                                      clock_in_time=entry.clock_in_time).update(
                                      clock_out_time=entry.clock_out_time)

    @classmethod
    def update_target(cls, *args, **kwargs):
        cls.create_on_target(*args, **kwargs)
        cls.edit_1_on_target(*args, **kwargs)


class CompleteDripper(models.Model):
    serial_number = models.CharField(max_length=10)
    completed = models.DateTimeField()
    create_at = models.DateTimeField()
    target = Complete

    @classmethod
    def load_from_target(cls):
        for entry in cls.target.objects.order_by('pk'):
            cls.objects.create(serial_number=entry.serial_number,
                               completed=entry.completed,
                               create_at=entry.completed)

    @classmethod
    def create_on_target(cls, start, stop):
        relevant = cls.objects.filter(create_at__gt=start)
        relevant = relevant.filter(create_at__lte=stop)
        for entry in relevant.order_by('pk'):
            cls.target.objects.create(serial_number=entry.serial_number,
                                      completed=entry.completed)
