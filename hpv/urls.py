from django.conf.urls import url
from .views import Load

urlpatterns = [
    url(r'^load/$', Load.as_view())
]
