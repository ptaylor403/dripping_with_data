from django.shortcuts import render
from .models import HPVATM
from .serializers import HPVSerializer
from rest_framework import generics, renderers, permissions
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime as dt


class HPVAPI(LoginRequiredMixin, generics.ListCreateAPIView):
    queryset = HPVATM.objects.all()
    serializer_class = HPVSerializer
    login_url = '/login/'


    # def get_queryset(self):
    #     queryset = HPVATM.objects.all()
    #     day = self.request.query_params.get("day", None)
    #     week = self.request.query_params.get("startdate", "enddate")
    #     # day = dt.datetime(2016, 6, 1, 0, 1) # change date to reflect current date
    #     # enddate = startdate + dt.timedelta(days=7)
    #     if day is not None:
    #         day = int(day)
    #         startdate = dt.datetime(2016, 6, 1, day, 1)
    #         queryset = queryset.filter(timestamp__gte=startdate, timestamp__lt=startdate + dt.timedelta(days=1))
    #     elif week is not None:
    #         week = int(week)
    #         startdate = dt.datetime(2016, 6, 1, week, 1)
    #         enddate = startdate + dt.timedelta(days=7)
    #         queryset = self.queryset.filter(timestamp__range=[startdate, enddate])
    #     return queryset

    def get_queryset(self):
        queryset = HPVATM.objects.all()
        date = self.request.query_params.get("date", None)
        if date is not None:
            date = int(date)
            date = dt.datetime(2016, 6, date, 0, 1)
            queryset = queryset.filter(timestamp__gte=date, timestamp__lt=date + dt.timedelta(days=1))
        return queryset
    # def get_queryset(self):
    #     startdate = dt.datetime(2016, 6, 1, 0, 1) # change date to reflect current date
    #     enddate = startdate + dt.timedelta(days=7)
    #     queryset = self.queryset.filter(timestamp__range=[startdate, enddate])
    #     return queryset
