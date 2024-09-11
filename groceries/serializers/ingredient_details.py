from rest_framework import serializers
from ..models import Ingredient, Category, DietaryDetail, Nutrition


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class DietaryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietaryDetail
        fields = ["id", "name"]


class NutritionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrition
        fields = [
            "servings_per_package",
            "serving_size",
            "energy_per_serving",
            "protein_per_serving",
            "fat_total_per_serving",
            "saturated_fat_per_serving",
            "carbohydrate_per_serving",
            "sugars_per_serving",
            "dietary_fibre_per_serving",
            "sodium_per_serving",
            "energy_per_100g",
            "protein_per_100g",
            "fat_total_per_100g",
            "saturated_fat_per_100g",
            "carbohydrate_per_100g",
            "sugars_per_100g",
            "dietary_fibre_per_100g",
            "sodium_per_100g",
        ]


class IngredientDetailsSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    dietary_details = serializers.SerializerMethodField()
    nutrition = NutritionSerializer(read_only=True)
    unit_id = serializers.StringRelatedField()

    class Meta:
        model = Ingredient
        fields = [
            "id",
            "name",
            "category",
            "unit_id",
            "unit_size",
            "price_per_unit",
            "measurement_size",
            "price_per_measurement",
            "description",
            "stock",
            "dietary_details",
            "nutrition",
        ]

    def get_dietary_details(self, obj):
        return obj.ingredientdietarydetail_set.values_list("dietary_details__name", flat=True)
