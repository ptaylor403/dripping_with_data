from django.conf.urls import url
from .views import Load, Login, Logout

urlpatterns = [
    url(r'^load/$', Load.as_view()),
    url(r'^$', Login.as_view()),
    url(r'^logout/$', Logout.as_view()),
]
