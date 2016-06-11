from django.db import models
from django.utils import timezone
import datetime as dt


# Rename to Plant Settings
class PlantSetting(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    plant_code = models.CharField(max_length=3, default="017")
    plant_target = models.IntegerField(default=55)
    num_of_shifts = models.IntegerField(default=2)
    first_shift = models.TimeField(default=dt.time(6, 30), null=True, blank=True)
    second_shift = models.TimeField(default=dt.time(14, 30), null=True, blank=True)
    third_shift = models.TimeField(null=True, blank=True)
    with timezone.override("US/Eastern"):
        dripper_start = models.DateTimeField(default=timezone.make_aware(dt.datetime(2016, 4, 1, 0, 0)))
