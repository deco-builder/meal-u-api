from rest_framework import serializers
from ..models import DietaryDetail


class DietaryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietaryDetail
        fields = "__all__"
