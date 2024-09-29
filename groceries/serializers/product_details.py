from rest_framework import serializers
from ..models import Product, Category, DietaryDetail, ProductNutrition
from community.models import Recipe
from community.serializers.recipes import RecipesSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class DietaryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietaryDetail
        fields = ["id", "name"]


class ProductNutritionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductNutrition
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


class ProductDetailsSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    dietary_details = serializers.SerializerMethodField()
    product_nutrition = serializers.SerializerMethodField()
    unit_id = serializers.StringRelatedField()
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category",
            "unit_id",
            "unit_size",
            "price_per_unit",
            "measurement_size",
            "price_per_measurement",
            "image",
            "description",
            "stock",
            "dietary_details",
            "product_nutrition",
            "recipes",
        ]

    def get_dietary_details(self, obj):
        return obj.productdietarydetail_set.values_list("dietary_details__name", flat=True)

    def get_product_nutrition(self, obj):
        try:
            return ProductNutritionSerializer(obj.productnutrition).data
        except Exception as e:
            return None
    
    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(recipeingredient__ingredient__product_id=obj).distinct()
        return RecipesSerializer(recipes, many=True).data