from rest_framework import serializers
from ..models import CategoryPreparationType


class CategoryPreparationTypeSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = CategoryPreparationType
        fields = ["name", "category", "additional_price"]

    def get_category(self, obj):
        return obj.category.name
