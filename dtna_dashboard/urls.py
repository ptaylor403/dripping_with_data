from django.conf.urls import include, url
from django.contrib import admin
from django.apps import AppConfig
import filelock
from apscheduler.schedulers.background import BackgroundScheduler
from data_processor.processor_functions.processor_get_new_hpv import get_new_hpv_data


scheduler = BackgroundScheduler()
scheduler.add_job(get_new_hpv_data, 'interval', seconds=2)
scheduler.start()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('hpv.urls')),
    url(r'^', include('api.urls')),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^getdata/', include('get_data.urls')),
    url(r'^dripper/', include('generic_dripper.urls'))
]
