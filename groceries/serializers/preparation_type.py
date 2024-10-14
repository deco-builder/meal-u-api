from rest_framework import serializers
from ..models import PreparationType


class CategoryPreparationTypeSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = PreparationType
        fields = ["id", "name", "category", "additional_price"]

    def get_category(self, obj):
        return obj.category.name
