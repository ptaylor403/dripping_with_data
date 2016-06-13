from django.apps import AppConfig
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
import filelock


class DataProcessorConfig(AppConfig):
    name = 'data_processor'

    """
    When django loads this will schedule an event that checks the server for new data to process every X minutes as defined in plant settings.
    """
    def ready(self):
        from .processor import get_new_hpv_data
        print("-" * 50)
        print('Entering get_new_hpv_data')
        # get_new_hpv_data()
        lock = filelock.FileLock('locker.txt')
        lock.timeout = 1
        try:
            lock.acquire()
        except:
            return
        scheduler = BackgroundScheduler()
        scheduler.add_job(get_new_hpv_data, 'interval', seconds=15)
        scheduler.start()
