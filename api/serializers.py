from rest_framework import serializers
from .models import HPVATM


class HPVSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    hpv_plant = serializers.DecimalField(decimal_places=1, max_digits=4)
    num_clocked_in = serializers.IntegerField()

    class Meta:
        model = HPVATM
