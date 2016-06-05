from django.test import TestCase
from .models import Attendance
from datetime import datetime


class AttendanceTestCase(TestCase):
    def setUp(self):
        #first shift clocked out
        Attendance.objects.create(employee_number=00001, department='CIW', clock_in_time=datetime(2016, 6, 1, 6, 30), clock_out_time=datetime(2016, 6, 1, 2, 30), shift='first')
        #first shift not clocked out
        Attendance.objects.create(employee_number=00002, department='CIW', clock_in_time=datetime(2016, 6, 1, 6, 30), clock_out_time=None, shift='first')
        #second shift clocked out
        Attendance.objects.create(employee_number=00003, department='CIW', clock_in_time=datetime(2016, 6, 1, 2, 30), clock_out_time=datetime(2016, 6, 1, 11, 0), shift='first')
        #second shift not clocked out
        Attendance.objects.create(employee_number=00004, department='CIW', clock_in_time=datetime(2016, 6, 1, 6, 30), clock_out_time=None, shift='first')
