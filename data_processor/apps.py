from django.apps import AppConfig


class DataProcessorConfig(AppConfig):
    name = 'data_processor'

    def ready(self):
        pass # startup code here
