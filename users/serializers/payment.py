from rest_framework import serializers
from ..models import UserPaymentMethod
from datetime import date

class UserPaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPaymentMethod
        fields = ['user', 'method', 'token', 'last_four_digits', 'expiration_date']

    def validate_token(self, value):
        """
        Custom validation for the token field.
        """
        if not value.isalnum() or len(value) != 16:
            raise serializers.ValidationError("Token must be 16 alphanumeric characters long.")
        return value

    def validate_expiration_date(self, value):
        """
        Custom validation for the expiration_date field.
        """
        if value <= date.today():
            raise serializers.ValidationError("Expiration date must be in the future.")
        return value

    def validate(self, data):
        """
        Custom validation logic to ensure that all fields are correctly validated.
        """
        # Validate last_four_digits
        last_four_digits = data.get('last_four_digits')
        if len(last_four_digits) != 4 or not last_four_digits.isdigit():
            raise serializers.ValidationError("Last four digits must be exactly 4 digits long.")
        
        return data
