from django.test import TestCase
from .models import RawClockData
import datetime as dt


class ManHoursTestCase(TestCase):

    def setUp(self):

        # clocked in before start, didn't clock out
        RawClockData.objects.create(
            PRSN_NBR_TXT='001',
            full_nam='Cameron',
            HM_LBRACCT_FULL_NAM='017.80000.00.80.07/1/-/017.P000080/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=dt.datetime(2016, 6, 3, 5, 35),
            end_rsn_txt='&missedOut',
            PNCHEVNT_OUT=dt.datetime(2016, 6, 3, 2, 31),
        )

        # clocked in after start, clocked out
        RawClockData.objects.create(
            PRSN_NBR_TXT='002',
            full_nam='Nic',
            HM_LBRACCT_FULL_NAM='017.20000.00.80.07/1/-/017.P000080/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=dt.datetime(2016, 6, 3, 6, 35),
            end_rsn_txt='&missedOut',
            PNCHEVNT_OUT=dt.datetime(2016, 6, 3, 2, 31),
        )

        # clocked out from previous shift but with today's clockin time
        RawClockData.objects.create(
            PRSN_NBR_TXT='003',
            full_nam='Trisha',
            HM_LBRACCT_FULL_NAM='017.80000.00.80.07/1/-/017.P000080/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=dt.datetime(2016, 6, 3, 5, 25),
            end_rsn_txt='&missedOut',
            PNCHEVNT_OUT=dt.datetime(2016, 6, 2, 2, 59),
        )

        # clocked out early from current shift
        RawClockData.objects.create(
            PRSN_NBR_TXT='004',
            full_nam='Stacey',
            HM_LBRACCT_FULL_NAM='017.20000.00.80.07/1/-/017.P000080/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=dt.datetime(2016, 6, 3, 6, 25),
            end_rsn_txt='&missedOut',
            PNCHEVNT_OUT=dt.datetime(2016, 6, 3, 10, 31)
        )

        # clocked in right at start time
        RawClockData.objects.create(
            PRSN_NBR_TXT='005',
            full_nam='Stacey',
            HM_LBRACCT_FULL_NAM='017.20000.00.80.07/1/-/017.P000080/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=dt.datetime(2016, 6, 3, 6, 30),
            end_rsn_txt='&missedOut',
            PNCHEVNT_OUT=dt.datetime(2016, 6, 3, 2, 30)
        )

        # clocked in before start, didn't clock out
        RawClockData.objects.create(
            PRSN_NBR_TXT='006',
            full_nam='Alex',
            HM_LBRACCT_FULL_NAM='017.80000.00.80.07/1/-/017.P000080/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=dt.datetime(2016, 6, 3, 6, 19),
            end_rsn_txt='&missedOut',
            PNCHEVNT_OUT=None
        )


    def test_get_currently_clocked_in_before_start(self):
        """Test for employees who clocked in before start is accurate"""
        start = dt.datetime(2016, 6, 3, 6, 30)
        expected_employees = ['001', '004', '006']

        # Should return 2 employees clocked in before start time
        employees = RawClockData.get_clocked_in_before_start(start).order_by('pk')
        self.assertEqual(employees.count(), 3)

        # Testing for accuracy of filter
        for employee, expected_employee_num in zip(employees, expected_employees):
            self.assertEqual(employee.PRSN_NBR_TXT, expected_employee_num)

    def test_get_clocked_in_after_start(self):
        """Test for employees who clock in after start is accurate"""
        start = dt.datetime(2016, 6, 3, 6, 30)
        expected_employees = ['002', '005']

        # Should return 2 employees clocked in after start time
        employees = RawClockData.get_clocked_in_after_start(start).order_by('pk')
        self.assertEqual(employees.count(), 2)

        for employee, expected_employee_num in zip(employees, expected_employees):
            self.assertEqual(employee.PRSN_NBR_TXT, expected_employee_num)

    def test_get_clocked_out_after_start(self):
        """Test for employees who clocked out after start is accurate"""
        start = dt.datetime(2016, 6, 3, 6, 30)
        expected_employees = ['002', '005']

        # Should return 2 employees clocked in after start time
        employees = RawClockData.get_clocked_in_after_start(start).order_by('pk')
        self.assertEqual(employees.count(), 2)

        for employee, expected_employee_num in zip(employees, expected_employees):
            self.assertEqual(employee.PRSN_NBR_TXT, expected_employee_num)

    def test_get_clocked_out_during_time_period(self):
        start = dt.datetime(2016, 6, 3, 6, 30)
        stop =  dt.datetime(2016, 6, 3, 2, 30)
        expected_employees = ['006']

        # Employees who clocked out after start
        employees = RawClockData.get_clocked_in_after_start(start).order_by('pk')
        for employee in employees:
            print("CLOCKED OUT AFTER START EMP #", employee.PRSN_NBR_TXT)


        # Filtering that list to capture those who didn't clock out after stop
        filtered_employees = RawClockData.get_clocked_out_during_time_period(stop, employees)
        for filtered_employee in filtered_employees:
            print("FILTERED EMP #", filtered_employee.PRSN_NBR_TXT)
