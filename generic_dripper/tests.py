from django.test import TestCase
from .models import CompleteDripper
from hpv.models import Complete
import datetime as dt
import pytz


class test_dripper_load_one(TestCase):
    time1 = dt.datetime.now(pytz.utc)

    def setUp(self):
        Complete.objects.create(serial_number="1", completed=self.time1)

    def test_load(self):
        CompleteDripper.load_from_Complete()
        assert(CompleteDripper.objects.count() == 1)
        for entry in CompleteDripper.objects.all():
            assert(entry.serial_number == "1")
            assert(entry.completed == self.time1)
            assert(entry.create_at == self.time1)


class test_dripper_load_many(TestCase):
    time1 = dt.datetime.now(pytz.utc)
    times = []
    for i in range(10):
        times.append(time1 + dt.timedelta(hours=i))
    serial_numbers = [str(x) for x in range(1, 11)]

    def setUp(self):
        for time, serial_number in zip(self.times, self.serial_numbers):
            Complete.objects.create(serial_number=serial_number,
                                    completed=time)

    def test_load(self):
        CompleteDripper.load_from_Complete()
        assert(CompleteDripper.objects.count() == len(self.times))
        for i, entry in enumerate(CompleteDripper.objects.all()):
            assert(entry.serial_number == self.serial_numbers[i])
            assert(entry.completed == self.times[i])
            assert(entry.create_at == self.times[i])


class test_dripper_one_drip(TestCase):
    time1 = dt.datetime.now(pytz.utc)

    def setUp(self):
        CompleteDripper.objects.create(serial_number="1", completed=self.time1,
                                       create_at=self.time1)

    def test_one_drip(self):
        one_hour = dt.timedelta(hours=1)
        CompleteDripper.create_on_Complete(self.time1 - one_hour,
                                           self.time1 + one_hour)
        assert(Complete.objects.count() == 1)
        for entry in Complete.objects.all():
            assert(entry.serial_number == "1")
            assert(entry.completed == self.time1)


class test_dripper_drips(TestCase):
    time1 = dt.datetime.now(pytz.utc)
    times = []
    for i in range(10):
        times.append(time1 + dt.timedelta(hours=i))
    serial_numbers = [str(x) for x in range(1, 11)]

    def setUp(self):
        for time, serial_number in zip(self.times, self.serial_numbers):
            CompleteDripper.objects.create(serial_number=serial_number,
                                           completed=time, create_at=time)

    def test_small_drips(self):
        last_time = self.time1 - dt.timedelta(hours=1)
        for i, t in enumerate(self.times):
            CompleteDripper.create_on_Complete(last_time, t)
            assert(Complete.objects.count() == i+1)
            for entry, time, serial_number in zip(Complete.objects.all(),
                                                  self.times[:i],
                                                  self.serial_numbers[:i]):
                assert(entry.serial_number == serial_number)
                assert(entry.completed == time)
            last_time = t

    def test_big_drips(self):
        last_time = self.time1 - dt.timedelta(hours=1)
        for i, t in enumerate(self.times):
            if i != len(self.times)-1 and i % 2 == 0:
                continue
            CompleteDripper.create_on_Complete(last_time, t)
            assert(Complete.objects.count() == i+1)
            for entry, time, serial_number in zip(Complete.objects.all(),
                                                  self.times[:i],
                                                  self.serial_numbers[:i]):
                assert(entry.serial_number == serial_number)
                assert(entry.completed == time)
            last_time = t

    def test_very_small_drips(self):
        last_time = self.time1 - dt.timedelta(hours=1)
        for i, t in enumerate(self.times):
            for j in range(2):
                k = i + j
                if j == 0:
                    small_t = last_time + ((t - last_time) / 2)
                else:
                    small_t = t
                CompleteDripper.create_on_Complete(last_time, small_t)
                assert(Complete.objects.count() == k)
                for entry, time, serial_number in zip(Complete.objects.all(),
                                                      self.times[:k],
                                                      self.serial_numbers[:k]):
                    assert(entry.serial_number == serial_number)
                    assert(entry.completed == time)
                last_time = small_t
