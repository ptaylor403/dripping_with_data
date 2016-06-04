from django.db import models


#Rename to Plant Settings
class PlantSetting(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    plant_code = models.IntegerField()
    plant_target = models.IntegerField()
    num_of_shifts = models.IntegerField()
    first_shift = models.TimeField(null=True, blank=True)
    second_shift = models.TimeField(null=True, blank=True)
    third_shift = models.TimeField(null=True, blank=True)

