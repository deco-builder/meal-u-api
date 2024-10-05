from  rest_framework import serializers
from .models import UserCart, CartIngredient, CartProduct, CartRecipe, CartMealKit, Recipe, RecipeIngredient
from community.models import MealKitRecipe
from community.serializers.recipes import IngredientSerializer, RecipeIngredientSerializer
from community.serializers.mealkits import MealKitsSerializer
from community.serializers.recipes import RecipeIngredientSerializer
from community.serializers.mealkit_details import MealKitDetailsSerializer
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
    mealkit = MealKitsSerializer(read_only=True)
    recipes = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartMealKit
        fields = ['id', 'mealkit', 'quantity', 'recipes', 'total_price']

    def get_recipes(self, obj):
        recipe_mealkits = MealKitRecipe.objects.filter(mealkit=obj.mealkit)
        return RecipesSerializer([rm.recipe for rm in recipe_mealkits], many=True).data


    def get_total_price(self, obj):
        total_price = 0
        for recipe_link in MealKitRecipe.objects.filter(mealkit=obj.mealkit):
            recipe_price = RecipesSerializer(recipe_link.recipe, context={
                'quantity_multiplier': obj.quantity,
                'cart_ingredients': CartIngredient.objects.filter(
                    user_cart=obj.user_cart,
                    recipe_ingredient__recipe=recipe_link.recipe
                )
            }).data['total_price']
            total_price += recipe_price
        return total_price

class RecipesSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    meal_type = serializers.CharField(source="meal_type.name", read_only=True)
    dietary_details = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    ingredients = RecipeIngredientSerializer(source='recipeingredient_set', many=True, read_only=True)

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
            "ingredients",
            "total_price",
        ]

    def get_creator(self, obj):
        return {
            "name": f"{obj.creator.first_name} {obj.creator.last_name}",
            "profile_picture": obj.creator.image.url if obj.creator.image else None
        }

    def get_dietary_details(self, obj):
        return obj.recipedietarydetail_set.values_list("dietary_details__name", flat=True)

    def get_total_price(self, obj):
        total_price = 0
        # Ensure quantity is defined in all cases
        quantity_multiplier = self.context.get('quantity_multiplier', 1)

        # Attempt to get cart_ingredients from context
        cart_ingredients = self.context.get('cart_ingredients', [])

        for ri in obj.recipeingredient_set.all():
            # Find the corresponding CartIngredient or use a default quantity
            cart_ingredient = next((ci for ci in cart_ingredients if ci.recipe_ingredient.id == ri.id), None)
            if cart_ingredient:
                quantity = cart_ingredient.quantity
            else:
                quantity = 1  # Default quantity if not specified in the cart

            ingredient_cost = ri.ingredient.price_per_unit
            preparation_cost = ri.preparation_type.additional_price if ri.preparation_type else 0
            total_price += (ingredient_cost + preparation_cost) * quantity * quantity_multiplier

        return total_price

    # def calculate_recipe_price(self, recipe):
    #     total_price = 0
    #     recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    #     for ri in recipe_ingredients:
    #         ingredient_cost = ri.ingredient.price_per_unit
    #         prep_cost = ri.preparation_type.additional_price if ri.preparation_type else 0
    #         total_price += (ingredient_cost + prep_cost) * ri.quantity
    #     return total_price


class CartRecipeSerializer(serializers.ModelSerializer):
    recipe = RecipesSerializer(read_only=True)
    is_from_mealkit = serializers.BooleanField(read_only=True)

    class Meta:
        model = CartRecipe
        fields = ['id', 'recipe', 'quantity', 'is_from_mealkit']

    # def get_cart_ingredients(self, obj):
    #     # Filtering CartIngredient entries specific to the given recipe in the cart
    #     cart_ingredients = CartIngredient.objects.filter(
    #         user_cart=obj.user_cart,
    #         recipe_ingredient__recipe=obj.recipe
    #     )
    #     return CartIngredientSerializer(cart_ingredients, many=True).data
class UserCartSerializer(serializers.ModelSerializer):
    cart_products = CartProductSerializer(many=True, read_only=True)
    cart_recipes = serializers.SerializerMethodField()
    cart_mealkits = CartMealKitSerializer(many=True, read_only=True)
    total_quantity = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = UserCart
        fields = ['user', 'cart_products', 'cart_recipes', 'cart_mealkits', 'total_quantity', 'total_price']

    def get_cart_recipes(self, obj):
        # Fetch only those recipes that were explicitly added as standalone (not part of a meal kit)
        cart_recipes = CartRecipe.objects.filter(
            user_cart=obj,
            is_from_mealkit=False
        )
        return CartRecipeSerializer(cart_recipes, many=True, context=self.context).data

    def get_total_quantity(self, obj):
        # Total quantity of meal kits
        total_mealkits = sum([
            mealkit.quantity for mealkit in obj.cart_mealkits.all()
        ])

        # Total quantity of standalone recipes (not from meal kits)
        total_recipes = sum([
            recipe.quantity for recipe in CartRecipe.objects.filter(
                user_cart=obj,
                is_from_mealkit=False
            )
        ])

        # Total quantity of products
        total_products = sum([
            product.quantity for product in obj.cart_products.all()
        ])

        # Calculate the total distinct counts
        total_quantity = total_mealkits + total_recipes + total_products
        return total_quantity

    def get_total_price(self, obj):
        total_price = 0
        # Sum the total price of products
        for product in obj.cart_products.all():
            total_price += product.product.price_per_unit * product.quantity
        
        # Sum the total price of cart recipes using the RecipesSerializer to calculate recipe prices
        for cart_recipe in obj.cart_recipes.all():
            recipe_serializer = RecipesSerializer(cart_recipe.recipe, context={'request': self.context.get('request')})
            total_price += recipe_serializer.data['total_price'] * cart_recipe.quantity
        
        # Sum the total price of meal kits
        for cart_mealkit in obj.cart_mealkits.all():
            meal_kit_serializer = CartMealKitSerializer(cart_mealkit, context={'request': self.context.get('request')})
            total_price += meal_kit_serializer.data['total_price']
        
        return total_price