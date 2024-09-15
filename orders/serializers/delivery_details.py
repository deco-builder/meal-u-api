from rest_framework import serializers
from orders.models import DeliveryDetails
from datetime import date

class DeliveryDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryDetails
        fields = ['order', 'user_delivery_location', 'delivery_time', 'delivery_date']

    def validate_delivery_date(self, value):
        """
        Ensure the delivery date is not in the past.
        """
        if value < date.today():
            raise serializers.ValidationError("Delivery date must be in the future.")
        return value

    def validate(self, data):
        """
        Custom validation logic if needed.
        """
        return data
