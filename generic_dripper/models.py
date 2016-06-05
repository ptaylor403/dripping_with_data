from django.db import models
from hpv.models import Attendance, Complete
import datetime as dt
import pytz
from get_data.models import *


class AttendanceDripper(models.Model):
    employee_number = models.IntegerField()
    department = models.CharField(max_length=16)
    clock_in_time = models.DateTimeField()
    clock_out_time = models.DateTimeField(null=True, blank=True)
    shift = models.CharField(max_length=16)
    create_at = models.DateTimeField()
    edit_1_at = models.DateTimeField(null=True)
    target = Attendance
    last_drip = dt.datetime(1, 1, 1, 0, 0, tzinfo=pytz.utc)

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
    def _create_on_target(cls, stop):
        relevant = cls.objects.filter(create_at__gt=cls.last_drip)
        relevant = relevant.filter(create_at__lte=stop)
        for entry in relevant.order_by('pk'):
            cls.target.objects.create(employee_number=entry.employee_number,
                                      department=entry.department,
                                      clock_in_time=entry.clock_in_time,
                                      clock_out_time=None,
                                      shift=entry.shift,)

    @classmethod
    def _edit_1_on_target(cls, stop):
        relevant = cls.objects.filter(edit_1_at__gt=cls.last_drip)
        relevant = relevant.filter(edit_1_at__lte=stop)
        for entry in relevant.order_by('pk'):
            cls.target.objects.filter(employee_number=entry.employee_number,
                                      clock_in_time=entry.clock_in_time).update(
                                      clock_out_time=entry.clock_out_time)

    @classmethod
    def update_target(cls, *args, **kwargs):
        cls._create_on_target(*args, **kwargs)
        cls._edit_1_on_target(*args, **kwargs)
        if "stop" in kwargs:
            stop = kwargs['stop']
        else:
            stop = args[0]
        cls.last_drip = stop


class CompleteDripper(models.Model):
    serial_number = models.CharField(max_length=10)
    completed = models.DateTimeField()
    create_at = models.DateTimeField()
    target = Complete
    last_drip = dt.datetime(1, 1, 1, 0, 0, tzinfo=pytz.utc)

    @classmethod
    def load_from_target(cls):
        for entry in cls.target.objects.order_by('pk'):
            cls.objects.create(serial_number=entry.serial_number,
                               completed=entry.completed,
                               create_at=entry.completed)

    @classmethod
    def _create_on_target(cls, stop):
        relevant = cls.objects.filter(create_at__gt=cls.last_drip)
        relevant = relevant.filter(create_at__lte=stop)
        for entry in relevant.order_by('pk'):
            cls.target.objects.create(serial_number=entry.serial_number,
                                      completed=entry.completed)

    @classmethod
    def update_target(cls, *args, **kwargs):
        cls._create_on_target(*args, **kwargs)
        if "stop" in kwargs:
            stop = kwargs['stop']
        else:
            stop = args[0]
        cls.last_drip = stop


class CombinedDripper:
    drippers = []

    def __init__(self, start_time, time_step=dt.timedelta(minutes=5)):
        self.simulated_time = start_time
        self.time_step = time_step

    def add_dripper(self, dripper):
        if dripper not in self.drippers:
            self.drippers.append(dripper)

    def update_to(self, new_time):
        for dripper in self.drippers:
            dripper.update_target(new_time)
        self.simulated_time = new_time

    def update_by(self, time_step):
        new_time = self.simulated_time + time_step
        self.update_to(new_time)

    def update(self):
        self.update_by(self.time_step)
