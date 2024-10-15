from rest_framework import serializers
from ..models import Recipe, RecipeIngredient, Ingredient
from groceries.models import PreparationType
from user_auth.models import User


class IngredientSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    product_id = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = ["id", "name", "image", "product_id", "unit_id", "unit_size", "price_per_unit"]

    def get_image(self, obj):
        return obj.product_id.image.url if obj.product_id.image else None

    def get_product_id(self, obj):
        return obj.product_id.id


class PreparationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreparationType
        fields = "__all__"


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
    creator = serializers.SerializerMethodField()
    meal_type = serializers.CharField(source="meal_type.name", read_only=True)
    dietary_details = serializers.SerializerMethodField()
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
            "image",
            "dietary_details",
            "total_price",
        ]

    def get_creator(self, obj):
        return {
            "name": f"{obj.creator.first_name} {obj.creator.last_name}",
            "profile_picture": obj.creator.image.url if obj.creator.image else None,
<<<<<<< HEAD
            "id": obj.creator.id
=======
            "userID": obj.creator.id
>>>>>>> 1e114faeb09fe6b7b7bde7d14f60dcbeb8734e77
        }

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


class TrendingRecipesSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    meal_type = serializers.CharField(source="meal_type.name", read_only=True)
    dietary_details = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField()
    comments_count = serializers.IntegerField()

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
            "image",
            "dietary_details",
            "total_price",
            "likes_count",
            "comments_count",
        ]

    def get_creator(self, obj):
        return {
            "name": f"{obj.creator.first_name} {obj.creator.last_name}",
            "profile_picture": obj.creator.image.url if obj.creator.image else None,
            "id": obj.creator.id
        }

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


class TopCreatorSerializer(serializers.Serializer):
    id = serializers.IntegerField(source="creator__id")
    email = serializers.EmailField(source="creator__email")
    first_name = serializers.CharField(source="creator__first_name")
    last_name = serializers.CharField(source="creator__last_name")
    image = serializers.SerializerMethodField()
    recipe_count = serializers.IntegerField()

    def get_image(self, obj):
        return User.objects.get(id=obj["creator__id"]).image.url if User.objects.get(id=obj["creator__id"]).image.url else None
