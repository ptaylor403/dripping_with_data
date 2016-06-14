from django.db import models
from .functions.process_raw_csv_data import *
from .functions.csv_file_paths import *
import datetime
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
import re


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
        # process generator file. CSV has headers.
        # each row is a dict.
        with timezone.override('US/Eastern'):
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

# Claims Data
class RawPlantActivity(models.Model):
    VEH_SER_NO = models.CharField(max_length=6)
    TS_LOAD = models.DateTimeField()
    POOL_CD = models.CharField(max_length=10)

    @staticmethod
    def load_raw_data():
        # process generator file. CSV has headers.
        # each row is a dict.
        with timezone.override('US/Pacific'):
            for row in read_csv_generator(plant_activty_csv, headers=True):
                created_row = RawPlantActivity.objects.create(
                    VEH_SER_NO=row['VEH_SER_NO'],
                    POOL_CD=row['POOL_CD'],
                    TS_LOAD=process_date(row['TS_LOAD']),
                )

                created_row.save()
            print("LOADED plant Row")

# Based on the Mount Holly Org Updates 2015 Excel File
class OrgUnits(models.Model):
    DEPT_NAME = models.CharField(max_length=255)
    DEPT_ABRV = models.CharField(max_length=5)
    DEPT_ID = models.CharField(max_length=100)
    SHIFT_ID = models.CharField(max_length=10)

    @staticmethod
    def load_raw_data():
        # process generator file. CSV has headers.
        # each row is a dict.
        for row in read_csv_generator(departments_csv, headers=True):
            created_row = OrgUnits.objects.create(
                DEPT_NAME=row['Name'],
                DEPT_ABRV=row['dept_abvr'],
                DEPT_ID=row['Shift'],
                SHIFT_ID=row['shift_id'],
            )
            created_row.save()
        print("LOADED Department List Row")

#######################################################
# Unused models
#######################################################
# class RawDirectRunData(models.Model):
#     VEH_SER_NO = models.CharField(max_length=6)
#     TS_LOAD = models.DateTimeField()
#     SHIFT = models.IntegerField()
#     QA = models.IntegerField()
#     PAINT = models.IntegerField()
#     SH = models.IntegerField()
#     ENG_SC = models.IntegerField()
#
#     @staticmethod
#     def load_raw_data():
#         # process generator file. CSV has headers.
#         # each row is a dict.
#         raise Exception("Timezone needed")
#         for row in read_csv_generator(direct_run_csv, headers=True):
#             created_row = RawDirectRunData.objects.create(
#                 VEH_SER_NO=row['\ufeffVEH_SER_NO'],
#                 TS_LOAD=process_date(row['TS_LOAD']),
#                 SHIFT=row['SHIFT'],
#                 QA=row['QA'],
#                 PAINT=row['PAINT'],
#                 SH=row['SH'],
#                 ENG_SC=row['ENG_SC'],
#             )
#             created_row.save()
#         print("LOADED DIRECT RUN Row")
#
#
# class RawCrysData(models.Model):
#     QA_ITEM_DSCREP_ID = models.CharField(max_length=255)
#     QA_INSP_ITEM_ID = models.CharField(max_length=255)
#     VEH_SER_NO = models.CharField(max_length=6)
#     FOUND_INSP_TEAM = models.CharField(max_length=3)
#     INSP_DSCREP_DESC = models.CharField(max_length=255)
#     INSP_COMT = models.TextField()
#     TS_LOAD = models.DateTimeField()
#
