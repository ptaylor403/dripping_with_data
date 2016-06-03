from django.conf.urls import url
from .views import Clone

urlpatterns = [
    url(r'^clone/$', Clone.as_view()),
]