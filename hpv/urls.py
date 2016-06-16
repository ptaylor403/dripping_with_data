from django.conf.urls import url
from .views import HPV, logout_view, Detail
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/hpv/', permanent=False),
        name='redirect'),
    url(r'^hpv/$', HPV.as_view(), name="hpv"),
    url(r'^detail/', Detail.as_view()),
    url(r'^logout/$', logout_view),
]
