from django.test import TestCase
from .models import Attendance, Complete
import datetime
# Create your tests here.
class AttendanceTestCase(TestCase):
    def setUP(self):
        employee1 = Attendance.objects.create(employee_number=1,
                                  department='FCB',
                                  clock_in_time=datetime.datetime.now(),
                                  clock_out_time=Null,
                                  shift='shift')
        employee2 = Attendance.objects.create(employee_number=2,
                                  department='CIW',
                                  clock_in_time=datetime.datetime.now(),
                                  clock_out_time=Null,
                                  shift='shift')


    def test_clocked_in(self):
        pass
