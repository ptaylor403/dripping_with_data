from django.test import TestCase
from django.utils import timezone
from get_data.models import RawPlantActivity
from plantsettings.models import PlantSetting
from api.models import HPVATM
import data_processor.tests.test_files.hpv_dict_test_cases as tc
import data_processor.tests.test_files.api_test_cases as api_tc
import data_processor.tests.test_files.plant_settings_test_cases as ps_tc

import datetime as dt

from data_processor.processor_functions.processor_get_new_hpv import get_new_hpv_data

from data_processor.processor_functions.processor_day_hpv import get_day_hpv_dict

from data_processor.processor_functions.processor_delete_old import delete_old_entries

from data_processor.processor_functions.processor_dept_day_stats import get_dept_day_stats

from data_processor.processor_functions.processor_plant_day_stats import get_plant_day_hpv

from data_processor.processor_functions.processor_shift import get_shift_info, get_day_start

from data_processor.processor_functions.processor_write_conditions import need_to_write

class GetHPVData(TestCase):
    def setUp(self):
        RawPlantActivity.objects.create(
            VEH_SER_NO='HZ3852',
            POOL_CD='03',
            TS_LOAD=timezone.make_aware(dt.datetime(2016, 6, 2, 6, 55)),
        )

        # timestamp after last write, but wrong pool number for false-positives
        RawPlantActivity.objects.create(
            VEH_SER_NO='HZ3853',
            POOL_CD='01',
            TS_LOAD=timezone.make_aware(dt.datetime(2016, 6, 2, 19, 55)),
        )

    def test_get_new_hpv_data_no_new_claims_recent_entry(self):
        HPVATM.objects.create(**api_tc.two_shifts_first_shift_api_entry_7_am)
        PlantSetting.objects.create(**ps_tc.default_plant_settings_7_05)

        self.assertEqual(get_new_hpv_data(), None)

    def test_get_new_hpv_data_no_new_claims_15_min_since_write(self):
        # API 6/2 @ 7:00
        HPVATM.objects.create(**api_tc.two_shifts_first_shift_api_entry_7_am)
        # Now/Plant 6/2 @ 8:00
        PlantSetting.objects.create(**ps_tc.three_shift_8_am_plant_settings)

        self.assertEqual(get_new_hpv_data(), True)

    def test_get_new_hpv_data_no_new_claims_end_shift_recent_entry(self):
        # API 6/2 @ 14:25
        HPVATM.objects.create(**api_tc.two_shifts_first_shift_api_entry)
        # Now/Plant 6/2 @ 14:27
        PlantSetting.objects.create(**ps_tc.default_plant_settings_14_27)

        self.assertEqual(get_new_hpv_data(), True)

    def test_get_new_hpv_data_no_api_entries(self):
        PlantSetting.objects.create(**ps_tc.three_shift_8_am_plant_settings)

        self.assertEqual(get_new_hpv_data(), True)

    def test_get_new_hpv_data_no_claims(self):
        RawPlantActivity.objects.all().delete()
        PlantSetting.objects.create(**ps_tc.default_plant_settings_7_05)

        self.assertEqual(get_new_hpv_data(), None)


class GetShiftInfoThreeShifts(TestCase):
    def setUp(self):
        PlantSetting.objects.create(**ps_tc.three_shift_8_am_plant_settings)

    @timezone.override("US/Eastern")
    def test_get_shift_info_now_early_3rd_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 3, 0))
        settings = PlantSetting.objects.latest('timestamp')
        expected_start = timezone.make_aware(dt.datetime(2016, 6, 1, 22, 30))
        expected_shift = 3

        self.assertEqual(get_shift_info(settings, now),
                         (expected_start, expected_shift))

    @timezone.override("US/Eastern")
    def test_get_shift_info_now_1st_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 8, 0))
        settings = PlantSetting.objects.latest('timestamp')
        expected_start = timezone.make_aware(dt.datetime(2016, 6, 2, 6, 30))
        expected_shift = 1

        self.assertEqual(get_shift_info(settings, now),
                         (expected_start, expected_shift))

    @timezone.override("US/Eastern")
    def test_get_shift_info_now_2nd_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 0))
        settings = PlantSetting.objects.latest('timestamp')
        expected_start = timezone.make_aware(dt.datetime(2016, 6, 2, 14, 30))
        expected_shift = 2

        self.assertEqual(get_shift_info(settings, now),
                         (expected_start, expected_shift))

    @timezone.override("US/Eastern")
    def test_get_shift_info_now_late_3rd_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 23, 0))
        settings = PlantSetting.objects.latest('timestamp')
        expected_start = timezone.make_aware(dt.datetime(2016, 6, 2, 22, 30))
        expected_shift = 3

        self.assertEqual(get_shift_info(settings, now),
                         (expected_start, expected_shift))


class GetShiftInfoTwoShifts(TestCase):
    def setUp(self):
        PlantSetting.objects.create(**ps_tc.two_shift_8_am_plant_settings)

    @timezone.override("US/Eastern")
    def test_get_shift_info_now_OT_1st_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 3, 0))
        settings = PlantSetting.objects.latest('timestamp')
        expected_start = timezone.make_aware(dt.datetime(2016, 6, 2, 0, 0))
        expected_shift = 1

        self.assertEqual(get_shift_info(settings, now),
                         (expected_start, expected_shift))

    @timezone.override("US/Eastern")
    def test_get_shift_info_now_OT_2nd_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 2, 0))
        settings = PlantSetting.objects.latest('timestamp')
        expected_start = timezone.make_aware(dt.datetime(2016, 6, 1, 14, 30))
        expected_shift = 2

        self.assertEqual(get_shift_info(settings, now),
                         (expected_start, expected_shift))

    @timezone.override("US/Eastern")
    def test_get_shift_info_now_1st_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 8, 0))
        settings = PlantSetting.objects.latest('timestamp')
        expected_start = timezone.make_aware(dt.datetime(2016, 6, 2, 6, 30))
        expected_shift = 1

        self.assertEqual(get_shift_info(settings, now),
                         (expected_start, expected_shift))

    @timezone.override("US/Eastern")
    def test_get_shift_info_now_2nd_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 0))
        settings = PlantSetting.objects.latest('timestamp')
        expected_start = timezone.make_aware(dt.datetime(2016, 6, 2, 14, 30))
        expected_shift = 2

        self.assertEqual(get_shift_info(settings, now),
                         (expected_start, expected_shift))


class GetShiftInfoOneShift(TestCase):
    def setUp(self):
        PlantSetting.objects.create(**ps_tc.one_shift_8_am_plant_settings)

    @timezone.override("US/Eastern")
    def test_get_shift_info_now_before_first_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 1, 0))
        settings = PlantSetting.objects.latest('timestamp')
        expected_start = timezone.make_aware(dt.datetime(2016, 6, 2, 0, 0))
        expected_shift = 1

        self.assertEqual(get_shift_info(settings, now),
                         (expected_start, expected_shift))

    @timezone.override("US/Eastern")
    def test_get_shift_info_now_1st_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 8, 0))
        settings = PlantSetting.objects.latest('timestamp')
        expected_start = timezone.make_aware(dt.datetime(2016, 6, 2, 6, 30))
        expected_shift = 1

        self.assertEqual(get_shift_info(settings, now),
                         (expected_start, expected_shift))

    @timezone.override("US/Eastern")
    def test_get_shift_info_now_evening(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 18, 0))
        settings = PlantSetting.objects.latest('timestamp')
        expected_start = timezone.make_aware(dt.datetime(2016, 6, 2, 6, 30))
        expected_shift = 1

        self.assertEqual(get_shift_info(settings, now),
                         (expected_start, expected_shift))


class GetDayStart(TestCase):
    def test_get_day_start_three_shifts_day_of(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 1, 23, 30))
        PlantSetting.objects.create(**ps_tc.three_shift_8_am_plant_settings)
        settings = PlantSetting.objects.latest('timestamp')
        expected_day_start = timezone.make_aware(dt.datetime(2016, 6, 1, 22, 30))

        self.assertEqual(get_day_start(settings, now), expected_day_start)

    def test_get_day_start_three_shifts_day_after(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 12, 0))
        PlantSetting.objects.create(**ps_tc.three_shift_8_am_plant_settings)
        settings = PlantSetting.objects.latest('timestamp')
        expected_day_start = timezone.make_aware(dt.datetime(2016, 6, 1, 22, 30))

        self.assertEqual(get_day_start(settings, now), expected_day_start)

    def test_get_day_start_less_than_three_shifts(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 12, 0))
        PlantSetting.objects.create(**ps_tc.two_shift_8_am_plant_settings)
        settings = PlantSetting.objects.latest('timestamp')
        expected_day_start = timezone.make_aware(dt.datetime(2016, 6, 2, 6, 30))

        self.assertEqual(get_day_start(settings, now), expected_day_start)


class GetDayStatsThreeShiftsPlant(TestCase):
    def setUp(self):
        PlantSetting.objects.create(**ps_tc.three_shift_8_am_plant_settings)

    def test_get_plant_day_hpv_third_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 1, 23, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_3_hpv_dict_with_plant

        expected_hpv = 90
        expected_mh = 90
        expected_claims = 1

        self.assertEqual(get_plant_day_hpv(hpv_dict, now),
                         (expected_hpv, expected_mh, expected_claims))

    def test_get_plant_day_hpv_third_shift_0_hpv(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 1, 23, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_3_hpv_dict_with_plant_0_hpv

        expected_hpv = 0
        expected_mh = 0
        expected_claims = 0

        self.assertEqual(get_plant_day_hpv(hpv_dict, now),
                         (expected_hpv, expected_mh, expected_claims))

    def test_get_plant_day_hpv_first_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 7, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_1_hpv_dict_with_plant
        HPVATM.objects.create(**api_tc.three_shifts_third_shift_api_entry)

        expected_hpv = 90
        expected_mh = 810
        expected_claims = 9

        self.assertEqual(get_plant_day_hpv(hpv_dict, now),
                         (expected_hpv, expected_mh, expected_claims))

    def test_get_plant_day_hpv_first_shift_0_hpv(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 7, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_1_hpv_dict_with_plant_0_hpv
        HPVATM.objects.create(**api_tc.three_shifts_third_shift_api_entry)

        expected_hpv = 90
        expected_mh = 720
        expected_claims = 8

        self.assertEqual(get_plant_day_hpv(hpv_dict, now),
                         (expected_hpv, expected_mh, expected_claims))

    def test_get_plant_day_hpv_first_shift_0_claims(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 7, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_1_hpv_dict_with_plant_0_hpv
        HPVATM.objects.create(**api_tc.three_shifts_third_shift_api_entry_0_claims)

        expected_hpv = 0
        expected_mh = 720
        expected_claims = 0

        self.assertEqual(get_plant_day_hpv(hpv_dict, now),
                         (expected_hpv, expected_mh, expected_claims))

    def test_get_plant_day_hpv_first_shift_no_api_entries(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 7, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_1_hpv_dict_with_plant

        expected_hpv = 90
        expected_mh = 90
        expected_claims = 1

        self.assertEqual(get_plant_day_hpv(hpv_dict, now),
                         (expected_hpv, expected_mh, expected_claims))

    def test_get_plant_day_hpv_second_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_2_hpv_dict_with_plant
        HPVATM.objects.create(**api_tc.three_shifts_third_shift_api_entry)
        HPVATM.objects.create(**api_tc.three_shifts_first_shift_api_entry)

        expected_hpv = 90
        expected_mh = 1530
        expected_claims = 17

        self.assertEqual(get_plant_day_hpv(hpv_dict, now),
                         (expected_hpv, expected_mh, expected_claims))

    def test_get_plant_day_hpv_second_shift_0_hpv(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_2_hpv_dict_with_plant_0_hpv
        HPVATM.objects.create(**api_tc.three_shifts_third_shift_api_entry)
        HPVATM.objects.create(**api_tc.three_shifts_first_shift_api_entry)

        expected_hpv = 90
        expected_mh = 1440
        expected_claims = 16

        self.assertEqual(get_plant_day_hpv(hpv_dict, now),
                         (expected_hpv, expected_mh, expected_claims))

    def test_get_plant_day_hpv_second_shift_0_claims(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_2_hpv_dict_with_plant_0_hpv
        HPVATM.objects.create(**api_tc.three_shifts_third_shift_api_entry_0_claims)
        HPVATM.objects.create(**api_tc.three_shifts_first_shift_api_entry_0_claims)

        expected_hpv = 0
        expected_mh = 1440
        expected_claims = 0

        self.assertEqual(get_plant_day_hpv(hpv_dict, now),
                         (expected_hpv, expected_mh, expected_claims))

    def test_get_plant_day_hpv_second_shift_no_third_shift_api_entry(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_2_hpv_dict_with_plant
        HPVATM.objects.create(**api_tc.three_shifts_first_shift_api_entry)

        expected_hpv = 90
        expected_mh = 810
        expected_claims = 9

        self.assertEqual(get_plant_day_hpv(hpv_dict, now),
                         (expected_hpv, expected_mh, expected_claims))

    def test_get_plant_day_hpv_second_shift_no_first_shift_api_entry(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_2_hpv_dict_with_plant
        HPVATM.objects.create(**api_tc.three_shifts_third_shift_api_entry)

        expected_hpv = 90
        expected_mh = 810
        expected_claims = 9

        self.assertEqual(get_plant_day_hpv(hpv_dict, now),
                         (expected_hpv, expected_mh, expected_claims))

    def test_get_plant_day_hpv_second_shift_no_api_entries(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_2_hpv_dict_with_plant

        expected_hpv = 90
        expected_mh = 90
        expected_claims = 1

        self.assertEqual(get_plant_day_hpv(hpv_dict, now),
                        (expected_hpv, expected_mh, expected_claims))


class GetDayStatsTwoShiftsPlant(TestCase):
    def setUp(self):
        PlantSetting.objects.create(**ps_tc.two_shift_8_am_plant_settings)

    def test_get_plant_day_hpv_first_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 7, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_1_hpv_dict_with_plant

        expected_hpv = 90
        expected_mh = 90
        expected_claims = 1

        self.assertEqual(get_plant_day_hpv(hpv_dict, now),
                         (expected_hpv, expected_mh, expected_claims))

    def test_get_plant_day_hpv_first_shift_0_hpv(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 7, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_1_hpv_dict_with_plant_0_hpv

        expected_hpv = 0
        expected_mh = 0
        expected_claims = 0

        self.assertEqual(get_plant_day_hpv(hpv_dict, now),
                         (expected_hpv, expected_mh, expected_claims))

    def test_get_plant_day_hpv_second_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_2_hpv_dict_with_plant
        HPVATM.objects.create(**api_tc.two_shifts_first_shift_api_entry)

        expected_hpv = 90
        expected_mh = 810
        expected_claims = 9

        self.assertEqual(get_plant_day_hpv(hpv_dict, now),
                         (expected_hpv, expected_mh, expected_claims))

    def test_get_plant_day_hpv_second_shift_0_hpv(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_2_hpv_dict_with_plant_0_hpv
        HPVATM.objects.create(**api_tc.two_shifts_first_shift_api_entry)

        expected_hpv = 90
        expected_mh = 720
        expected_claims = 8

        self.assertEqual(get_plant_day_hpv(hpv_dict, now),
                         (expected_hpv, expected_mh, expected_claims))

    def test_get_plant_day_hpv_second_shift_0_claims(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_2_hpv_dict_with_plant_0_hpv
        HPVATM.objects.create(**api_tc.two_shifts_first_shift_api_entry_0_claims)

        expected_hpv = 0
        expected_mh = 720
        expected_claims = 0

        self.assertEqual(get_plant_day_hpv(hpv_dict, now),
                         (expected_hpv, expected_mh, expected_claims))

    def test_get_plant_day_hpv_second_shift_no_first_shift_api_entry(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_2_hpv_dict_with_plant

        expected_hpv = 90
        expected_mh = 90
        expected_claims = 1

        self.assertEqual(get_plant_day_hpv(hpv_dict, now),
                         (expected_hpv, expected_mh, expected_claims))


class GetDayStatsOneShiftPlant(TestCase):
    def setUp(self):
        PlantSetting.objects.create(**ps_tc.one_shift_8_am_plant_settings)

    def test_get_plant_day_hpv_first_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 7, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_1_hpv_dict_with_plant

        expected_hpv = 90
        expected_mh = 90
        expected_claims = 1

        self.assertEqual(get_plant_day_hpv(hpv_dict, now),
                         (expected_hpv, expected_mh, expected_claims))

    def test_get_plant_day_hpv_first_shift_0_hpv(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 7, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_1_hpv_dict_with_plant_0_hpv

        expected_hpv = 0
        expected_mh = 0
        expected_claims = 0

        self.assertEqual(get_plant_day_hpv(hpv_dict, now),
                         (expected_hpv, expected_mh, expected_claims))


class GetDayStatsThreeShiftsDept(TestCase):
    def setUp(self):
        PlantSetting.objects.create(**ps_tc.three_shift_8_am_plant_settings)

    def test_get_dept_day_stats_third_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 1, 23, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_3_hpv_dict
        dept_list = ['CIW', 'FCB', 'PNT', 'PCH', 'FCH', 'DAC', 'MAINT', 'QA', 'MAT', 'OTHER']

        expected_hpv = 10
        expected_mh = 10

        for dept in dept_list:
            if dept == 'OTHER':
                expected_hpv = 0
                expected_mh = 0
            self.assertEqual(get_dept_day_stats(hpv_dict, now, dept),
                             (expected_hpv, expected_mh))

    def test_get_dept_day_stats_first_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 7, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_1_hpv_dict
        HPVATM.objects.create(**api_tc.three_shifts_third_shift_api_entry)

        dept_list = ['CIW', 'FCB', 'PNT', 'PCH', 'FCH', 'DAC', 'MAINT', 'QA', 'MAT', 'OTHER']

        expected_hpv = 10
        expected_mh = 90

        for dept in dept_list:
            if dept == 'OTHER':
                expected_hpv = 0
                expected_mh = 0
            self.assertEqual(get_dept_day_stats(hpv_dict, now, dept),
                             (expected_hpv, expected_mh))

    def test_get_dept_day_stats_first_shift_0_claims(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 7, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_1_hpv_dict_0_hpv
        HPVATM.objects.create(**api_tc.three_shifts_third_shift_api_entry_0_claims)

        dept_list = ['CIW', 'FCB', 'PNT', 'PCH', 'FCH', 'DAC', 'MAINT', 'QA', 'MAT', 'OTHER']

        expected_hpv = 0
        expected_mh = 80

        for dept in dept_list:
            if dept == 'OTHER':
                expected_hpv = 0
                expected_mh = 0
            self.assertEqual(get_dept_day_stats(hpv_dict, now, dept),
                             (expected_hpv, expected_mh))

    def test_get_dept_day_stats_first_shift_no_third_shift_api_entry(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 7, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_1_hpv_dict

        dept_list = ['CIW', 'FCB', 'PNT', 'PCH', 'FCH', 'DAC', 'MAINT', 'QA', 'MAT', 'OTHER']

        expected_hpv = 10
        expected_mh = 10

        for dept in dept_list:
            if dept == 'OTHER':
                expected_hpv = 0
                expected_mh = 0
            self.assertEqual(get_dept_day_stats(hpv_dict, now, dept),
                             (expected_hpv, expected_mh))

    def test_get_dept_day_stats_second_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_2_hpv_dict
        HPVATM.objects.create(**api_tc.three_shifts_third_shift_api_entry)
        HPVATM.objects.create(**api_tc.three_shifts_first_shift_api_entry)

        dept_list = ['CIW', 'FCB', 'PNT', 'PCH', 'FCH', 'DAC', 'MAINT', 'QA', 'MAT', 'OTHER']

        expected_hpv = 10
        expected_mh = 170

        for dept in dept_list:
            if dept == 'OTHER':
                expected_hpv = 0
                expected_mh = 0
            self.assertEqual(get_dept_day_stats(hpv_dict, now, dept),
                             (expected_hpv, expected_mh))

    def test_get_dept_day_stats_second_shift_0_claims(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_2_hpv_dict_0_hpv
        HPVATM.objects.create(**api_tc.three_shifts_third_shift_api_entry_0_claims)
        HPVATM.objects.create(**api_tc.three_shifts_first_shift_api_entry_0_claims)

        dept_list = ['CIW', 'FCB', 'PNT', 'PCH', 'FCH', 'DAC', 'MAINT', 'QA', 'MAT', 'OTHER']

        expected_hpv = 0
        expected_mh = 160

        for dept in dept_list:
            if dept == 'OTHER':
                expected_hpv = 0
                expected_mh = 0
            self.assertEqual(get_dept_day_stats(hpv_dict, now, dept),
                             (expected_hpv, expected_mh))

    def test_get_dept_day_stats_second_shift_no_api_entries(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_2_hpv_dict

        dept_list = ['CIW', 'FCB', 'PNT', 'PCH', 'FCH', 'DAC', 'MAINT', 'QA', 'MAT', 'OTHER']

        expected_hpv = 10
        expected_mh = 10

        for dept in dept_list:
            if dept == 'OTHER':
                expected_hpv = 0
                expected_mh = 0
            self.assertEqual(get_dept_day_stats(hpv_dict, now, dept),
                             (expected_hpv, expected_mh))

    def test_get_dept_day_stats_second_shift_no_third_shift_api_entry(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_2_hpv_dict
        HPVATM.objects.create(**api_tc.three_shifts_first_shift_api_entry)

        dept_list = ['CIW', 'FCB', 'PNT', 'PCH', 'FCH', 'DAC', 'MAINT', 'QA', 'MAT', 'OTHER']

        expected_hpv = 10
        expected_mh = 90

        for dept in dept_list:
            if dept == 'OTHER':
                expected_hpv = 0
                expected_mh = 0
            self.assertEqual(get_dept_day_stats(hpv_dict, now, dept),
                             (expected_hpv, expected_mh))

    def test_get_dept_day_stats_second_shift_no_first_shift_api_entry(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_2_hpv_dict
        HPVATM.objects.create(**api_tc.three_shifts_third_shift_api_entry)

        dept_list = ['CIW', 'FCB', 'PNT', 'PCH', 'FCH', 'DAC', 'MAINT', 'QA', 'MAT', 'OTHER']

        expected_hpv = 10
        expected_mh = 90

        for dept in dept_list:
            if dept == 'OTHER':
                expected_hpv = 0
                expected_mh = 0
            self.assertEqual(get_dept_day_stats(hpv_dict, now, dept),
                             (expected_hpv, expected_mh))


class GetDayStatsTwoShiftsDept(TestCase):
    def setUp(self):
        PlantSetting.objects.create(**ps_tc.two_shift_8_am_plant_settings)

    def test_get_dept_day_stats_first_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 7, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_1_hpv_dict
        dept_list = ['CIW', 'FCB', 'PNT', 'PCH', 'FCH', 'DAC', 'MAINT', 'QA', 'MAT', 'OTHER']

        expected_hpv = 10
        expected_mh = 10

        for dept in dept_list:
            if dept == 'OTHER':
                expected_hpv = 0
                expected_mh = 0
            self.assertEqual(get_dept_day_stats(hpv_dict, now, dept),
                             (expected_hpv, expected_mh))

    def test_get_dept_day_stats_second_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_2_hpv_dict
        HPVATM.objects.create(**api_tc.two_shifts_first_shift_api_entry)
        dept_list = ['CIW', 'FCB', 'PNT', 'PCH', 'FCH', 'DAC', 'MAINT', 'QA', 'MAT', 'OTHER']

        expected_hpv = 10
        expected_mh = 90

        for dept in dept_list:
            if dept == 'OTHER':
                expected_hpv = 0
                expected_mh = 0
            self.assertEqual(get_dept_day_stats(hpv_dict, now, dept),
                             (expected_hpv, expected_mh))

    def test_get_dept_day_stats_second_shift_0_claims(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_2_hpv_dict_0_hpv
        HPVATM.objects.create(**api_tc.two_shifts_first_shift_api_entry_0_claims)
        dept_list = ['CIW', 'FCB', 'PNT', 'PCH', 'FCH', 'DAC', 'MAINT', 'QA', 'MAT', 'OTHER']

        expected_hpv = 0
        expected_mh = 80

        for dept in dept_list:
            if dept == 'OTHER':
                expected_hpv = 0
                expected_mh = 0
            self.assertEqual(get_dept_day_stats(hpv_dict, now, dept),
                             (expected_hpv, expected_mh))

    def test_get_dept_day_stats_second_shift_no_api_entries(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_2_hpv_dict
        dept_list = ['CIW', 'FCB', 'PNT', 'PCH', 'FCH', 'DAC', 'MAINT', 'QA', 'MAT', 'OTHER']

        expected_hpv = 10
        expected_mh = 10

        for dept in dept_list:
            if dept == 'OTHER':
                expected_hpv = 0
                expected_mh = 0
            self.assertEqual(get_dept_day_stats(hpv_dict, now, dept),
                             (expected_hpv, expected_mh))


class GetDayStatsOneShiftDept(TestCase):
    def setUp(self):
        PlantSetting.objects.create(**ps_tc.one_shift_8_am_plant_settings)

    def test_get_dept_day_stats_first_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 7, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_1_hpv_dict
        dept_list = ['CIW', 'FCB', 'PNT', 'PCH', 'FCH', 'DAC', 'MAINT', 'QA', 'MAT', 'OTHER']

        expected_hpv = 10
        expected_mh = 10

        for dept in dept_list:
            if dept == 'OTHER':
                expected_hpv = 0
                expected_mh = 0
            self.assertEqual(get_dept_day_stats(hpv_dict, now, dept),
                             (expected_hpv, expected_mh))


class GetDayHpvDict(TestCase):
    def setUp(self):
        PlantSetting.objects.create(**ps_tc.two_shift_8_am_plant_settings)

    def test_get_day_hpv_dict(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hpv_dict = tc.shift_2_hpv_dict_with_plant
        HPVATM.objects.create(**api_tc.two_shifts_first_shift_api_entry)

        expected_full_hpv_dict = tc.expected_full_hpv_dict

        self.assertEqual(get_day_hpv_dict(hpv_dict, now),
                         expected_full_hpv_dict)


class DeleteOldEntries(TestCase):
    def setUp(self):
        # Deletes after 1 day
        PlantSetting.objects.create(**ps_tc.default_plant_settings_with_del)
        # API 6/2 @ 7:00
        HPVATM.objects.create(**api_tc.two_shifts_first_shift_api_entry_7_am)
        # API 6/2 @ 14:30
        HPVATM.objects.create(**api_tc.two_shifts_first_shift_api_entry)

    def test_delete_old_entries(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 3, 12, 30))
        plant_settings = PlantSetting.objects.latest('timestamp')
        delete_old_entries(plant_settings, now)

        self.assertEqual(HPVATM.objects.count(), 1)


class NeedToWrite(TestCase):
    def setUp(self):
        PlantSetting.objects.create(**ps_tc.default_plant_settings_20_30)

        RawPlantActivity.objects.create(
            VEH_SER_NO='HZ3852',
            POOL_CD='03',
            TS_LOAD=timezone.make_aware(dt.datetime(2016, 6, 2, 6, 55)),
        )

    def test_need_to_write_true_and_near_end(self):
        HPVATM.objects.create(**api_tc.two_shifts_first_shift_api_entry_7_am)
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 14, 27))
        plant_settings = PlantSetting.objects.latest('timestamp')
        last_api_write = HPVATM.objects.filter(timestamp__lte=now)
        last_api_write = last_api_write.latest('timestamp')
        last_claim = RawPlantActivity.objects.filter(POOL_CD='03',
                                                     TS_LOAD__lte=now)
        last_claim = last_claim.latest('TS_LOAD')

        self.assertEqual(need_to_write(now, plant_settings, last_api_write, last_claim), True)

    def test_need_to_write_true_and_not_near_end(self):
        HPVATM.objects.create(**api_tc.two_shifts_first_shift_api_entry_7_am)
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 12, 30))
        plant_settings = PlantSetting.objects.latest('timestamp')
        last_api_write = HPVATM.objects.filter(timestamp__lte=now)
        last_api_write = last_api_write.latest('timestamp')
        last_claim = RawPlantActivity.objects.filter(POOL_CD='03',
                                                     TS_LOAD__lte=now)
        last_claim = last_claim.latest('TS_LOAD')

        self.assertEqual(need_to_write(now, plant_settings, last_api_write, last_claim), True)

    def test_need_to_write_false_and_near_end(self):
        HPVATM.objects.create(**api_tc.two_shifts_first_shift_api_entry)
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 14, 27))
        plant_settings = PlantSetting.objects.latest('timestamp')
        last_api_write = HPVATM.objects.filter(timestamp__lte=now)
        last_api_write = last_api_write.latest('timestamp')
        last_claim = RawPlantActivity.objects.filter(POOL_CD='03',
                                                     TS_LOAD__lte=now)
        last_claim = last_claim.latest('TS_LOAD')

        self.assertEqual(need_to_write(now, plant_settings, last_api_write, last_claim), True)

    def test_need_to_write_false_and_not_near_end(self):
        HPVATM.objects.create(**api_tc.two_shifts_first_shift_api_entry_7_am)
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 7, 5))
        plant_settings = PlantSetting.objects.latest('timestamp')
        last_api_write = HPVATM.objects.filter(timestamp__lte=now)
        last_api_write = last_api_write.latest('timestamp')
        last_claim = RawPlantActivity.objects.filter(POOL_CD='03',
                                                     TS_LOAD__lte=now)
        last_claim = last_claim.latest('TS_LOAD')

        self.assertEqual(need_to_write(now, plant_settings, last_api_write, last_claim), False)
