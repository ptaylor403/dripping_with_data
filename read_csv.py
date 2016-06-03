import csv
from .models import RawClockData


class ProcessEmployee():

    """Requires a csv_file_path
    in order to process data"""
    def __init__(self):
        self.csv_file = '/Users/Nic/TIY/customer-dtna/data/emp+item+punch.csv'
        self.csv_reader()

    #Reads the csv file and passes the row off to process_row
    def csv_reader(self):
        with open(self.csv_file) as f:
            reader = csv.reader(f)
            for row in reader:
                self.process_row(row)

    #takes each rom from csv and
    # clones the information
    def process_row(self, row):
        #catches header row from CSV
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
            created_row.save()
            print("Created Row")


if __name__ == "__main__":
    ProcessEmployee()
