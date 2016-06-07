from .models import RawClockDataDripper, RawDirectRunDataDripper
from .models import RawCrysDataDripper, RawPlantActivityDripper, CombinedDripper


class MasterDripper:
    instance = None

    def __init__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = CombinedDripper(*args, **kwargs)
        else:
            raise AttributeError("A dripper is already defined")


    def __getattr__(self, name):
        return getattr(self.instance, name)
