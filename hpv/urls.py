from django.conf.urls import url
from .views import Load, Drip

urlpatterns = [
    url(r'^load/$', Load.as_view()),
    url(r'^drip/$', Drip.as_view())
]
