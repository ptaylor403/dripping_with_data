from django.conf.urls import url
from .views import Load, HPV

urlpatterns = [
    url(r'^load/$', Load.as_view()),
    url(r'^hpv/$', HPV.as_view())
]
