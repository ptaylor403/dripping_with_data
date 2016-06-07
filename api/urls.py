from django.conf.urls import include, url
from django.contrib import admin
from . import views


urlpatterns = [
   url(r'^api/hpv', views.HPVAPI.as_view()),
]
