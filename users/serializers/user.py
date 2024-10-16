from rest_framework import serializers
from ..models import UserProfile, User
from groceries.models import DietaryDetail

class DietaryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietaryDetail
        fields = ['id', 'name']

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = [
            'role', 'status', 'profile_pic', 'phone_number',
            'created_at', 'updated_at'
        ]

class UserSerializer(serializers.ModelSerializer):
    # profile = UserProfileSerializer(source='userprofile')
    dietary_requirements = DietaryDetailSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'role',
            'image', 'voucher_credits', 'gender', 'dietary_requirements'
        ]
        # read_only_fields = ['id', 'is_active', 'is_staff', 'role', 'voucher_credits']