from django.test import TestCase
from rest_framework.test import APIRequestFactory
from .models import HPVATM
from .views import HPVAPI
import pytz
import datetime as dt

class HPVAPITest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = APIRequestFactory()

        # Create 2 test objects
        HPVATM.objects.create(timestamp=pytz.utc.localize(dt.datetime(2016, 6, 1, 10, 30)), hpv_plant=89.9)

        HPVATM.objects.create(timestamp=pytz.utc.localize(dt.datetime(2016, 6, 1, 15, 30)), hpv_plant=86.7)

    def test_view(self):
        request = self.factory.get('/api/hpv')

        response = HPVAPI.as_view()(request)
        self.assertEqual(response.status_code, 200)
        # self.assertEqual()
