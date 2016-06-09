from django.test import TestCase
import datetime as dt
from django.utils import timezone
from get_data.models import RawClockData, RawPlantActivity
import random

from .functions.man_hours_calculations import get_clocked_in, get_emp_man_hours, get_emp_dept
from .functions.claims_calculations import get_claimed_objects_in_range, get_range_of_claims
from .functions.process_data_main import get_hpv


# Create your tests here.
class ManHoursTestCase(TestCase):
    
    @timezone.override("US/Eastern")
    def setUp(self):
        #################################################
        # Previous Day Clock In/Out
        #################################################
        RawClockData.objects.create(
            PRSN_NBR_TXT='001',
            full_nam='Cameron',
            HM_LBRACCT_FULL_NAM='017.30000.00.51.05/1/-/017.P000051/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=timezone.make_aware(dt.datetime(2016, 6, 2, 5, 35)),
            end_rsn_txt='&out',
            PNCHEVNT_OUT=timezone.make_aware(dt.datetime(2016, 6, 2, 14, 32)),
        )

        RawClockData.objects.create(
            PRSN_NBR_TXT='002',
            full_nam='Nic',
            HM_LBRACCT_FULL_NAM='017.20000.00.80.07/1/-/017.P000080/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=timezone.make_aware(dt.datetime(2016, 6, 2, 22, 29)),
            end_rsn_txt='&out',
            PNCHEVNT_OUT=timezone.make_aware(dt.datetime(2016, 6, 3, 6, 32)),
        )
        #################################################
        # Previous Day Forgot Clock Out
        #################################################
        RawClockData.objects.create(
            PRSN_NBR_TXT='001',
            full_nam='Cameron',
            HM_LBRACCT_FULL_NAM='017.30000.00.51.05/1/-/017.P000051/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=timezone.make_aware(dt.datetime(2016, 6, 2, 5, 35)),
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
            PNCHEVNT_IN=timezone.make_aware(dt.datetime(2016, 6, 3, 5, 35)),
            end_rsn_txt='&missedOut',
            PNCHEVNT_OUT=None
        )

        RawClockData.objects.create(
            PRSN_NBR_TXT='003',
            full_nam='Trisha',
            HM_LBRACCT_FULL_NAM='017.60000.00.84.43/2/-/017.P000085/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=timezone.make_aware(dt.datetime(2016, 6, 3, 5, 25)),
            end_rsn_txt='&missedOut',
            PNCHEVNT_OUT=None
        )

        RawClockData.objects.create(
            PRSN_NBR_TXT='006',
            full_nam='Alex',
            HM_LBRACCT_FULL_NAM='017.80000.00.80.07/1/-/017.P000080/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=timezone.make_aware(dt.datetime(2016, 6, 3, 6, 19)),
            end_rsn_txt='&missedOut',
            PNCHEVNT_OUT=None
        )

        RawClockData.objects.create(
            PRSN_NBR_TXT='004',
            full_nam='Stacey',
            HM_LBRACCT_FULL_NAM='017.20000.00.80.07/1/-/017.P000080/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=timezone.make_aware(dt.datetime(2016, 6, 3, 6, 25)),
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
            PNCHEVNT_IN=timezone.make_aware(dt.datetime(2016, 6, 3, 6, 30)),
            end_rsn_txt='&missedOut',
            PNCHEVNT_OUT=None
        )

        RawClockData.objects.create(
            PRSN_NBR_TXT='002',
            full_nam='Nic',
            HM_LBRACCT_FULL_NAM='017.80000.00.80.07/1/-/017.P000080/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=timezone.make_aware(dt.datetime(2016, 6, 3, 6, 35)),
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
            PNCHEVNT_IN=timezone.make_aware(dt.datetime(2016, 6, 3, 6, 25)),
            end_rsn_txt='&out',
            PNCHEVNT_OUT=timezone.make_aware(dt.datetime(2016, 6, 3, 10, 31))
        )

        RawClockData.objects.create(
            PRSN_NBR_TXT='002',
            full_nam='Nic',
            HM_LBRACCT_FULL_NAM='017.20000.00.80.07/1/-/017.P000080/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=timezone.make_aware(dt.datetime(2016, 6, 3, 6, 35)),
            end_rsn_txt='&out',
            PNCHEVNT_OUT=timezone.make_aware(dt.datetime(2016, 6, 3, 8, 30)),
        )

        #################################################
        # Employee came back
        #################################################
        RawClockData.objects.create(
            PRSN_NBR_TXT='004',
            full_nam='Stacey',
            HM_LBRACCT_FULL_NAM='017.20000.00.80.07/1/-/017.P000080/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=timezone.make_aware(dt.datetime(2016, 6, 3, 12, 30)),
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
            PNCHEVNT_IN=timezone.make_aware(dt.datetime(2016, 6, 3, 5, 35)),
            end_rsn_txt='&out',
            PNCHEVNT_OUT=timezone.make_aware(dt.datetime(2016, 6, 3, 14, 29)),
        )

        #################################################
        # Clock out regular
        #################################################

        RawClockData.objects.create(
            PRSN_NBR_TXT='006',
            full_nam='Alex',
            HM_LBRACCT_FULL_NAM='017.80000.00.80.07/1/-/017.P000080/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=timezone.make_aware(dt.datetime(2016, 6, 3, 6, 19)),
            end_rsn_txt='&out',
            PNCHEVNT_OUT=timezone.make_aware(dt.datetime(2016, 6, 3, 14, 30)),
        )

        RawClockData.objects.create(
            PRSN_NBR_TXT='005',
            full_nam='Stacey',
            HM_LBRACCT_FULL_NAM='017.20000.00.80.07/1/-/017.P000080/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=timezone.make_aware(dt.datetime(2016, 6, 3, 6, 30)),
            end_rsn_txt='&out',
            PNCHEVNT_OUT=timezone.make_aware(dt.datetime(2016, 6, 3, 14, 30))
        )

        RawClockData.objects.create(
            PRSN_NBR_TXT='004',
            full_nam='Stacey',
            HM_LBRACCT_FULL_NAM='017.20000.00.80.07/1/-/017.P000080/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=timezone.make_aware(dt.datetime(2016, 6, 3, 12, 30)),
            end_rsn_txt='&out',
            PNCHEVNT_OUT=timezone.make_aware(dt.datetime(2016, 6, 3, 14, 30))
        )

        RawClockData.objects.create(
            PRSN_NBR_TXT='003',
            full_nam='Trisha',
            HM_LBRACCT_FULL_NAM='017.60000.00.84.43/2/-/017.P000085/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=timezone.make_aware(dt.datetime(2016, 6, 3, 5, 25)),
            end_rsn_txt='&out',
            PNCHEVNT_OUT=timezone.make_aware(dt.datetime(2016, 6, 3, 14, 30))
        )

        #################################################
        # Tests
        #################################################

    @timezone.override("US/Eastern")
    def test_get_currently_clocked_in(self):
        """Test for employees who clocked in before start is accurate"""
        start = timezone.make_aware(dt.datetime(2016, 6, 3, 6, 30))
        expected_employees = ['001', '003', '004', '006', '005', '002']
        employees = get_clocked_in(start)

        for employee in employees:
            print(employee.PRSN_NBR_TXT)
        self.assertEqual(employees.count(), 7)

        # Testing for accuracy of filter
        for employee, expected_employee_num in zip(employees, expected_employees):
            self.assertIn(employee.PRSN_NBR_TXT, expected_employees)


    @timezone.override("US/Eastern")
    def test_emp_man_hours(self):
        """Test for employees who clocked in before start is accurate"""
        start = timezone.make_aware(dt.datetime(2016, 6, 3, 6, 30))
        stop = timezone.make_aware(dt.datetime(2016, 6, 3, 10, 30))

        func_name = 'test_man_hours'

        employees = get_clocked_in(start)

        for employee in employees:
            emp_hours = get_emp_man_hours(employee, start, stop)
            self.assertEqual(emp_hours, 4)
            break

    def test_process_department(self):
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

        for index, item in enumerate(employee_dept_test_list):
            # print("/"*50)
            # print('index = ', index)
            # print('item = ', item)
            emp_dept = get_emp_dept(item)
            self.assertEqual(expected_dept_test_list[index], emp_dept)


class ClaimData(TestCase):
    def setUp(self):
        #################################################
        # claim trucks previous day as test manhours
        #################################################
        RawPlantActivity.objects.create(
            VEH_SER_NO='HZ3849',
            POOL_CD='03',
            TS_LOAD=timezone.make_aware(dt.datetime(2016, 6, 2, 12, 25)),
        )

        RawPlantActivity.objects.create(
            VEH_SER_NO='HZ3850',
            POOL_CD='03',
            TS_LOAD=timezone.make_aware(dt.datetime(2016, 6, 2, 14, 25)),
        )

        #################################################
        # claim trucks same day as test manhours
        #################################################
        RawPlantActivity.objects.create(
            VEH_SER_NO='HZ3851',
            POOL_CD='DL',
            TS_LOAD=timezone.make_aware(dt.datetime(2016, 6, 3, 6, 45)),
        )

        RawPlantActivity.objects.create(
            VEH_SER_NO='HZ3852',
            POOL_CD='03',
            TS_LOAD=timezone.make_aware(dt.datetime(2016, 6, 3, 6, 55)),
        )

        RawPlantActivity.objects.create(
            VEH_SER_NO='HZ3853',
            POOL_CD='01',
            TS_LOAD=timezone.make_aware(dt.datetime(2016, 6, 3, 7, 15)),
        )

        RawPlantActivity.objects.create(
            VEH_SER_NO='HZ3854',
            POOL_CD='03',
            TS_LOAD=timezone.make_aware(dt.datetime(2016, 6, 3, 8, 15)),
        )

    def test_get_claim_data(self):
        #regular test case of start to end time
        start = timezone.make_aware(dt.datetime(2016, 6, 3, 6, 30))
        stop = timezone.make_aware(dt.datetime(2016, 6, 3, 10, 30))
        num_trucks = get_range_of_claims(start, stop)
        self.assertEqual(num_trucks, 2)

        #testing range
        start = timezone.make_aware(dt.datetime(2016, 6, 2, 6, 30))
        stop = timezone.make_aware(dt.datetime(2016, 6, 3, 7, 30))
        num_trucks = get_range_of_claims(start, stop)
        # print("*"*50)
        # print(num_trucks)
        self.assertEqual(num_trucks, 3)

        claimed_objects = get_claimed_objects_in_range(start, stop)
        expected_claims = ['HZ3849', 'HZ3850', 'HZ3852', 'HZ3854']
        not_expected_claims = ['HZ3854', 'HZ3853']

        for claim in claimed_objects:
            print(claim.VEH_SER_NO)
            self.assertIn(claim.VEH_SER_NO, expected_claims)
            self.assertNotIn(claim.VEH_SER_NO, not_expected_claims)

class HPVCalculations(TestCase):
    def setUp(self):
        pass


    def test_get_hpv(self):
        test_dept_dict = {
            'CIW': {
                'mh': 100,
                'ne': 30,
                'hpv': 0,
            },
            'FCB': {
                'mh': 25,
                'ne': 40,
                'hpv': 0,
            },
            'PNT': {
                'mh': 75,
                'ne': 20,
                'hpv': 0,
            },
            'PLANT': {
                'mh': 0,
                'ne': 0,
                'hpv': 0,
            },
            'claims_for_range': 15
        }

        result_dict = get_hpv(test_dept_dict)

        expected_result = test_dept_dict['CIW']['mh']/test_dept_dict['claims_for_range']
        self.assertEqual(expected_result, result_dict['CIW']['hpv'])

        # test divide by zero
        test_dept_dict['claims_for_range'] = 0
        result_dict = get_hpv(test_dept_dict)
        expected_result = 0
        self.assertEqual(expected_result, result_dict['FCB']['hpv'])

        # test plant totals
        test_dept_dict['claims_for_range'] = 25
        result_dict = get_hpv(test_dept_dict)

        # mh total
        expected_result = 200
        self.assertEqual(expected_result, result_dict['PLANT']['mh'])

        # ne total
        expected_result = 90
        self.assertEqual(expected_result, result_dict['PLANT']['ne'])

        # hpv total
        expected_result = 8
        self.assertEqual(expected_result, result_dict['PLANT']['hpv'])
