from django.conf.urls import url
from .views import Clone, HPV
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^', Clone.as_view()),
    url(r'^planthpv/$', HPV.as_view(), name="plant_hpv"),
]
