from django.db import models

# Capture clock in / clock out data
class ClockData(models.Model):
    PLANT_DECODER = (
        (17, 'MTH'),
    )
    emp_id = models.IntegerField(primary_key=True)
    full_name = models.TextField()
    plant_id = models.IntegerField(choices=PLANT_DECODER)
    dept_id = models.IntegerField()
    shift = models.IntegerField()
    clock_in = models.DateTimeField()
    clock_out = models.DateTimeField()
    clock_in_flag = models.CharField(max_length=255)
    clock_out_flag = models.CharField(max_length=255)

# Based on the Mount Holly Org Updates 2015 Excel File
class OrgUnits(models.Model):
    dept_name = models.CharField(max_length=255)
    dept_abrv = models.CharField(max_length=5)
    dept_id = models.CharField(max_length=100)


