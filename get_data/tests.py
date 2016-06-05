from django.test import TestCase
from .models import RawClockData
import datetime as dt


class ManHoursTestCase(TestCase):
    def setup(self):
        RawClockData.objects.create(PRSN_NBR_TXT=001, full_nam='Cameron', HM_LBRACCT_FULL_NAM='017.80000.00.80.07/1/-/017.P000080/-/-/-', start_rsn_txt='&newShift', PNCHEVNT_IN=dt.datetime(2016, 6, 1, 5, 35), end_rsn_txt='&missedOut', PNCHEVNT_OUT=None)
