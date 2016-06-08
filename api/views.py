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
        queryset = HPVATM.objects.all()
        date = self.request.query_params.get("date", None)
        if date is not None:
            date = int(date)
            date = dt.datetime(2016, 6, date, 0, 1)
            queryset = queryset.filter(timestamp__gte=date, timestamp__lt=date + dt.timedelta(days=1))

        return queryset
