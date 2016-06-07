from django.test import TestCase
from .models import RawClockData, RawPlantActivity
import datetime as dt
import pytz


class ManHoursTestCase(TestCase):
    def setUp(self):
        #################################################
        # Previous Day Clock In/Out
        #################################################
        RawClockData.objects.create(
            PRSN_NBR_TXT='001',
            full_nam='Cameron',
            HM_LBRACCT_FULL_NAM='017.30000.00.51.05/1/-/017.P000051/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=dt.datetime(2016, 6, 2, 5, 35, tzinfo=pytz.utc),
            end_rsn_txt='&out',
            PNCHEVNT_OUT=dt.datetime(2016, 6, 2, 14, 32, tzinfo=pytz.utc)
        )

        RawClockData.objects.create(
            PRSN_NBR_TXT='002',
            full_nam='Nic',
            HM_LBRACCT_FULL_NAM='017.20000.00.80.07/1/-/017.P000080/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=dt.datetime(2016, 6, 2, 22, 29, tzinfo=pytz.utc),
            end_rsn_txt='&out',
            PNCHEVNT_OUT=dt.datetime(2016, 6, 3, 6, 32, tzinfo=pytz.utc)
        )
        #################################################
        # Previous Day Forgot Clock Out
        #################################################
        RawClockData.objects.create(
            PRSN_NBR_TXT='001',
            full_nam='Cameron',
            HM_LBRACCT_FULL_NAM='017.30000.00.51.05/1/-/017.P000051/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=dt.datetime(2016, 6, 2, 5, 35, tzinfo=pytz.utc),
            end_rsn_txt='&missedOut',
            PNCHEVNT_OUT=None
        )
        #################################################
        # Current Day Clock In
        #################################################
        RawClockData.objects.create(
            PRSN_NBR_TXT='001',
            full_nam='Cameron',
            HM_LBRACCT_FULL_NAM='017.30000.00.51.05/1/-/017.P000051/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=dt.datetime(2016, 6, 3, 5, 35, tzinfo=pytz.utc),
            end_rsn_txt='&missedOut',
            PNCHEVNT_OUT=None
        )

        RawClockData.objects.create(
            PRSN_NBR_TXT='003',
            full_nam='Trisha',
            HM_LBRACCT_FULL_NAM='017.60000.00.84.43/2/-/017.P000085/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=dt.datetime(2016, 6, 3, 5, 25, tzinfo=pytz.utc),
            end_rsn_txt='&missedOut',
            PNCHEVNT_OUT=None
        )

        RawClockData.objects.create(
            PRSN_NBR_TXT='006',
            full_nam='Alex',
            HM_LBRACCT_FULL_NAM='017.80000.00.80.07/1/-/017.P000080/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=dt.datetime(2016, 6, 3, 6, 19, tzinfo=pytz.utc),
            end_rsn_txt='&missedOut',
            PNCHEVNT_OUT=None
        )

        RawClockData.objects.create(
            PRSN_NBR_TXT='004',
            full_nam='Stacey',
            HM_LBRACCT_FULL_NAM='017.20000.00.80.07/1/-/017.P000080/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=dt.datetime(2016, 6, 3, 6, 25, tzinfo=pytz.utc),
            end_rsn_txt='missedOut',
            PNCHEVNT_OUT=None,
        )

        #################################################
        # Employees late
        #################################################
        RawClockData.objects.create(
            PRSN_NBR_TXT='005',
            full_nam='Stacey',
            HM_LBRACCT_FULL_NAM='017.20000.00.80.07/1/-/017.P000080/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=dt.datetime(2016, 6, 3, 6, 30, tzinfo=pytz.utc),
            end_rsn_txt='&missedOut',
            PNCHEVNT_OUT=None
        )

        RawClockData.objects.create(
            PRSN_NBR_TXT='002',
            full_nam='Nic',
            HM_LBRACCT_FULL_NAM='017.80000.00.80.07/1/-/017.P000080/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=dt.datetime(2016, 6, 3, 6, 35, tzinfo=pytz.utc),
            end_rsn_txt='&missedOut',
            PNCHEVNT_OUT=None,
        )

        #################################################
        # Clocked Out Early
        #################################################
        RawClockData.objects.create(
            PRSN_NBR_TXT='004',
            full_nam='Stacey',
            HM_LBRACCT_FULL_NAM='017.20000.00.80.07/1/-/017.P000080/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=dt.datetime(2016, 6, 3, 6, 25, tzinfo=pytz.utc),
            end_rsn_txt='&out',
            PNCHEVNT_OUT=dt.datetime(2016, 6, 3, 10, 31, tzinfo=pytz.utc)
        )

        RawClockData.objects.create(
            PRSN_NBR_TXT='002',
            full_nam='Nic',
            HM_LBRACCT_FULL_NAM='017.20000.00.80.07/1/-/017.P000080/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=dt.datetime(2016, 6, 3, 6, 35, tzinfo=pytz.utc),
            end_rsn_txt='&out',
            PNCHEVNT_OUT=dt.datetime(2016, 6, 3, 8, 30, tzinfo=pytz.utc),
        )

        #################################################
        # Employee came back
        #################################################
        RawClockData.objects.create(
            PRSN_NBR_TXT='004',
            full_nam='Stacey',
            HM_LBRACCT_FULL_NAM='017.20000.00.80.07/1/-/017.P000080/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=dt.datetime(2016, 6, 3, 12, 30, tzinfo=pytz.utc),
            end_rsn_txt='&missedOut',
            PNCHEVNT_OUT=None
        )

        #################################################
        # Clock out early
        #################################################
        RawClockData.objects.create(
            PRSN_NBR_TXT='001',
            full_nam='Cameron',
            HM_LBRACCT_FULL_NAM='017.30000.00.51.05/1/-/017.P000051/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=dt.datetime(2016, 6, 3, 5, 35, tzinfo=pytz.utc),
            end_rsn_txt='&out',
            PNCHEVNT_OUT=dt.datetime(2016, 6, 3, 14, 29, tzinfo=pytz.utc),
        )

        #################################################
        # Clock out regular
        #################################################

        RawClockData.objects.create(
            PRSN_NBR_TXT='006',
            full_nam='Alex',
            HM_LBRACCT_FULL_NAM='017.80000.00.80.07/1/-/017.P000080/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=dt.datetime(2016, 6, 3, 6, 19, tzinfo=pytz.utc),
            end_rsn_txt='&out',
            PNCHEVNT_OUT=dt.datetime(2016, 6, 3, 14, 30, tzinfo=pytz.utc),
        )

        RawClockData.objects.create(
            PRSN_NBR_TXT='005',
            full_nam='Stacey',
            HM_LBRACCT_FULL_NAM='017.20000.00.80.07/1/-/017.P000080/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=dt.datetime(2016, 6, 3, 6, 30, tzinfo=pytz.utc),
            end_rsn_txt='&out',
            PNCHEVNT_OUT=dt.datetime(2016, 6, 3, 14, 30, tzinfo=pytz.utc)
        )

        RawClockData.objects.create(
            PRSN_NBR_TXT='004',
            full_nam='Stacey',
            HM_LBRACCT_FULL_NAM='017.20000.00.80.07/1/-/017.P000080/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=dt.datetime(2016, 6, 3, 12, 30, tzinfo=pytz.utc),
            end_rsn_txt='&out',
            PNCHEVNT_OUT=dt.datetime(2016, 6, 3, 14, 30, tzinfo=pytz.utc)
        )

        RawClockData.objects.create(
            PRSN_NBR_TXT='003',
            full_nam='Trisha',
            HM_LBRACCT_FULL_NAM='017.60000.00.84.43/2/-/017.P000085/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=dt.datetime(2016, 6, 3, 5, 25, tzinfo=pytz.utc),
            end_rsn_txt='&out',
            PNCHEVNT_OUT=dt.datetime(2016, 6, 3, 14, 30, tzinfo=pytz.utc)
        )

        #################################################
        # Tests
        #################################################

    def test_get_currently_clocked_in(self):
        """Test for employees who clocked in before start is accurate"""
        start = dt.datetime(2016, 6, 3, 6, 30, tzinfo=pytz.utc)
        expected_employees = ['001', '003', '004', '006', '005', '002']
        func_name = 'test_get_currently_clocked_in_before_start'

        employees = RawClockData.get_clocked_in(start)

        # for employee in employees:
        #     ManHoursTestCase.print_employee_results(func_name, employee)

        self.assertEqual(employees.count(), 7)

        # Testing for accuracy of filter
        for employee, expected_employee_num in zip(employees, expected_employees):
            self.assertIn(employee.PRSN_NBR_TXT, expected_employees)

    def test_man_hours(self):
        """Test for employees who clocked in before start is accurate"""
        start = dt.datetime(2016, 6, 3, 6, 30, tzinfo=pytz.utc)
        stop = dt.datetime(2016, 6, 3, 10, 30, tzinfo=pytz.utc)
        expected_employees = ['001', '003', '004', '006', '005', '002']
        func_name = 'test_man_hours'

        hours, num_employees = RawClockData.get_plant_man_hours_atm(start, stop)

        self.assertEqual(hours, 28)
        self.assertEqual(num_employees, 7)

    def test_process_deparment(self):
        """Testing base functionality of process department to make sure that we are ripping the correct data out"""
        employee_dept_test_list = [
            '017.30000.00.51.05/1/-/017.P000051/-/-/-',
            '017.90000.00.00.21/2/-/017.I996063/-/-/-',
            '017.60000.00.84.43/2/-/017.P000085/-/-/-',
            '017.20000.00.84.01/1/-/017.P000084/-/-/-',
            '017.80000.00.80.09/3/-/017.P000080/-/-/-',
            '017.10000.00.00.12/1/-/017.I996063/-/-/-'
        ]

        expected_dept_test_list = ['PNT', 'MAT', 'DAC', 'FCB', 'QA', 'CIW']
        expected_shift_test_list = ['1', '2', '2', '1', '3', '1']

        PLANT_CODE = '017'

        for index, item in enumerate(employee_dept_test_list):
            # print("/"*50)
            # print('index = ', index)
            # print('item = ', item)
            emp_plant, emp_dept, emp_shift= RawClockData.process_department(item)
            self.assertEqual(PLANT_CODE, emp_plant)
            self.assertEqual(expected_dept_test_list[index], emp_dept)
            self.assertEqual(expected_shift_test_list[index], emp_shift)


    @staticmethod
    def print_employee_results(fun_name, objects):
        print(
            fun_name,
            '---',
            objects.PRSN_NBR_TXT,
            ' ', objects.PNCHEVNT_IN,
            ' ', objects.PNCHEVNT_OUT,
            ' ', objects.end_rsn_txt
        )



class ClaimData(TestCase):
    def setUp(self):
        #################################################
        # claim trucks previous day as test manhours
        #################################################
        RawPlantActivity.objects.create(
            VEH_SER_NO='HZ3849',
            POOL_TRIG_TYPE='VEH DLVRY',
            TS_LOAD=dt.datetime(2016, 6, 2, 12, 25, tzinfo=pytz.utc),
            DATE_WORK=dt.datetime(2016, 6, 1, 5, 25, tzinfo=pytz.utc),
        )

        RawPlantActivity.objects.create(
            VEH_SER_NO='HZ3850',
            POOL_TRIG_TYPE='VEH DLVRY',
            TS_LOAD=dt.datetime(2016, 6, 2, 14, 25, tzinfo=pytz.utc),
            DATE_WORK=dt.datetime(2016, 6, 1, 5, 25, tzinfo=pytz.utc),
        )

        #################################################
        # claim trucks same day as test manhours
        #################################################
        RawPlantActivity.objects.create(
            VEH_SER_NO='HZ3851',
            POOL_TRIG_TYPE='VEH DLVRY',
            TS_LOAD=dt.datetime(2016, 6, 3, 6, 45, tzinfo=pytz.utc),
            DATE_WORK=dt.datetime(2016, 6, 1, 5, 25, tzinfo=pytz.utc),
        )

        RawPlantActivity.objects.create(
            VEH_SER_NO='HZ3852',
            POOL_TRIG_TYPE='VEH DLVRY',
            TS_LOAD=dt.datetime(2016, 6, 3, 6, 55, tzinfo=pytz.utc),
            DATE_WORK=dt.datetime(2016, 6, 1, 5, 25, tzinfo=pytz.utc),
        )

        RawPlantActivity.objects.create(
            VEH_SER_NO='HZ3853',
            POOL_TRIG_TYPE='VEH DLVRY',
            TS_LOAD=dt.datetime(2016, 6, 3, 7, 15, tzinfo=pytz.utc),
            DATE_WORK=dt.datetime(2016, 6, 1, 5, 25, tzinfo=pytz.utc),
        )

        RawPlantActivity.objects.create(
            VEH_SER_NO='HZ3854',
            POOL_TRIG_TYPE='VEH DLVRY',
            TS_LOAD=dt.datetime(2016, 6, 3, 8, 15, tzinfo=pytz.utc),
            DATE_WORK=dt.datetime(2016, 6, 1, 5, 25, tzinfo=pytz.utc),
        )

    def test_get_claim_data(self):
        #regular test case of start to end time
        start = dt.datetime(2016, 6, 3, 6, 30, tzinfo=pytz.utc)
        num_trucks = RawPlantActivity.get_claims_date_range(start)
        self.assertEqual(num_trucks, 4)

        #testing range
        start = dt.datetime(2016, 6, 2, 6, 30, tzinfo=pytz.utc)
        stop = dt.datetime(2016, 6, 3, 7, 30, tzinfo=pytz.utc)
        num_trucks = RawPlantActivity.get_claims_date_range(start, stop)

        print("*"*50)
        print(num_trucks)

        self.assertEqual(num_trucks, 5)

        claimed_objects = RawPlantActivity.get_claimed_objects_in_range(start,stop)
        expected_claims = ['HZ3849', 'HZ3850', 'HZ3851', 'HZ3852', 'HZ3853']
        not_expected_claims = ['HZ3854']

        for claim in claimed_objects:
            self.assertIn(claim.VEH_SER_NO, expected_claims)
            self.assertNotIn(claim.VEH_SER_NO, not_expected_claims)



