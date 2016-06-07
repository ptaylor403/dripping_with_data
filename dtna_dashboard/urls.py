from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('hpv.urls')),
    url(r'^', include('api.urls')),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^getdata/', include('get_data.urls')),
    url(r'^dripper/', include('generic_dripper.urls'))
]
