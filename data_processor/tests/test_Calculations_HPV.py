from django.test import TestCase

from data_processor.functions.process_data_main import get_hpv


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