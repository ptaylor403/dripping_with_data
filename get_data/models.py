from django.db import models
from .functions.process_raw_csv_data import *
from .functions.csv_file_paths import *
import datetime

from datetime import datetime

"""
This model is intended to hold
all model data for the raw CSV dumps.
"""


class RawClockData(models.Model):
    PRSN_NBR_TXT = models.CharField(max_length=100)
    full_nam = models.TextField()
    HM_LBRACCT_FULL_NAM = models.TextField()
    start_rsn_txt = models.CharField(max_length=100, blank=True)
    PNCHEVNT_IN = models.DateTimeField(null=True, blank=True)
    end_rsn_txt = models.CharField(max_length=100, blank=True)
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
    def get_plant_man_hours_atm(start, stop=None):
        """

        :param start: a filter based on when you want to start analyzing manhours
        :param stop:  a filter based on when you want to stop analyzing manhours
        :return: Man_hours based on employees in and out during the given time
            frame
        """
        if stop is None:
            stop = datetime.now()

        currently_clocked_in = RawClockData.get_clocked_in_before_stop(stop)
        clocked_in_after_start = RawClockData.get_clocked_in_after_start(start)
        clocked_out_after_start = RawClockData.get_clocked_out_after_start(start)

        # Filtering employees who didn't clock out after timeframe
        clocked_out_during_time_period = clocked_out_after_start.filter(PNCHEVNT_OUT__lt=stop)
        # creates a query set of the filters objects
        all_relevent = currently_clocked_in | clocked_in_after_start | clocked_out_during_time_period
        print('-' * 50)
        print(all_relevent.count())

        # Performing actual calculations on man_hours
        man_hours = 0
        for employee in all_relevent:
            begin = max(employee.PNCHEVNT_IN, start)
            end = min(employee.PNCHEVNT_OUT, stop)
            man_hours += ((end - begin).total_seconds()) / 3600
            print('-' * 50)
            print('MANHOURS =', man_hours)
        return man_hours


    @staticmethod
    def get_clocked_in_before_stop(stop):
        """
        Filters employees who clocked in before shift time, exluding those who
        have clocked out
        :param stop: the start of time that you want to look at
        :return: filtered objects before the start value
        """
        return RawClockData.objects.filter(PNCHEVNT_IN__lt=stop).exclude(PNCHEVNT_OUT__lt=start)


    @staticmethod
    def get_clocked_in_after_start(start):
        """
        Filtering employees who came in after the start of this shift
        :param start: the start of time that you want to look at
        :return: filtered objects after the start value
        """
        return RawClockData.objects.filter(PNCHEVNT_IN__gte=datetime.date(start)).exclude(PNCHEVNT_IN__lt=start)


    @staticmethod
    def get_clocked_out_after_start(start):
        """
        Filtering employees who clocked out after the start
        :param start: the start of time that you want to look at
        :return: filtered objects after the start value
        """
        return RawClockData.objects.filter(PNCHEVNT_OUT__gt=start)


    def currently_clocked_in(self):
        pass


    @staticmethod
    def get_department(HM_LBRACCT_FULL_NAM):
        departments = []
        if RawClockData.objects.filter(HM_LBRACCT_FULL_NAM__startswith='017.10000'):
            CIW = list(RawClockData.objects.filter(HM_LBRACCT_FULL_NAM__startswith='017.10000'))
            departments.append(CIW)
        if RawClockData.objects.filter(HM_LBRACCT_FULL_NAM__startswith='017.20000'):
            FCB = list(RawClockData.objects.filter(HM_LBRACCT_FULL_NAM__startswith='017.20000'))
            departments.append(FCB)
        if RawClockData.objects.filter(HM_LBRACCT_FULL_NAM__startswith='017.30000'):
            PNT = list(RawClockData.objects.filter(HM_LBRACCT_FULL_NAM__startswith='017.30000'))
            departments.append(PNT)
        if RawClockData.objects.filter(HM_LBRACCT_FULL_NAM__startswith='017.40000'):
            PCH = list(RawClockData.objects.filter(HM_LBRACCT_FULL_NAM__startswith='017.40000'))
            departments.append(PCH)
        if RawClockData.objects.filter(HM_LBRACCT_FULL_NAM__startswith='017.50000'):
            FCH = list(RawClockData.objects.filter(HM_LBRACCT_FULL_NAM__startswith='017.50000'))
            departments.append(FCH)
        if RawClockData.objects.filter(HM_LBRACCT_FULL_NAM__startswith='017.60000'):
            DAC = list(RawClockData.objects.filter(HM_LBRACCT_FULL_NAM__startswith='017.60000'))
            departments.append(DAC)
        if RawClockData.objects.filter(HM_LBRACCT_FULL_NAM__startswith='017.70000'):
            MAINT = list(RawClockData.objects.filter(HM_LBRACCT_FULL_NAM__startswith='017.70000'))
            departments.append(MAINT)
        if RawClockData.objects.filter(HM_LBRACCT_FULL_NAM__startswith='017.80000'):
            QA = list(RawClockData.objects.filter(HM_LBRACCT_FULL_NAM__startswith='017.80000'))
            departments.append(QA)
        if RawClockData.objects.filter(HM_LBRACCT_FULL_NAM__startswith='017.90000'):
            MAT = list(RawClockData.objects.filter(HM_LBRACCT_FULL_NAM__startswith='017.90000'))
            departments.append(MAT)
        return departments


    @staticmethod
    def get_manhours_during(start, stop=None, department='all', shift='all'):

        if stop is None:
            stop = datetime.datetime.now()
        if shift == 'all':
            this_shift = RawClockData.objects.all()
        else:
            this_shift = RawClockData.objects.filter(shift=shift)
        if department == 'all' or department == 'plant':
            in_department = this_shift
        else:
            in_department = this_shift.filter(department=department)
        were_clocked_in = in_department.filter(PNCHEVNT_IN__lt=start).exclude(PNCHEVNT_OUT__lt=start)
        clocked_in_after_start = in_department.filter(PNCHEVNT_IN__gte=start)
        clocked_in_during = clocked_in_after_start.filter(PNCHEVNT_IN__lt=stop)
        clocked_out_after_start = in_department.filter(PNCHEVNT_OUT__gte=start)
        clocked_out_during = clocked_out_after_start.filter(PNCHEVNT_OUT__lt=stop)
        all_relevent = were_clocked_in | clocked_in_during | clocked_out_during

        manhours = 0
        for employee in all_relevent:
            begin = max(employee.PNCHEVNT_IN, start)
            if employee.PNCHEVNT_OUT == None:
                end = stop
            else:
                end = min(employee.PNCHEVNT_OUT, stop)
            manhours += ((end - begin).total_seconds())/3600
        return manhours


    @staticmethod
    def get_active_at(active_time=None, department='all', shift='all'):
        if active_time is None:
            active_time = datetime.datetime.now()
        if shift == 'all':
            this_shift = RawClockData.objects.all()
        else:
            this_shift = RawClockData.objects.filter(shift=shift)
        if department == 'all' or department == 'plant':
            in_department = this_shift
        else:
            in_department = this_shift.filter(department=department)
        have_clocked_in = in_department.filter(PNCHEVNT_IN__lt=active_time)
        not_clocked_out_yet = have_clocked_in.filter(PNCHEVNT_OUT__gt=active_time)
        never_clocked_out = have_clocked_in.filter(PNCHEVNT_OUT=None)
        not_clocked_out = not_clocked_out_yet | never_clocked_out
        return not_clocked_out.count()

    # def is_ot(self, time_in_question=None):
    #     if time_in_question is None:
    #         time_in_question = datetime.datetime.now().time()
    #     if self.shift == 0:
    #         if not self.PNCHEVNT_OUT and time_in_question > datetime.time(14, 30):
    #             return True
    #         else:
    #             return False
    #     else:
    #         if not self.PNCHEVNT_OUT and time_in_question > datetime.time(22, 30):
    #             return True
    #         else:
    #             return False


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
        print("LOADED crys Row")


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