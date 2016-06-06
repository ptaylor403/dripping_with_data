from rest_framework import serializers
from .models import HPVATM
​
​
class HPVSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    hpv_plant = serializers.IntegerField()
​
    class Meta:
        model = HPVATM
