from rest_framework import serializers
from ..models import UserProfile, User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['role', 'status', 'profile_pic', 'phone_number', 'created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(source='userprofile', read_only=True) 

    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'role',
            'image', 'voucher_credits', 'profile'  
        ]