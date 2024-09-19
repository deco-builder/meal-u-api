from rest_framework import serializers
from .models import UserCart, CartIngredient, CartProduct, CartRecipe
from community.serializers.recipes import RecipesSerializer, IngredientSerializer, RecipeIngredientSerializer, MealKitsSerializer
from groceries.serializers.products import ProductsSerializer

class CartIngredientSerializer(serializers.ModelSerializer):
    recipe_ingredient = RecipeIngredientSerializer(read_only=True)

    class Meta:
        model = CartIngredient
        fields = ['id', 'recipe_ingredient', 'quantity']

class CartProductSerializer(serializers.ModelSerializer):
    product = ProductsSerializer(read_only=True)

    class Meta:
        model = CartProduct
        fields = ['id', 'product', 'quantity']

class CartRecipeSerializer(serializers.ModelSerializer):
    recipe = RecipesSerializer(read_only=True)

    class Meta:
        model = CartRecipe
        fields = ['id', 'recipe', 'quantity']

class CartMealKitSerializer(serializers.ModelSerializer):
    mealkit = MealKitSerializer(read_only=True)

    class Meta:
        model = CartMealKit
        fields = ['id', 'mealkit', 'quantity']

class UserCartSerializer(serializers.ModelSerializer):
    cart_ingredients = CartIngredientSerializer(many=True, read_only=True)
    cart_products = CartProductSerializer(many=True, read_only=True)
    cart_recipes = CartRecipeSerializer(many=True, read_only=True)
    cart_mealkits = CartMealKitSerializer(many=True, read_only=True)

    class Meta:
        model = UserCart
        fields = ['user', 'updated_at', 'cart_ingredients', 'cart_products', 'cart_recipes', 'cart_mealkits']