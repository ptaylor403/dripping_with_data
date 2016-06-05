from django.db import models
from .functions.process_raw_csv_data import *
from .functions.csv_file_paths import *


"""
This model is intended to hold
all model data for the raw CSV dumps.
"""


class RawClockData(models.Model):
    PRSN_NBR_TXT = models.CharField(max_length=100)
    full_nam = models.TextField()
    HM_LBRACCT_FULL_NAM = models.TextField()
    start_rsn_txt = models.CharField(max_length=100)
    PNCHEVNT_IN = models.DateTimeField(null=True, blank=True)
    end_rsn_txt = models.CharField(max_length=100)
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
