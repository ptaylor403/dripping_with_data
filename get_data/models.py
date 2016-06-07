from django.db import models
from .functions.process_raw_csv_data import *
from .functions.csv_file_paths import *

from datetime import datetime
from datetime import timedelta



"""
This model is intended to hold
all model data for the raw CSV dumps.
"""


class RawClockData(models.Model):
    PRSN_NBR_TXT = models.CharField(max_length=100)
    full_nam = models.TextField()
    HM_LBRACCT_FULL_NAM = models.TextField()
    start_rsn_txt = models.CharField(max_length=100, null=True)
    PNCHEVNT_IN = models.DateTimeField(null=True, blank=True)
    end_rsn_txt = models.CharField(max_length=100, null=True)
    PNCHEVNT_OUT = models.DateTimeField(null=True, blank=True)

    @staticmethod
    def load_raw_data():
        # process generator file. Punch CSV has headers.
        # each row is a dict.
        for row in read_csv_generator(clock_in_out_csv, headers=True):
            created_row = RawClockData.objects.create(
                PRSN_NBR_TXT=row['PRSN_NBR_TXT'],
                full_nam=row['full_nam'],
                HM_LBRACCT_FULL_NAM=row['HM_LBRACCT_FULL_NAM'],
                start_rsn_txt=row['start_rsn_txt'],
                PNCHEVNT_IN=process_date(row['PNCHEVNT_DTM_IN']),
                end_rsn_txt=row['end_rsn_txt'],
                PNCHEVNT_OUT=process_date(row['PNCHEVNT_DTM_OUT']),
            )
            created_row.save()
        print("LOADED Raw Clock Data Row")

    @staticmethod
    def get_plant_man_hours_atm(start, stop=None, by_department=False):
        """
        Static method that calls RawClockedData.get_clocked_in to determine how
        many people are clocked in at the specified time slice.
        :param start: a filter based on when you want to start analyzing manhours
        :param stop:  a filter based on when you want to stop analyzing manhours
        :return: num of employees clocked as int and manhours as a float
        """
        if stop is None:
            stop = datetime.now()

        currently_clocked_in = RawClockData.get_clocked_in(start)

        if by_department:
            for employee in currently_clocked_in:
                pass

        else:
            # Performing calculations on man_hours for the entire plant
            #write in case for max employee clock in and clockout = none
            man_hours = timedelta(hours=0)
            num_employees = currently_clocked_in.count()
            for employee in currently_clocked_in:
                begin = start
                end = stop
                man_hours += end-begin
                man_seconds = man_hours.total_seconds()
                total_man_hours =man_seconds/3600
            return total_man_hours, num_employees

    @staticmethod
    def get_clocked_in(start):
        """
        Filters employees who clocked in before shift time, excluding those who have clocked out from previous shifts
        :param start: the start of time that you want to look at
        :return: filtered objects before the start value
        """
        employees = RawClockData.objects.filter(
            PNCHEVNT_IN__year=start.year,
            PNCHEVNT_IN__month=start.month,
            PNCHEVNT_IN__day=start.day,
            PNCHEVNT_OUT__exact=None,
        ).exclude(end_rsn_txt__exact='&out')

        return employees



class RawDirectRunData(models.Model):
    VEH_SER_NO = models.CharField(max_length=6)
    TS_LOAD = models.DateTimeField()
    SHIFT = models.IntegerField()
    QA = models.IntegerField()
    PAINT = models.IntegerField()
    SH = models.IntegerField()
    ENG_SC = models.IntegerField()

    @staticmethod
    def load_raw_data():
        # process generator file. Punch CSV has headers.
        # each row is a dict.
        for row in read_csv_generator(direct_run_csv, headers=True):
            created_row = RawDirectRunData.objects.create(
                VEH_SER_NO=row['\ufeffVEH_SER_NO'],
                TS_LOAD=process_date(row['TS_LOAD']),
                SHIFT=row['SHIFT'],
                QA=row['QA'],
                PAINT=row['PAINT'],
                SH=row['SH'],
                ENG_SC=row['ENG_SC'],
            )
            created_row.save()
        print("LOADED DIRECT RUN Row")


class RawCrysData(models.Model):
    QA_ITEM_DSCREP_ID = models.CharField(max_length=255)
    QA_INSP_ITEM_ID = models.CharField(max_length=255)
    VEH_SER_NO = models.CharField(max_length=6)
    FOUND_INSP_TEAM = models.CharField(max_length=3)
    INSP_DSCREP_DESC = models.CharField(max_length=255)
    INSP_COMT = models.TextField()
    TS_LOAD = models.DateTimeField()

    @staticmethod
    def load_raw_data():
        # process generator file. Punch CSV has headers.
        # each row is a dict.
        for row in read_csv_generator(crys_csv, headers=True):
            created_row = RawCrysData.objects.create(
                QA_ITEM_DSCREP_ID=row['\ufeffQA_ITEM_DSCREP_ID'],
                QA_INSP_ITEM_ID=row['QA_INSP_ITEM_ID'],
                VEH_SER_NO=row['VEH_SER_NO'],
                FOUND_INSP_TEAM=row['FOUND_INSP_TEAM'],
                INSP_DSCREP_DESC=row['INSP_DSCREP_DESC'],
                INSP_COMT=row['INSP_COMT'],
                TS_LOAD=process_date(row['TS_LOAD']),
            )
            created_row.save()
        print("LOADED crys Row")


class RawPlantActivity(models.Model):
    VEH_SER_NO = models.CharField(max_length=6)
    POOL_TRIG_TYPE = models.CharField(max_length=255)
    TS_LOAD = models.DateTimeField()
    DATE_WORK = models.DateTimeField()

    @staticmethod
    def load_raw_data():
        # process generator file. Punch CSV has headers.
        # each row is a dict.
        for row in read_csv_generator(plant_activty_csv, headers=True):
            temp_date = row['DATE_WORK']
            created_row = RawPlantActivity.objects.create(
                VEH_SER_NO=row['VEH_SER_NO'],
                POOL_TRIG_TYPE=row['POOL_TRIG_TYPE'],
                TS_LOAD=process_date(row['TS_LOAD']),
                DATE_WORK=process_date(row['DATE_WORK']),
            )
            created_row.save()
        print("LOADED plant Row")



    @staticmethod
    def get_claims_date_range(start, stop=None):
        """

        :param start: Datetime object that points to the start of the query
        :param stop: Datetime object or None to slice the view or just get from start to current time
        :return: int of number of trucks produced from start to stop
        """

        if stop == None:
            stop = datetime.now()
        num_trucks = RawPlantActivity.get_claimed_objects_in_range(start, stop)

        # for truck in num_trucks:
        #     print(truck.VEH_SER_NO)

        return num_trucks.count()

    @staticmethod
    def get_claimed_objects_in_range(start, stop):
        """
        returns filtered objects within a range of start, stop
        :param start: Datetime object that points to the start of the query
        :param stop: Datetime object to slice the view
        :return: RawPlantActivity, 'claim', objects

        """
        claimed_objects = RawPlantActivity.objects.filter(
            TS_LOAD__gte=start,
            TS_LOAD__lte=stop,
        )
        return claimed_objects

    @staticmethod
    def get_hpv_at_slice(start, stop):
        """
        Calculates the plants HPV at current slice of time
        :param start: Datetime object that points to the start of the query
        :param stop: Datetime object to slice the view
        :returns: 4 variables in order of HPV, number of claims, current total hours, and current number of employees
        """

        #calls the two methods to get the needed data
        num_claims_at_slice = RawPlantActivity.get_claims_date_range(start, stop)
        total_hours_at_slice, current_num_employees = RawClockData.get_plant_man_hours_atm(start, stop)

        #calculating the HPV
        plant_hpv_at_slice = total_hours_at_slice/num_claims_at_slice

        return plant_hpv_at_slice, num_claims_at_slice, total_hours_at_slice, current_num_employees

    @staticmethod
    def get_department_manhours(employees_obj_from_slice):
        """

        :param employees_obj_from_slice:
        :return:
        """

# Based on the Mount Holly Org Updates 2015 Excel File
class OrgUnits(models.Model):
    dept_name = models.CharField(max_length=255)
    dept_abrv = models.CharField(max_length=5)
    dept_id = models.CharField(max_length=100)
    shift_id = models.CharField(max_length=10)


    # class RawShopCalls(models.Model):
    #     SC_ID = models.CharField(max_length=6)
    #     VEH_SER_NO = models.CharField(max_length=6)
    #
    #     @staticmethod
    #     def load_raw_data():
    #         # process generator file. Punch CSV has headers.
    #         # each row is a dict.
    #         for row in read_csv_generator(shopcalls_csv, headers=True):
    #             print(row)
    #             print('*'*40)
    #             created_row = RawShopCalls.objects.create(
    #                 SC_ID=row['SC_ID'],
    #                 VEH_SER_NO=row['VEH_SER_NO'],
    #             )
    #             created_row.save()
    #         print("LOADED shopcalls Row")
