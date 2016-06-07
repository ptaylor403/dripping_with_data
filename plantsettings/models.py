from django.db import models
import datetime as dt
import pytz


#Rename to Plant Settings
class PlantSetting(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    plant_code = models.CharField(max_length=3, default="017")
    plant_target = models.IntegerField(default=55)
    num_of_shifts = models.IntegerField(default=2)
    first_shift = models.TimeField(null=True, blank=True)
    second_shift = models.TimeField(null=True, blank=True)
    third_shift = models.TimeField(null=True, blank=True)
    dripper_start = models.DateTimeField(default=dt.datetime(2016, 6, 1, 0, 0, tzinfo=pytz.utc))
