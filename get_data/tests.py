from django.test import TestCase
from .models import RawClockData, RawDirectRunData, RawCrysData, RawPlantActivity
import datetime
# Create your tests here.
class RawClockDataTestCase(TestCase):
    def setUp(self):
        RawClockData.objects.create(
            PRSN_NBR_TXT=12345,
            full_nam='John Doe',
            HM_LBRACCT_FULL_NAM='017.10000',
            start_rsn_txt=row['start_rsn_txt'],
            PNCHEVNT_IN=process_date(row['PNCHEVNT_DTM_IN']),
            end_rsn_txt=row['end_rsn_txt'],
            PNCHEVNT_OUT=process_date(row['PNCHEVNT_DTM_OUT']),
        )
