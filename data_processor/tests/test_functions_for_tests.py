from django.test import TestCase
from django.utils import timezone
import datetime as dt
from get_data.models import RawClockData
from .functions.functions_for_tests import find_pop_and_return, compare_expect_against_query
from data_processor.functions.man_hours_calculations import get_clocked_in


class FunctionsForTest(TestCase):
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
        # Clock In
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

        #################################################
        # Employees left early
        #################################################
        RawClockData.objects.create(
            PRSN_NBR_TXT='002',
            full_nam='Nic',
            HM_LBRACCT_FULL_NAM='017.80000.00.80.07/1/-/017.P000080/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=timezone.make_aware(dt.datetime(2016, 6, 3, 6, 45)),
            end_rsn_txt='&out',
            PNCHEVNT_OUT=timezone.make_aware(dt.datetime(2016, 6, 3, 8, 51)),
        )

        ################################################
        # Employees left early and then came back
        ################################################
        RawClockData.objects.create(
            PRSN_NBR_TXT='010',
            full_nam='Janet',
            HM_LBRACCT_FULL_NAM='017.80000.00.80.07/1/-/017.P000080/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=timezone.make_aware(dt.datetime(2016, 6, 3, 6, 39)),
            end_rsn_txt='&break',
            PNCHEVNT_OUT=timezone.make_aware(dt.datetime(2016, 6, 3, 8, 30)),
        )

        RawClockData.objects.create(
            PRSN_NBR_TXT='010',
            full_nam='Janet',
            HM_LBRACCT_FULL_NAM='017.80000.00.80.07/1/-/017.P000080/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=timezone.make_aware(dt.datetime(2016, 6, 3, 9, 30)),
            end_rsn_txt='&missedOut',
            PNCHEVNT_OUT=None,
        )

    def test_find_pop_and_return_expected(self):
        expected_employees = ['001', '004', '006']
        looking_for = '004'

        # testing items of the returned list
        found_item, returned_list = find_pop_and_return(
            looking_for=looking_for,
            expected_list=expected_employees,

        )

        # is what is found actually the item we are looking for?
        self.assertEqual(looking_for, found_item)

        # returned list should be 2 long
        self.assertEqual(len(returned_list), 2)

    def test_compare_expect_against_query(self):
        start = timezone.make_aware(dt.datetime(2016, 6, 3, 6, 30))
        expected_employees = ['001', '004', '006', '005', '010']
        employees = get_clocked_in(start)
        print(employees)
        self.assertTrue(compare_expect_against_query(expected_employees, employees))

