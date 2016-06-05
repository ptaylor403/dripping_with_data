from django.test import TestCase
from .models import Attendance, Complete
import datetime
# Create your tests here.
class AttendanceTestCase(TestCase):
    def setUp(self):
        Attendance.objects.create(employee_number=1,
                                  department='FCB',
                                  clock_in_time=datetime.datetime.now(),
                                  clock_out_time=None,
                                  shift='shift')
        Attendance.objects.create(employee_number=2,
                                  department='CIW',
                                  clock_in_time=datetime.datetime.now(),
                                  clock_out_time=None,
                                  shift='shift')

    def test_count(self):
        self.assertEqual(Attendance.objects.count(), 2)


    # def test_dept(self):
    #     dept = 'FCB'
    #     employee1 = Attendance.objects.get(department='FCB')
    #     self.assertEqual(employee1.department(), dept)
