from django.apps import AppConfig
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler

from .processor import check_server


class DataProcessorConfig(AppConfig):
    name = 'data_processor'

    """
    When django loads this will schedule an event that checks the server for new data to process every X minutes as defined in plant settings.
    """
    def ready(self):
        from .processor import get_new_hpv_data
        # scheduler = BackgroundScheduler()
        # scheduler.add_job(get_new_hpv_data(), 'interval', minutes=5)
        pass
