from django.shortcuts import render
from .models import HPVATM
from .serializers import HPVSerializer
from rest_framework import generics, renderers, permissions
from django.contrib.auth.mixins import LoginRequiredMixin


class HPVAPI(LoginRequiredMixin, generics.ListCreateAPIView):
    queryset = HPVATM.objects.all()
    serializer_class = HPVSerializer
    login_url = '/login/'
