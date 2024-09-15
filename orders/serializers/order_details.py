from rest_framework import serializers
from ..models import OrderProducts, OrderRecipes, OrderMealKits, Orders

class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProducts
        fields = ['product', 'quantity', 'total']

class OrderRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRecipes
        fields = ['recipe', 'quantity', 'total']

class OrderMealKitSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderMealKits
        fields = ['mealkit', 'quantity', 'total']

class OrderDetailSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(source='orderproducts_set', many=True)
    recipes = OrderRecipeSerializer(source='orderrecipes_set', many=True)
    meal_kits = OrderMealKitSerializer(source='ordermealkits_set', many=True)

    class Meta:
        model = Orders
        fields = ['id', 'user_id', 'order_status', 'created_at', 'updated_at', 'total', 'products', 'recipes', 'meal_kits']
