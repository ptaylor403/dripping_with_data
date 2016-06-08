from django.apps import AppConfig
from pytz import utc
# from apscheduler.schedulers.background import BackgroundScheduler
from .processor import check_server


class DataProcessorConfig(AppConfig):
    name = 'data_processor'

    """
    When django loads this will schedule an event that will check the server for new data to process every X minutes as defined in plant settings.
    """
    def ready(self):
        # scheduler = BackgroundScheduler()
        # scheduler.add_job(check_server(), 'interval', minutes=5)
        pass
