from rest_framework import serializers
from ..models import Recipe, RecipeIngredient
from .recipes import RecipeIngredientSerializer


class RecipeDetailsSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
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
            "description",
            "serving_size",
            "meal_type",
            "cooking_time",
            "instructions",
            "created_at",
            "updated_at",
            "is_customized",
            "photo",
            "dietary_details",
            "ingredients",
            "total_price",
        ]

    def get_creator(self, obj):
        return f"{obj.creator.first_name} {obj.creator.last_name}"

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