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
    shift = models.IntegerField()
    claims = models.IntegerField()

    CIW_d_hpv = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    CIW_d_mh = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    CIW_s_hpv = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    CIW_s_ne = models.IntegerField()
    CIW_s_mh = models.DecimalField(decimal_places=2, max_digits=6, null=True)

    FCB_d_hpv = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    FCB_d_mh = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    FCB_s_hpv = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    FCB_s_ne = models.IntegerField()
    FCB_s_mh = models.DecimalField(decimal_places=2, max_digits=6, null=True)

    PNT_d_hpv = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    PNT_d_mh = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    PNT_s_hpv = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    PNT_s_ne = models.IntegerField()
    PNT_s_mh = models.DecimalField(decimal_places=2, max_digits=6, null=True)

    PCH_d_hpv = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    PCH_d_mh = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    PCH_s_hpv = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    PCH_s_ne = models.IntegerField()
    PCH_s_mh = models.DecimalField(decimal_places=2, max_digits=6, null=True)

    FCH_d_hpv = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    FCH_d_mh = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    FCH_s_hpv = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    FCH_s_ne = models.IntegerField()
    FCH_s_mh = models.DecimalField(decimal_places=2, max_digits=6, null=True)

    DAC_d_hpv = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    DAC_d_mh = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    DAC_s_hpv = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    DAC_s_ne = models.IntegerField()
    DAC_s_mh = models.DecimalField(decimal_places=2, max_digits=6, null=True)

    MAINT_d_hpv = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    MAINT_d_mh = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    MAINT_s_hpv = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    MAINT_s_ne = models.IntegerField()
    MAINT_s_mh = models.DecimalField(decimal_places=2, max_digits=6, null=True)

    QA_d_hpv = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    QA_d_mh = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    QA_s_hpv = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    QA_s_ne = models.IntegerField()
    QA_s_mh = models.DecimalField(decimal_places=2, max_digits=6, null=True)

    MAT_d_hpv = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    MAT_d_mh = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    MAT_s_hpv = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    MAT_s_ne = models.IntegerField()
    MAT_s_mh = models.DecimalField(decimal_places=2, max_digits=6, null=True)

    OTHER_d_hpv = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    OTHER_d_mh = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    OTHER_s_hpv = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    OTHER_s_ne = models.IntegerField()
    OTHER_s_mh = models.DecimalField(decimal_places=2, max_digits=6, null=True)

    PLANT_d_hpv = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    PLANT_d_mh = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    PLANT_s_hpv = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    PLANT_s_ne = models.IntegerField()
    PLANT_s_mh = models.DecimalField(decimal_places=2, max_digits=6, null=True)



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
