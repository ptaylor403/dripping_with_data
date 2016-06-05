from django.conf.urls import url
from .views import Clone

urlpatterns = [
    url(r'^', Clone.as_view()),
]