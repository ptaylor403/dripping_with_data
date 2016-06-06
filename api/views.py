from django.shortcuts import render
from .models import HPVATM
from .serializers import HPVSerializer
from rest_framework import generics, renderers
from rest_framework import permissions


class HPVAPI(generics.ListCreateAPIView):
    queryset = HPVATM.objects.all()
    serializer_class = HPVSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
