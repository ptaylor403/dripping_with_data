from django.conf.urls import url
from .views import Load, HPV, Drip, logout_view, heatmap
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/hpv/', permanent=False), name='redirect'),
    url(r'^load/$', Load.as_view()),
    url(r'^hpv/$', HPV.as_view(), name="hpv"),
    url(r'^drip/$', Drip.as_view()),
    url(r'^heatmap/', heatmap),
    url(r'^logout/$', logout_view),
]
