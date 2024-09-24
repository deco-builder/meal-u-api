from ..models import DeliveryDetails, DeliveryLocation, DeliveryTimeSlot
from rest_framework import serializers

class DeliveryLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryLocation
        fields = ['name', 'branch', 'address_line1', 'address_line2', 'city', 'postal_code', 'country', 'details']

class DeliveryTimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryTimeSlot
        fields = ['name', 'start_time', 'end_time', 'cut_off']

class DeliveryDetailsSerializer(serializers.ModelSerializer):
    delivery_location = DeliveryLocationSerializer()
    delivery_time = DeliveryTimeSlotSerializer()

    class Meta:
        model = DeliveryDetails
        fields = ['delivery_location', 'delivery_time', 'delivery_date']
