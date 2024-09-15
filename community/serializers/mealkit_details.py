# serializers.py

from rest_framework import serializers
from ..models import MealKit, MealKitRecipe
from .recipes import RecipesSerializer
from .recipe_details import RecipeDetailsSerializer

class MealKitDetailsSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    dietary_details = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = MealKit
        fields = ["name", "creator", "image", "created_at", "description", "dietary_details", "total_price", "recipes"]

    def get_creator(self, obj):
        return f"{obj.creator.first_name} {obj.creator.last_name}"

    def get_dietary_details(self, obj):
        return obj.mealkitdietarydetail_set.values_list("dietary_details__name", flat=True)

    def get_total_price(self, obj):
        meal_kit_recipes = MealKitRecipe.objects.filter(mealkit=obj)
        total_price = 0
        for meal_kit_recipe in meal_kit_recipes:
            recipe = meal_kit_recipe.recipe
            recipe_serializer = RecipesSerializer(recipe)
            total_price += recipe_serializer.data.get("total_price", 0) * meal_kit_recipe.quantity
        return total_price

    def get_recipes(self, obj):
        meal_kit_recipes = MealKitRecipe.objects.filter(mealkit=obj).select_related("recipe")
        recipes = [meal_kit_recipe.recipe for meal_kit_recipe in meal_kit_recipes]
        recipes_details = []
        for recipe in recipes:
            recipes_details.append(RecipeDetailsSerializer(recipe).data)
        return recipes_details
