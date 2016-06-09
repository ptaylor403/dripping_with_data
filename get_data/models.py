from django.db import models
from .functions.process_raw_csv_data import *
from .functions.csv_file_paths import *
import datetime

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
        many people are clocked in from specified start. Usage,'new truck claimed',
            start = start of shift and stop is the datetime of the new truck claim.
        This is not intended to provide a time slice to look at previous entries.
        :param start: a filter based on when you want to start analyzing manhours
        :param stop:  a filter based on when you want to stop analyzing manhours.

        :return: dictionary of departments, plant, total man_hours
        RETURN DICT is structured by dept_mh and dept_ne.
        'mh' = manhours for that dept
        '
        """
        man_hours_by_dept_dict = {
            'CIW_mh': 0,
            'CIW_ne': 0,
            'FCB': 0,
            'PNT': 0,
            'PCH': 0,
            'FCH': 0,
            'DAC': 0,
            'MAINT': 0,
            'QA': 0,
            'MAT': 0,
            'OTHER': 0,
            'PLANT': 0,
            'total_man_hours':0,
        }

        if stop is None:
            stop = datetime.now()

        currently_clocked_in = RawClockData.get_clocked_in(start)


        if by_department:
            for employee in currently_clocked_in:
                emp_plant, emp_dept, emp_shift = RawClockData.process_department(employee.HM_LBRACCT_FULL_NAM)
                if emp_dept in man_hours_by_dept_dict:
                    by_dept_clocked_in[emp_dept] += 1
                by_dept_clocked_in['PLANT'] += 1

        else:
            # Performing calculations on man_hours for the entire plant
            # write in case for max employee clock in and clockout = none
            man_hours = timedelta(hours=0)
            num_employees = currently_clocked_in.count()
            total_man_hours = man_hours
            for employee in currently_clocked_in:

                # TODO begin defined twice here
                begin = max(employee.PNCHEVNT_IN, start)
                begin = start
                end = stop
                man_hours += end - begin
                man_seconds = man_hours.total_seconds()

                total_man_hours = man_seconds / 3600
            return by_dept_clocked_in



    @staticmethod
    def get_clocked_in(start):
        """
        Filters employees who clocked in before shift time, excluding those who have clocked out from previous shifts
        :param start: the start of time that you want to look at
        :return: filtered objects before the start value
        """
        employees = RawClockData.objects.filter(
            PNCHEVNT_IN__gte=start
        )

        return employees

    @staticmethod
    def process_department(dept_string):
        """
        Analyzes which department, plant, and shift that employee belongs too.
        :param dept_string: expects a string from column HM_LBRACCT_FULL_NAM that looks like '017.30000.00.51.05/1/-/017.P000051/-/-/-'
        :return: plant_code, dept, and shift as strings
        """
        dept_dict = {
            '1': 'CIW',
            '2': 'FCB',
            '3': 'PNT',
            '4': 'PCH',
            '5': 'FCH',
            '6': 'DAC',
            '7': 'MAINT',
            '8': 'QA',
            '9': 'MAT',
        }

        regex_dict = {'shift': "/([1-9])/"}
        plant_code = dept_string[:3]

        emp_dept_code = dept_string[4:5]

        if emp_dept_code in dept_dict:
            dept = dept_dict[emp_dept_code]
        else:
            dept = 'OTHER'

        regex_compiled = re.compile(regex_dict['shift'])
        shift = re.findall(regex_compiled, dept_string)[0]


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
        # process generator file. CSV has headers.
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
        # process generator file. CSV has headers.
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
    POOL_CD = models.CharField(max_length=10, null=True)



    @staticmethod
    def load_raw_data():
        # process generator file. CSV has headers.
        # each row is a dict.
        for row in read_csv_generator(plant_activty_csv, headers=True):
            created_row = RawPlantActivity.objects.create(
                VEH_SER_NO=row['VEH_SER_NO'],
                POOL_CD=row['POOL_CD'],
                DATE_WORK=row['DATE_WORK'],
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
