from django.test import TestCase
from .functions_for_tests import find_pop_and_return


class FunctionsForTest(TestCase):
    def setUp(self):
        pass

    def test_find_pop_and_return_expected(self):
        expected_employees = ['001', '004', '006']
        looking_for = '004'

        # testing items of the returned list
        found_item, returned_list= find_pop_and_return(
            looking_for=looking_for,
            expected_list=expected_employees,

        )

        # is what is found actually the item we are looking for?
        self.assertEqual(looking_for, found_item)

        # returned list should be 2 long
        self.assertEqual(len(returned_list), 2)

