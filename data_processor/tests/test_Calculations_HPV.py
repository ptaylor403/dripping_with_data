from django.test import TestCase
from django.utils import timezone
import datetime as dt
from get_data.models import RawClockData
from data_processor.functions.hpv_calcuations import iterate_over_employees, calc_hpv
from data_processor.functions.man_hours_calculations import get_employees


class HPVCalculations(TestCase):
    @timezone.override("US/Eastern")
    def setUp(self):
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
            HM_LBRACCT_FULL_NAM='017.10000.00.80.07/1/-/017.P000080/-/-/-',
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
            HM_LBRACCT_FULL_NAM='017.30000.00.80.07/1/-/017.P000080/-/-/-',
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
            HM_LBRACCT_FULL_NAM='017.30000.00.80.07/1/-/017.P000080/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=timezone.make_aware(dt.datetime(2016, 6, 3, 6, 39)),
            end_rsn_txt='&break',
            PNCHEVNT_OUT=timezone.make_aware(dt.datetime(2016, 6, 3, 8, 30)),
        )

        RawClockData.objects.create(
            PRSN_NBR_TXT='010',
            full_nam='Janet',
            HM_LBRACCT_FULL_NAM='017.30000.00.80.07/1/-/017.P000080/-/-/-',
            start_rsn_txt='&newShift',
            PNCHEVNT_IN=timezone.make_aware(dt.datetime(2016, 6, 3, 9, 30)),
            end_rsn_txt='&missedOut',
            PNCHEVNT_OUT=None,
        )

    @timezone.override("US/Eastern")
    def test_iterate_over_employees(self):
        test_dept_dict = {
            'CIW': {
                'mh': 0,
                'ne': 0,
                'hpv': 0,
            },
            'FCB': {
                'mh': 0,
                'ne': 0,
                'hpv': 0,
            },
            'PNT': {
                'mh': 0,
                'ne': 0,
                'hpv': 0,
            },
            'PLANT': {
                'mh': 0,
                'ne': 0,
                'hpv': 0,
            },
            'claims_for_range': 10
        }

        expected_dict = {
            'PLANT': {
                'ne': 7,
                'hpv': 2.095,
                'mh': 20.950000000000003
            },
            'FCB': {
                'ne': 2,
                'hpv': 0.8,
                'mh': 8.0
            },
            'PNT': {
                'ne': 4,
                'hpv': 0.8949999999999999,
                'mh': 8.95
            },
            'CIW': {
                'ne': 1,
                'hpv': 0.4,
                'mh': 4.0
            },
            'claims_for_range': 10
        }

        start = timezone.make_aware(dt.datetime(2016, 6, 3, 6, 30))
        stop = timezone.make_aware(dt.datetime(2016, 6, 3, 10, 30))
        employees = get_employees(start, stop)
        result_dict = iterate_over_employees(test_dept_dict, employees, start, stop)
        print(result_dict)
        for key in result_dict:
            if key != 'claims_for_range':
                self.assertEqual(
                    result_dict[key]['hpv'],
                    expected_dict[key]['hpv']
                )
                self.assertEqual(
                    result_dict[key]['ne'],
                    expected_dict[key]['ne']
                )
                self.assertEqual(
                    result_dict[key]['mh'],
                    expected_dict[key]['mh']
                )

    def test_calc_hpv(self):
        claims = 5
        test_dept_dict = {
            'mh': 30,
            'ne': 10,
            'hpv': 0,
        }

        plant_dict = {
            'ne': 10,
            'hpv': 0,
            'mh': 20,
        }

        dept_result, plant_result = calc_hpv(claims, test_dept_dict, plant_dict)
        self.assertEqual(dept_result['hpv'], 6)
        self.assertEqual(plant_result['hpv'], 4)

