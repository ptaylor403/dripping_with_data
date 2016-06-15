from django.test import TestCase
from get_data.models import RawPlantActivity
from django.utils import timezone
import datetime as dt

from data_processor.functions.claims_calculations import get_claimed_objects_in_range, get_range_of_claims

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