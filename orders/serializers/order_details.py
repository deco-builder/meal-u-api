from rest_framework import serializers
from ..models import OrderProducts, OrderRecipes, OrderMealKits, Orders

class OrderProductSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderProducts
        fields = ['product', 'product_name', 'quantity', 'total']

class OrderRecipeSerializer(serializers.ModelSerializer):
    recipe_name = serializers.CharField(source='recipe.name', read_only=True)

    class Meta:
        model = OrderRecipes
        fields = ['recipe', 'recipe_name', 'quantity', 'total']

class OrderMealKitSerializer(serializers.ModelSerializer):
    mealkit_name = serializers.CharField(source='mealkit.name', read_only=True)

    class Meta:
        model = OrderMealKits
        fields = ['mealkit', 'mealkit_name', 'quantity', 'total']

class OrderDetailSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(source='orderproducts_set', many=True)
    recipes = OrderRecipeSerializer(source='orderrecipes_set', many=True)
    meal_kits = OrderMealKitSerializer(source='ordermealkits_set', many=True)

    class Meta:
        model = Orders
        fields = ['id', 'user_id', 'order_status', 'created_at', 'updated_at', 'total', 'products', 'recipes', 'meal_kits']