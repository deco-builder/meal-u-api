from rest_framework import serializers
from ..models import DeliveryTimeSlot

class DeliveryTimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryTimeSlot
        fields = '__all__'
