from rest_framework import serializers
from .models import CartIngredient, CartProduct, CartRecipe, CartMealKit
from community.models import RecipeDietaryDetail
from community.serializers.recipes import (
    PreparationTypeSerializer,
    IngredientSerializer,
)
from groceries.serializers.products import ProductsSerializer


class CartProductSerializer(serializers.ModelSerializer):
    product = ProductsSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartProduct
        fields = ["id", "product", "quantity", "total_price"]

    def get_total_price(self, obj):
        return obj.quantity * obj.product.price_per_unit if obj.product else 0


class CartIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(source="recipe_ingredient.ingredient", read_only=True)
    preparation_type = PreparationTypeSerializer(source="recipe_ingredient.preparation_type", read_only=True)
    price = serializers.SerializerMethodField()

    class Meta:
        model = CartIngredient
        fields = ["id", "ingredient", "preparation_type", "quantity", "price"]

    def get_price(self, obj):
        ingredient_price = obj.recipe_ingredient.ingredient.price_per_unit
        preparation_price = (
            obj.recipe_ingredient.preparation_type.additional_price if obj.recipe_ingredient.preparation_type else 0
        )
        return (ingredient_price + preparation_price) * obj.quantity


class CartRecipeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="recipe.name", read_only=True)
    image = serializers.URLField(source="recipe.image.url", read_only=True)
    dietary_details = serializers.SerializerMethodField()
    ingredients = CartIngredientSerializer(many=True, read_only=True, source="cartingredient_set")
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartRecipe
        fields = ["id", "recipe", "name", "image", "quantity", "ingredients", "dietary_details", "total_price"]

    def get_dietary_details(self, obj):
        dietary_details = RecipeDietaryDetail.objects.filter(recipe=obj.recipe)
        return dietary_details.values_list("dietary_details__name", flat=True)

    def get_total_price(self, obj):
        total_price = 0
        for ingredient in obj.cartingredient_set.all():
            ingredient_price = ingredient.recipe_ingredient.ingredient.price_per_unit
            preparation_price = (
                ingredient.recipe_ingredient.preparation_type.additional_price
                if ingredient.recipe_ingredient.preparation_type
                else 0
            )
            total_price += (ingredient_price + preparation_price) * ingredient.quantity

        return total_price


class CartMealKitSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="mealkit.name", read_only=True)
    image = serializers.URLField(source="mealkit.image.url", read_only=True)
    recipes = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartMealKit
        fields = ["id", "mealkit", "name", "image", "quantity", "recipes", "total_price"]

    def get_recipes(self, obj):
        mealkit_recipes = (
            CartRecipe.objects.filter(mealkit=obj)
            .select_related("recipe")
            .prefetch_related(
                "cartingredient_set__recipe_ingredient__ingredient",
                "cartingredient_set__recipe_ingredient__preparation_type",
            )
        )
        return CartRecipeSerializer(mealkit_recipes, many=True).data

    def get_total_price(self, obj):
        recipes = self.get_recipes(obj)
        total_price = 0
        for recipe in recipes:
            total_price += recipe["total_price"]
        return total_price
