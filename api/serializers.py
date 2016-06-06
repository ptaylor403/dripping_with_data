from rest_framework import serializers
from .models import HPVATM


class HPVSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    num_clocked_in = serializers.IntegerField()
    num_claims = serializers.IntegerField()
    num_claims_first = serializers.IntegerField()
    num_claims_second = serializers.IntegerField()
    num_claims_third = serializers.IntegerField()
    manhours = serializers.IntegerField()
    hpv_plant = serializers.IntegerField()

    class Meta:
        model = HPVATM
