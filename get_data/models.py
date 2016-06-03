from django.db import models
import csv
from datetime import datetime

raw_csv_file = '/Users/Nic/TIY/customer-dtna/data/emp+item+punch.csv'
date_format = '%Y-%m-%d %H:%M:%S.%f'
#6/1/2016  10:10:00 PM

# UNPROCESSED clock in/out data
class RawClockData(models.Model):
    PRSN_NBR_TXT = models.CharField(max_length=100)
    full_nam = models.TextField()
    HM_LBRACCT_FULL_NAM = models.TextField()
    start_rsn_txt = models.CharField(max_length=100)
    PNCHEVNT_IN = models.DateTimeField(null=True, blank=True)
    end_rsn_txt = models.CharField(max_length=100)
    PNCHEVNT_OUT = models.DateTimeField(null=True, blank=True)

    # Reads the csv file and
    # passes the row off to process_row
    @staticmethod
    def csv_reader():
        with open(raw_csv_file) as f:
            reader = csv.reader(f)
            for row in reader:
                print(row)
                RawClockData.process_row(row)


    # takes each rom from csv and
    # clones the information
    @staticmethod
    def process_row(row):
        # catches header row from CSV
        if row[0] == "\ufeffPRSN_NBR_TXT":
            pass
        else:
            processed_clockin_date = RawClockData.process_date(row[4])
            processed_clockout_date = RawClockData.process_date(row[4])

            created_row = RawClockData.objects.create(
                PRSN_NBR_TXT=row[0],
                full_nam=row[1],
                HM_LBRACCT_FULL_NAM=row[2],
                start_rsn_txt=row[3],
                PNCHEVNT_IN=processed_clockin_date,
                end_rsn_txt=row[5],
                PNCHEVNT_OUT=processed_clockout_date,
            )

            print(row)
            created_row.save()
            print("Created Row")

    @staticmethod
    def process_date(date_string):
        if date_string == "NULL":
            return None
        else:
            date_object = datetime.strptime(date_string, date_format)
            mod_date = date_object.strftime('%Y-%m-%d %H:%M:%S')
            print("-"*50)
            print(mod_date)
            return date_object.strftime('%Y-%m-%d %H:%M:%S')


# Based on the Mount Holly Org Updates 2015 Excel File
class OrgUnits(models.Model):
    dept_name = models.CharField(max_length=255)
    dept_abrv = models.CharField(max_length=5)
    dept_id = models.CharField(max_length=100)
