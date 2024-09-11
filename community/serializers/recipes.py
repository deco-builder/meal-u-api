from rest_framework import serializers
from ..models import Recipe, RecipeIngredient, Ingredient, PreparationType


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name", "unit_size", "price_per_unit"]


class PreparationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreparationType
        fields = ["id", "name", "additional_price"]


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)
    preparation_type = PreparationTypeSerializer(read_only=True)
    price = serializers.SerializerMethodField()

    class Meta:
        model = RecipeIngredient
        fields = ["ingredient", "preparation_type", "price"]

    def get_price(self, obj):
        ingredient_price = obj.ingredient.price_per_unit
        preparation_price = obj.preparation_type.additional_price if obj.preparation_type else 0
        return ingredient_price + preparation_price


class RecipesSerializer(serializers.ModelSerializer):
    meal_type = serializers.CharField(source="meal_type.name", read_only=True)
    dietary_details = serializers.SerializerMethodField()
    ingredients = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            "id",
            "creator",
            "name",
            "serving_size",
            "meal_type",
            "cooking_time",
            "created_at",
            "photo",
            "dietary_details",
            "ingredients",
            "total_price",
        ]

    def get_dietary_details(self, obj):
        return obj.recipedietarydetail_set.values_list("dietary_details__name", flat=True)

    def get_ingredients(self, obj):
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=obj)
        return RecipeIngredientSerializer(recipe_ingredients, many=True).data

    def get_total_price(self, obj):
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=obj)
        total_price = 0
        for recipe_ingredient in recipe_ingredients:
            ingredient_price = recipe_ingredient.ingredient.price_per_unit
            preparation_price = (
                recipe_ingredient.preparation_type.additional_price if recipe_ingredient.preparation_type else 0
            )
            total_price += ingredient_price + preparation_price
        return total_price
