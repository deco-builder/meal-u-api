from rest_framework import serializers
from orders.models import OrderProducts, OrderRecipes, OrderMealKits

# Serializers for nested objects
class OrderProductSerializer(serializers.ModelSerializer):
    delivery_date = serializers.DateField()
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
