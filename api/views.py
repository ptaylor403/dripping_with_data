from django.shortcuts import render
from .models import HPVATM
from .serializers import HPVSerializer
from rest_framework import generics, renderers, permissions
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max, Min
import datetime as dt


class HPVAPI(LoginRequiredMixin, generics.ListCreateAPIView):
    queryset = HPVATM.objects.all()
    serializer_class = HPVSerializer
    login_url = '/login/'

    def get_queryset(self):
        queryset = HPVATM.objects.all()

        days = self.request.query_params.get('days', None)
        start = self.request.query_params.get('start', None)
        end = self.request.query_params.get('end', None)
        start_time = queryset.aggregate(Min('timestamp'))['timestamp__min']
        print(start_time)
        end_time = queryset.aggregate(Max('timestamp'))['timestamp__max']
        print(end_time)
        if start is not None:
            start_time = dt.datetime.fromtimestamp(int(start), dt.timezone.utc)
        if end is not None:
            end_time = dt.datetime.fromtimestamp(int(end), dt.timezone.utc)
        if days is not None:
            if start is None:
                start_time = end_time - dt.timedelta(days=int(days))
            elif end is None:
                end_time = start_time + dt.timedelta(days=int(days))
        print(start_time)
        print(end_time)
        return queryset.filter(timestamp__gte=start_time, timestamp__lte=end_time).order_by('timestamp')
