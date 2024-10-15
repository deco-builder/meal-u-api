from rest_framework import serializers
from ..models import MealKit, MealKitRecipe
from .recipes import RecipesSerializer


class MealKitsSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    dietary_details = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = MealKit
        fields = ["id", "name", "image", "creator", "created_at", "description", "dietary_details", "price"]

    def get_creator(self, obj):
        return {
            "name": f"{obj.creator.first_name} {obj.creator.last_name}",
            "profile_picture": obj.creator.image.url if obj.creator.image else None,
            "id": obj.creator.id
        }

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


class CommunityMealKitsSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    dietary_details = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField( read_only=True)  
    comments_count = serializers.IntegerField( read_only=True)
    meal_types = serializers.SerializerMethodField()  

    class Meta:
        model = MealKit
        fields = ["id", "name", "image", "creator", "created_at", "description", "dietary_details", "meal_types", "price", "likes_count", "comments_count"]

    def get_creator(self, obj):
        return {
            "name": f"{obj.creator.first_name} {obj.creator.last_name}",
            "profile_picture": obj.creator.image.url if obj.creator.image else None,
            "id": obj.creator.id
        }

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
    
    def get_meal_types(self, obj):
        meal_kit_recipes = MealKitRecipe.objects.filter(mealkit=obj)
        meal_types = set()  
        for meal_kit_recipe in meal_kit_recipes:
            meal_type = meal_kit_recipe.recipe.meal_type.name  # Assuming meal_type is a ForeignKey field in the Recipe model
            meal_types.add(meal_type)
        return list(meal_types)
