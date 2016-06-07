from django.db import models

# Create your models here.
class HPVATM(models.Model):
    """
    Keeps track of all data related to HPV (Man Hours per Vehicle) for graphing and historical viewing. All values are ATM (At This Moment) referring to the timestamp.

    :param timestamp: When processed data was added
    :param num_clocked_in: Currently working employees
    :param num_claims_to_time: Number of trucks completed so far that day
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    # num_clocked_in = models.IntegerField()
    # num_claims = models.IntegerField()
    # num_claims_first = models.IntegerField(null=True)
    # num_claims_second = models.IntegerField(null=True)
    # num_claims_third = models.IntegerField(null=True)
    # manhours = models.IntegerField(null=True)
    hpv_plant = models.DecimalField(decimal_places=1, max_digits=4, null=True)


### To Add
# calculated tables hpv atm
# attendance table atm
# api call to serve hpv y and time as x
