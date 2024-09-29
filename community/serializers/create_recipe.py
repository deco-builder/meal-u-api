from rest_framework import serializers
from ..models import (
    RecipeIngredient,
    RecipeNutrition,
    Recipe,
    Ingredient,
    PreparationType,
    RecipeDietaryDetail,
)
from decimal import Decimal


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["name", "product_id", "unit_id", "unit_size", "description"]

    def create(self, validated_data):
        product = validated_data.get("product_id")
        unit_id = validated_data.get("unit_id")
        unit_size = validated_data.get("unit_size")

        if product.unit_id != unit_id:
            price_per_unit = product.price_per_measurement
        else:
            price_per_unit = Decimal(unit_size) / product.measurement_size * product.price_per_measurement
        
        validated_data['price_per_unit'] = price_per_unit
        validated_data['stock'] = 100

        return super().create(validated_data)


class PreparationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreparationType
        fields = ["name", "ingredient"]


class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = "__all__"


class RecipeDietaryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeDietaryDetail
        fields = "__all__"


class RecipeNutritionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeNutrition
        fields = "__all__"
