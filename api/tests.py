from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth.models import User
from .models import HPVATM
from .views import HPVAPI
import pytz
import datetime as dt


class HPVAPITest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = APIRequestFactory()
        User.objects.create(username='cameron', password='password123')

        # Create 2 test objects
        HPVATM.objects.create(timestamp=pytz.utc.localize(dt.datetime(2016, 6, 1, 10, 30, 0, 0)), hpv_plant=89.9)

        HPVATM.objects.create(timestamp=pytz.utc.localize(dt.datetime(2016, 6, 1, 15, 30, 0, 0)), hpv_plant=86.7)


    def test_list_view(self):
        request = self.factory.get('/api/hpv')
        user = User.objects.get(username='cameron')
        force_authenticate(request, user='cameron')
        response = HPVAPI.as_view()(request)

        # Gets 200 response code
        self.assertEqual(response.status_code, 200)
        # Returns only 2 results for 2 items in the table
        self.assertEqual(len(response.data), 2)
        # Returns the correct HPV when querying the response data
        self.assertEqual(response.data[0]['hpv_plant'], '89.9')
        self.assertEqual(response.data[1]['hpv_plant'], '86.7')
