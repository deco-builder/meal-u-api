from rest_framework import serializers
from ..models import Product, ProductDietaryDetail, DietaryDetail


class DietaryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietaryDetail
        fields = ["name"]


class ProductDietaryDetailSerializer(serializers.ModelSerializer):
    dietary_details = serializers.StringRelatedField(source="dietary_details.name")

    class Meta:
        model = ProductDietaryDetail
        fields = ["dietary_details"]


class ProductsSerializer(serializers.ModelSerializer):
    category_id = serializers.StringRelatedField()
    unit_id = serializers.StringRelatedField()
    dietary_details = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_dietary_details(self, obj):
        return obj.productdietarydetail_set.values_list(
            "dietary_details__name", flat=True
        )
