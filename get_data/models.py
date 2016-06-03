from django.db import models
import csv

raw_csv_file = '/Users/Nic/TIY/customer-dtna/data/emp+item+punch.csv'

# UNPROCESSED clock in/out data
class RawClockData(models.Model):
    PRSN_NBR_TXT = models.CharField(max_length=100)
    full_nam = models.TextField()
    HM_LBRACCT_FULL_NAM = models.TextField()
    start_rsn_txt = models.CharField(max_length=100)
    PNCHEVNT_IN = models.DateTimeField(null=True)
    end_rsn_txt = models.CharField(max_length=100)
    PNCHEVNT_OUT = models.DateTimeField(null=True)


    # Reads the csv file and
    # passes the row off to process_row
    def csv_reader(self):
        with open(self.csv_file) as f:
            reader = csv.reader(f)
            for row in reader:
                self.process_row(row)

    # takes each rom from csv and
    # clones the information
    def process_row(self, row):
        # catches header row from CSV
        if row[0] == "PRSN_NBR_TXT":
            pass
        else:
            created_row = RawClockData.objects.create(
                PRSN_NBR_TXT=row[0],
                full_nam=row[1],
                HM_LBRACCT_FULL_NAM=row[2],
                start_rsn_txt=row[3],
                PNCHEVNT_IN=row[4],
                end_rsn_txt=row[5],
                PNCHEVNT_OUT=row[6],
            )
            print(row)
            created_row.save()
            print("Created Row")

# Based on the Mount Holly Org Updates 2015 Excel File
class OrgUnits(models.Model):
    dept_name = models.CharField(max_length=255)
    dept_abrv = models.CharField(max_length=5)
    dept_id = models.CharField(max_length=100)


