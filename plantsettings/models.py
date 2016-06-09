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


    @staticmethod
    def set_timezone(plant_code, datetime_obj):
        """
        Takes in a plant code, datetime object to return plant specific timezone
        :param plant_code: string of the 3 digit plant code
        :param datetime_obj_naive:
        :return: returns datetime with timezone information
        """

        if plant_code == '017':
            return pytz.timezone('US/Eastern').localize(datetime_obj)


    @staticmethod
    def convert_datetime_to_utc(datetime_obj):
        """

        :param datetime_obj: assumes datetime coming in.
        :return:
        """

        try: #if timezone aware
            out = datetime_obj.astimezone(pytz.utc)

        except (ValueError, TypeError) as exc: #not timezone aware
            local = pytz.timezone('US/Eastern')
            out = datetime_obj.replace(tzinfo='US/Eastern')
            #convert to UTC
            utc_timezone = pytz.timezone('UTC')
            return out.replace(tzinfo=pytz.utc)

        return out


