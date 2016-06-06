from django.test import TestCase
from .models import Attendance
import datetime as dt


class AttendanceTestCase(TestCase):

    def setUp(self):
        #first shift clocked out
        Attendance.objects.create(employee_number=00001,
                                  department='CIW',
                                  clock_in_time=datetime(2016, 6, 1, 6, 30),
                                  clock_out_time=datetime(2016, 6, 1, 2, 30),
                                  shift='first')

        #first shift not clocked out
        Attendance.objects.create(employee_number=00002,
                                  department='FCH',
                                  clock_in_time=datetime(2016, 6, 1, 6, 30),
                                  clock_out_time=None,
                                  shift='first')

        #second shift clocked out
        Attendance.objects.create(employee_number=00003,
                                  department='FCB',
                                  clock_in_time=datetime(2016, 6, 1, 14, 30),
                                  clock_out_time=datetime(2016, 6, 1, 11, 0),
                                  shift='second')

        #second shift not clocked out
        Attendance.objects.create(employee_number=00004,
                                  department='PNT',
                                  clock_in_time=datetime(2016, 6, 1, 14, 30),
                                  clock_out_time=None,
                                  shift='second')

    def test_get_manhours_during_first_shift_plus_1_hour(self):
        start = dt.datetime(2016, 6, 1, 6, 30)
        stop = dt.datetime(2016, 6, 1, 15, 30)
        expected_manhours = 19

        manhours = Attendance.get_manhours_during(start, stop)
        self.assertEqual(manhours, expected_manhours)
