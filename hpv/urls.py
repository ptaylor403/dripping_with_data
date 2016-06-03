from django.conf.urls import url
from .views import Load, HPV, Drip, Login, Logout

urlpatterns = [
    url(r'^load/$', Load.as_view()),
    url(r'^hpv/$', HPV.as_view()),
    url(r'^drip/$', Drip.as_view()),
    url(r'^$', Login.as_view()),
    url(r'^logout/$', Logout.as_view()),
]
