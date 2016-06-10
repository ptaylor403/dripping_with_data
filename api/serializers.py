from rest_framework import serializers
from .models import HPVATM


class HPVSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    shift = serializers.IntegerField()
    claims_s = serializers.IntegerField()
    claims_d = serializers.IntegerField()

    CIW_d_hpv = serializers.DecimalField(decimal_places=1, max_digits=4)
    CIW_d_mh = serializers.DecimalField(decimal_places=2, max_digits=6)
    CIW_s_hpv = serializers.DecimalField(decimal_places=1, max_digits=4)
    CIW_s_ne = serializers.IntegerField()
    CIW_s_mh = serializers.DecimalField(decimal_places=2, max_digits=6)

    FCB_d_hpv = serializers.DecimalField(decimal_places=1, max_digits=4)
    FCB_d_mh = serializers.DecimalField(decimal_places=2, max_digits=6)
    FCB_s_hpv = serializers.DecimalField(decimal_places=1, max_digits=4)
    FCB_s_ne = serializers.IntegerField()
    FCB_s_mh = serializers.DecimalField(decimal_places=2, max_digits=6)

    PNT_d_hpv = serializers.DecimalField(decimal_places=1, max_digits=4)
    PNT_d_mh = serializers.DecimalField(decimal_places=2, max_digits=6)
    PNT_s_hpv = serializers.DecimalField(decimal_places=1, max_digits=4)
    PNT_s_ne = serializers.IntegerField()
    PNT_s_mh = serializers.DecimalField(decimal_places=2, max_digits=6)

    PCH_d_hpv = serializers.DecimalField(decimal_places=1, max_digits=4)
    PCH_d_mh = serializers.DecimalField(decimal_places=2, max_digits=6)
    PCH_s_hpv = serializers.DecimalField(decimal_places=1, max_digits=4)
    PCH_s_ne = serializers.IntegerField()
    PCH_s_mh = serializers.DecimalField(decimal_places=2, max_digits=6)

    FCH_d_hpv = serializers.DecimalField(decimal_places=1, max_digits=4)
    FCH_d_mh = serializers.DecimalField(decimal_places=2, max_digits=6)
    FCH_s_hpv = serializers.DecimalField(decimal_places=1, max_digits=4)
    FCH_s_ne = serializers.IntegerField()
    FCH_s_mh = serializers.DecimalField(decimal_places=2, max_digits=6)

    DAC_d_hpv = serializers.DecimalField(decimal_places=1, max_digits=4)
    DAC_d_mh = serializers.DecimalField(decimal_places=2, max_digits=6)
    DAC_s_hpv = serializers.DecimalField(decimal_places=1, max_digits=4)
    DAC_s_ne = serializers.IntegerField()
    DAC_s_mh = serializers.DecimalField(decimal_places=2, max_digits=6)

    MAINT_d_hpv = serializers.DecimalField(decimal_places=1, max_digits=4)
    MAINT_d_mh = serializers.DecimalField(decimal_places=2, max_digits=6)
    MAINT_s_hpv = serializers.DecimalField(decimal_places=1, max_digits=4)
    MAINT_s_ne = serializers.IntegerField()
    MAINT_s_mh = serializers.DecimalField(decimal_places=2, max_digits=6)

    QA_d_hpv = serializers.DecimalField(decimal_places=1, max_digits=4)
    QA_d_mh = serializers.DecimalField(decimal_places=2, max_digits=6)
    QA_s_hpv = serializers.DecimalField(decimal_places=1, max_digits=4)
    QA_s_ne = serializers.IntegerField()
    QA_s_mh = serializers.DecimalField(decimal_places=2, max_digits=6)

    MAT_d_hpv = serializers.DecimalField(decimal_places=1, max_digits=4)
    MAT_d_mh = serializers.DecimalField(decimal_places=2, max_digits=6)
    MAT_s_hpv = serializers.DecimalField(decimal_places=1, max_digits=4)
    MAT_s_ne = serializers.IntegerField()
    MAT_s_mh = serializers.DecimalField(decimal_places=2, max_digits=6)

    OTHER_d_hpv = serializers.DecimalField(decimal_places=1, max_digits=4)
    OTHER_d_mh = serializers.DecimalField(decimal_places=2, max_digits=6)
    OTHER_s_hpv = serializers.DecimalField(decimal_places=1, max_digits=4)
    OTHER_s_ne = serializers.IntegerField()
    OTHER_s_mh = serializers.DecimalField(decimal_places=2, max_digits=6)

    PLANT_d_hpv = serializers.DecimalField(decimal_places=1, max_digits=4)
    PLANT_d_mh = serializers.DecimalField(decimal_places=2, max_digits=6)
    PLANT_s_hpv = serializers.DecimalField(decimal_places=1, max_digits=4)
    PLANT_s_ne = serializers.IntegerField()
    PLANT_s_mh = serializers.DecimalField(decimal_places=2, max_digits=6)

    class Meta:
        model = HPVATM
