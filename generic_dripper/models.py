from django.db import models
from hpv.models import Attendance, Complete
import datetime as dt
from django.utils import timezone
from get_data.models import RawClockData, RawPlantActivity
# Model._meta.get_all_field_names()


class AttendanceDripper(models.Model):
    employee_number = models.IntegerField()
    department = models.CharField(max_length=16)
    clock_in_time = models.DateTimeField()
    clock_out_time = models.DateTimeField(null=True, blank=True)
    shift = models.CharField(max_length=16)
    create_at = models.DateTimeField()
    edit_1_at = models.DateTimeField(null=True)
    target = Attendance
    last_drip = timezone.make_aware(dt.datetime(1, 1, 1, 0, 0))

    @classmethod
    def load_from_target(cls):
        for entry in cls.target.objects.all():
            AttendanceDripper.objects.create(employee_number=entry.employee_number,
                                             department=entry.department,
                                             clock_in_time=entry.clock_in_time,
                                             clock_out_time=entry.clock_out_time,
                                             shift=entry.shift,
                                             create_at=entry.clock_in_time,
                                             edit_1_at=entry.clock_out_time)

    @classmethod
    def _create_on_target(cls, stop):
        relevant = cls.objects.filter(create_at__gt=cls.last_drip)
        relevant = relevant.filter(create_at__lte=stop)
        for entry in relevant.order_by('pk'):
            cls.target.objects.create(employee_number=entry.employee_number,
                                      department=entry.department,
                                      clock_in_time=entry.clock_in_time,
                                      clock_out_time=None,
                                      shift=entry.shift,)

    @classmethod
    def _edit_1_on_target(cls, stop):
        relevant = cls.objects.filter(edit_1_at__gt=cls.last_drip)
        relevant = relevant.filter(edit_1_at__lte=stop)
        for entry in relevant.order_by('pk'):
            cls.target.objects.filter(employee_number=entry.employee_number,
                                      clock_in_time=entry.clock_in_time).update(
                                      clock_out_time=entry.clock_out_time)

    @classmethod
    def update_target(cls, *args, **kwargs):
        cls._create_on_target(*args, **kwargs)
        cls._edit_1_on_target(*args, **kwargs)
        if "stop" in kwargs:
            stop = kwargs['stop']
        else:
            stop = args[0]
        cls.last_drip = stop


class CompleteDripper(models.Model):
    serial_number = models.CharField(max_length=10)
    completed = models.DateTimeField()
    create_at = models.DateTimeField()
    target = Complete
    last_drip = timezone.make_aware(dt.datetime(1, 1, 1, 0, 0))

    @classmethod
    def load_from_target(cls):
        for entry in cls.target.objects.order_by('pk'):
            cls.objects.create(serial_number=entry.serial_number,
                               completed=entry.completed,
                               create_at=entry.completed)

    @classmethod
    def _create_on_target(cls, stop):
        relevant = cls.objects.filter(create_at__gt=cls.last_drip)
        relevant = relevant.filter(create_at__lte=stop)
        for entry in relevant.order_by('pk'):
            cls.target.objects.create(serial_number=entry.serial_number,
                                      completed=entry.completed)

    @classmethod
    def update_target(cls, *args, **kwargs):
        cls._create_on_target(*args, **kwargs)
        if "stop" in kwargs:
            stop = kwargs['stop']
        else:
            stop = args[0]
        cls.last_drip = stop


class RawClockDataDripper(models.Model):
    PRSN_NBR_TXT = models.CharField(max_length=100)
    full_nam = models.TextField()
    HM_LBRACCT_FULL_NAM = models.TextField()
    start_rsn_txt = models.CharField(max_length=100, null=True)
    PNCHEVNT_IN = models.DateTimeField(null=True, blank=True)
    end_rsn_txt = models.CharField(max_length=100, null=True)
    PNCHEVNT_OUT = models.DateTimeField(null=True, blank=True)
    create_at = models.DateTimeField(null=True)
    edit_1_at = models.DateTimeField(null=True)
    edit_2_at = models.DateTimeField(null=True)
    target = RawClockData
    last_drip = timezone.make_aware(dt.datetime(1, 1, 1, 0, 0))

    @classmethod
    def load_from_target(cls):
        with timezone.override("US/Eastern"):
            earliest_time = timezone.localtime(cls.target.objects.earliest('PNCHEVNT_IN').PNCHEVNT_IN)
            for entry in cls.target.objects.order_by('pk'):
                if entry.start_rsn_txt in [None, "&newShift"]:
                    create_time = dt.datetime.combine(earliest_time, dt.time(hour=3))
                    create_time = timezone.make_aware(create_time)
                else:
                    create_time = entry.PNCHEVNT_IN
                cls.objects.create(PRSN_NBR_TXT=entry.PRSN_NBR_TXT,
                                   full_nam=entry.full_nam,
                                   HM_LBRACCT_FULL_NAM=entry.HM_LBRACCT_FULL_NAM,
                                   start_rsn_txt=entry.start_rsn_txt,
                                   PNCHEVNT_IN=entry.PNCHEVNT_IN,
                                   end_rsn_txt=entry.end_rsn_txt,
                                   PNCHEVNT_OUT=entry.PNCHEVNT_OUT,
                                   create_at=create_time,
                                   edit_1_at=entry.PNCHEVNT_IN,
                                   edit_2_at=entry.PNCHEVNT_OUT)
                if entry.PNCHEVNT_IN is not None:
                    earliest_time = entry.PNCHEVNT_IN

    @classmethod
    def _create_on_target(cls, stop):
        relevant = cls.objects.filter(create_at__gt=cls.last_drip)
        relevant = relevant.filter(create_at__lte=stop)
        for entry in relevant.order_by('pk'):
            cls.target.objects.create(PRSN_NBR_TXT=entry.PRSN_NBR_TXT,
                                      full_nam=entry.full_nam,
                                      HM_LBRACCT_FULL_NAM=entry.HM_LBRACCT_FULL_NAM,
                                      start_rsn_txt=None,
                                      PNCHEVNT_IN=None,
                                      end_rsn_txt=None,
                                      PNCHEVNT_OUT=None)

    @classmethod
    def _edit_1_on_target(cls, stop):
        relevant = cls.objects.filter(edit_1_at__gt=cls.last_drip)
        relevant = relevant.filter(edit_1_at__lte=stop)
        for entry in relevant.order_by('pk'):
            to_update = cls.target.objects.filter(PRSN_NBR_TXT=entry.PRSN_NBR_TXT,
                                                  full_nam=entry.full_nam,
                                                  HM_LBRACCT_FULL_NAM=entry.HM_LBRACCT_FULL_NAM).last()
            if to_update:
                to_update.PNCHEVNT_IN = entry.PNCHEVNT_IN
                to_update.start_rsn_txt = entry.start_rsn_txt
                to_update.end_rsn_txt = "&missedOut"
                to_update.save()

    @classmethod
    def _edit_2_on_target(cls, stop):
        relevant = cls.objects.filter(edit_2_at__gt=cls.last_drip)
        relevant = relevant.filter(edit_2_at__lte=stop)
        for entry in relevant.order_by('pk'):
            cls.target.objects.filter(HM_LBRACCT_FULL_NAM=entry.HM_LBRACCT_FULL_NAM,
                                      PNCHEVNT_IN=entry.PNCHEVNT_IN).update(
                                      end_rsn_txt=entry.end_rsn_txt,
                                      PNCHEVNT_OUT=entry.PNCHEVNT_OUT)

    @classmethod
    def update_target(cls, *args, **kwargs):
        cls._create_on_target(*args, **kwargs)
        cls._edit_1_on_target(*args, **kwargs)
        cls._edit_2_on_target(*args, **kwargs)
        if "stop" in kwargs:
            stop = kwargs['stop']
        else:
            stop = args[0]
        cls.last_drip = stop


class RawPlantActivityDripper(models.Model):
    VEH_SER_NO = models.CharField(max_length=6)
    POOL_CD = models.CharField(max_length=10)
    TS_LOAD = models.DateTimeField()
    create_at = models.DateTimeField()
    target = RawPlantActivity
    last_drip = timezone.make_aware(dt.datetime(1, 1, 1, 0, 0))

    @classmethod
    def load_from_target(cls):
        for entry in cls.target.objects.all():
            cls.objects.create(VEH_SER_NO=entry.VEH_SER_NO,
                               POOL_CD=entry.POOL_CD,
                               TS_LOAD=entry.TS_LOAD,
                               create_at=entry.TS_LOAD
                               )

    @classmethod
    def _create_on_target(cls, stop):
        relevant = cls.objects.filter(create_at__gt=cls.last_drip)
        relevant = relevant.filter(create_at__lte=stop)
        for entry in relevant.order_by('pk'):
            cls.target.objects.create(VEH_SER_NO=entry.VEH_SER_NO,
                                      POOL_CD=entry.POOL_CD,
                                      TS_LOAD=entry.TS_LOAD,
                                      )
    @classmethod
    def update_target(cls, *args, **kwargs):
        cls._create_on_target(*args, **kwargs)
        if "stop" in kwargs:
            stop = kwargs['stop']
        else:
            stop = args[0]
        cls.last_drip = stop


class CombinedDripper:
    drippers = []

    def __init__(self, start_time, time_step=dt.timedelta(minutes=5)):
        self.simulated_time = start_time
        self.time_step = time_step

    def add_dripper(self, *args):
        for dripper in args:
            if dripper not in self.drippers:
                self.drippers.append(dripper)
                dripper.update_target(self.simulated_time)

    def update_to(self, new_time):
        for dripper in self.drippers:
            dripper.update_target(new_time)
        self.simulated_time = new_time

    def update_by(self, time_step):
        new_time = self.simulated_time + time_step
        self.update_to(new_time)

    def update(self):
        self.update_by(self.time_step)

    def clear_targets(self):
        for dripper in self.drippers:
            dripper.target.objects.all().delete()
            dripper.last_drip = timezone.make_aware(dt.datetime(1, 1, 1, 0, 0))

    def load_drippers(self):
        for dripper in self.drippers:
            dripper.load_from_target()

    def clear_drippers(self):
        for dripper in self.drippers:
            dripper.objects.all().delete()


#######################################################
# Unused models
#######################################################
# class RawCrysDataDripper(models.Model):
#     QA_ITEM_DSCREP_ID = models.CharField(max_length=255)
#     QA_INSP_ITEM_ID = models.CharField(max_length=255)
#     VEH_SER_NO = models.CharField(max_length=6)
#     FOUND_INSP_TEAM = models.CharField(max_length=3)
#     INSP_DSCREP_DESC = models.CharField(max_length=255)
#     INSP_COMT = models.TextField()
#     TS_LOAD = models.DateTimeField()
#     create_at = models.DateTimeField()
#     target = RawCrysData
#     last_drip = timezone.make_aware(dt.datetime(1, 1, 1, 0, 0))
#
#     @classmethod
#     def load_from_target(cls):
#         for entry in cls.target.objects.all():
#             cls.objects.create(QA_ITEM_DSCREP_ID=entry.QA_ITEM_DSCREP_ID,
#                                QA_INSP_ITEM_ID=entry.QA_INSP_ITEM_ID,
#                                VEH_SER_NO=entry.VEH_SER_NO,
#                                FOUND_INSP_TEAM=entry.FOUND_INSP_TEAM,
#                                INSP_DSCREP_DESC=entry.INSP_DSCREP_DESC,
#                                INSP_COMT=entry.INSP_COMT,
#                                TS_LOAD=entry.TS_LOAD,
#                                create_at=entry.TS_LOAD
#                                )
#
#     @classmethod
#     def _create_on_target(cls, stop):
#         relevant = cls.objects.filter(create_at__gt=cls.last_drip)
#         relevant = relevant.filter(create_at__lte=stop)
#         for entry in relevant.order_by('pk'):
#             cls.target.objects.create(QA_ITEM_DSCREP_ID=entry.QA_ITEM_DSCREP_ID,
#                                       QA_INSP_ITEM_ID=entry.QA_INSP_ITEM_ID,
#                                       VEH_SER_NO=entry.VEH_SER_NO,
#                                       FOUND_INSP_TEAM=entry.FOUND_INSP_TEAM,
#                                       INSP_DSCREP_DESC=entry.INSP_DSCREP_DESC,
#                                       INSP_COMT=entry.INSP_COMT,
#                                       TS_LOAD=entry.TS_LOAD
#                                       )
#
#     @classmethod
#     def update_target(cls, *args, **kwargs):
#         cls._create_on_target(*args, **kwargs)
#         if "stop" in kwargs:
#             stop = kwargs['stop']
#         else:
#             stop = args[0]
#         cls.last_drip = stop
#
# class RawDirectRunDataDripper(models.Model):
#     VEH_SER_NO = models.CharField(max_length=6)
#     TS_LOAD = models.DateTimeField()
#     SHIFT = models.IntegerField()
#     QA = models.IntegerField()
#     PAINT = models.IntegerField()
#     SH = models.IntegerField()
#     ENG_SC = models.IntegerField()
#     create_at = models.DateTimeField()
#     target = RawDirectRunData
#     last_drip = timezone.make_aware(dt.datetime(1, 1, 1, 0, 0))
#
#     @classmethod
#     def load_from_target(cls):
#         for entry in cls.target.objects.all():
#             cls.objects.create(VEH_SER_NO=entry.VEH_SER_NO,
#                                TS_LOAD=entry.TS_LOAD,
#                                SHIFT=entry.SHIFT,
#                                QA=entry.QA,
#                                PAINT=entry.PAINT,
#                                SH=entry.SH,
#                                ENG_SC=entry.ENG_SC,
#                                create_at=entry.TS_LOAD
#                                )
#
#     @classmethod
#     def _create_on_target(cls, stop):
#         relevant = cls.objects.filter(create_at__gt=cls.last_drip)
#         relevant = relevant.filter(create_at__lte=stop)
#         for entry in relevant.order_by('pk'):
#             cls.target.objects.create(VEH_SER_NO=entry.VEH_SER_NO,
#                                       TS_LOAD=entry.TS_LOAD,
#                                       SHIFT=entry.SHIFT,
#                                       QA=entry.QA,
#                                       PAINT=entry.PAINT,
#                                       SH=entry.SH,
#                                       ENG_SC=entry.ENG_SC)
#
#     @classmethod
#     def update_target(cls, *args, **kwargs):
#         cls._create_on_target(*args, **kwargs)
#         if "stop" in kwargs:
#             stop = kwargs['stop']
#         else:
#             stop = args[0]
#         cls.last_drip = stop
#
