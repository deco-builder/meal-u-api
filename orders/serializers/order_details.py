from rest_framework import serializers
from ..models import OrderProducts, OrderRecipes, OrderMealKits, Orders, DeliveryDetails
from community.models import RecipeIngredient, Ingredient
from user_auth.models import User
from .orders import DeliveryLocationSerializer, DeliveryTimeSlotSerializer

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.CharField(source='ingredient.name', read_only=True)
    preparation_type = serializers.CharField(source='preparation_type.name', read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient_name', 'preparation_type']

class OrderProductSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderProducts
        fields = ['product', 'product_name', 'quantity', 'total']

class OrderRecipeSerializer(serializers.ModelSerializer):
    recipe_name = serializers.CharField(source='recipe.name', read_only=True)
    ingredients = RecipeIngredientSerializer(source='recipe.recipeingredient_set', many=True, read_only=True)

    class Meta:
        model = OrderRecipes
        fields = ['recipe', 'recipe_name', 'quantity', 'total', 'ingredients']

class OrderMealKitSerializer(serializers.ModelSerializer):
    mealkit_name = serializers.CharField(source='mealkit.name', read_only=True)

    class Meta:
        model = OrderMealKits
        fields = ['mealkit', 'mealkit_name', 'quantity', 'total']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'image']

class DeliveryDetailsSerializer(serializers.ModelSerializer):
    delivery_location = DeliveryLocationSerializer(read_only=True)  
    delivery_time = DeliveryTimeSlotSerializer(read_only=True)      
    locker_number = serializers.CharField(source='locker.locker_number', read_only=True, allow_null=True)

    class Meta:
        model = DeliveryDetails
        fields = ['delivery_location', 'delivery_time', 'delivery_date', 'locker_number', 'qr_code']

class OrderDetailSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(source='orderproducts_set', many=True)
    recipes = OrderRecipeSerializer(source='orderrecipes_set', many=True)
    meal_kits = OrderMealKitSerializer(source='ordermealkits_set', many=True)
    user_id = UserSerializer(read_only=True)
    delivery_details = DeliveryDetailsSerializer(source='deliverydetails_set', many=True, read_only=True)  # Add this line

    class Meta:
        model = Orders
        fields = ['id', 'user_id', 'order_status', 'created_at', 'updated_at', 'total', 'products', 'recipes', 'meal_kits', 'delivery_details']
