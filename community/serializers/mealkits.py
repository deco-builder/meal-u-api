from rest_framework import serializers
from ..models import MealKit, MealKitRecipe, MealkitDietaryDetail
from .recipes import RecipesSerializer


class MealKitDietaryDetailSerializer(serializers.ModelSerializer):
    dietary_details = serializers.StringRelatedField()

    class Meta:
        model = MealkitDietaryDetail
        fields = ["dietary_details"]


class MealKitsSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    dietary_details = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = MealKit
        fields = ["name", "creator", "created_at", "description", "dietary_details", "price"]

    def get_creator(self, obj):
        return f"{obj.creator.first_name} {obj.creator.last_name}"

    def get_dietary_details(self, obj):
        return obj.mealkitdietarydetail_set.values_list("dietary_details__name", flat=True)

    def get_price(self, obj):
        meal_kit_recipes = MealKitRecipe.objects.filter(mealkit=obj)
        total_price = 0
        for meal_kit_recipe in meal_kit_recipes:
            recipe = meal_kit_recipe.recipe
            recipe_serializer = RecipesSerializer(recipe)
            total_price += recipe_serializer.data.get("total_price", 0) * meal_kit_recipe.quantity
        return total_price
