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

    def get_queryset(self):
        startdate = dt.datetime(2016, 6, 1, 0, 1) # change date to reflect current
        enddate = startdate + dt.timedelta(days=1)
        queryset = HPVATM.objects.filter(timestamp__range=[startdate, enddate])
        return queryset
