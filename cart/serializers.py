from rest_framework import serializers
from .models import UserCart, CartIngredient, CartProduct, CartRecipe, CartMealKit
<<<<<<< HEAD
from community.models import MealKitRecipe
from community.serializers.recipes import RecipesSerializer, IngredientSerializer, RecipeIngredientSerializer
from community.serializers.mealkits import MealKitsSerializer
=======
from community.serializers.recipes import RecipesSerializer, RecipeIngredientSerializer
from community.serializers.mealkit_details import MealKitDetailsSerializer
>>>>>>> origin/dev
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

class CartMealKitSerializer(serializers.ModelSerializer):
<<<<<<< HEAD
    mealkit = MealKitsSerializer(read_only=True)
    recipes = serializers.SerializerMethodField()
=======
    mealkit = MealKitDetailsSerializer(read_only=True)
>>>>>>> origin/dev

    class Meta:
        model = CartMealKit
        fields = ['id', 'mealkit', 'quantity', 'recipes']

    def get_recipes(self, obj):
        recipe_mealkits = MealKitRecipe.objects.filter(mealkit=obj.mealkit)
        return RecipesSerializer([rm.recipe for rm in recipe_mealkits], many=True).data

class CartRecipeSerializer(serializers.ModelSerializer):
    recipe = RecipesSerializer(read_only=True)
    cart_ingredients = CartIngredientSerializer(many=True, read_only=True)

    class Meta:
        model = CartRecipe
        fields = ['id', 'recipe', 'quantity', 'cart_ingredients']

class UserCartSerializer(serializers.ModelSerializer):
    cart_ingredients = CartIngredientSerializer(many=True, read_only=True)
    cart_products = CartProductSerializer(many=True, read_only=True)
    cart_recipes = CartRecipeSerializer(many=True, read_only=True)
    cart_mealkits = CartMealKitSerializer(many=True, read_only=True)

    class Meta:
        model = UserCart
        fields = ['user', 'updated_at', 'cart_ingredients', 'cart_products', 'cart_recipes', 'cart_mealkits']