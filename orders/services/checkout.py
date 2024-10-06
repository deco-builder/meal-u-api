from datetime import datetime, date
from rest_framework.exceptions import ValidationError
from orders.models import OrderProducts, OrderRecipes, OrderMealKits, DeliveryDetails, Orders
# from ..models import UserCart, UserCartProducts, UserCartRecipes, UserCartMealKits
from community.models import RecipeIngredient, MealKitRecipe
from cart.models import UserCart, CartIngredient, CartProduct, CartRecipe, CartMealKit
from cart.serializers import CartProductSerializer, CartRecipeSerializer, CartMealKitSerializer

class CheckoutService:
    @staticmethod
    def create_order(user, data):
        # Validate delivery date
        delivery_date = data.get('delivery_date')
        if isinstance(delivery_date, str):
            delivery_date = datetime.strptime(delivery_date, '%Y-%m-%d').date()

        if delivery_date < date.today():
            raise ValidationError("Delivery date must be in the future.")

        # Fetch cart items for the user
        user_cart = UserCart.objects.get(user_id=user)

        # Fetch products, recipes, and meal kits from the cart
        products_data = CartProduct.objects.filter(user_cart=user_cart)
        recipes_data = CartRecipe.objects.filter(user_cart=user_cart)
        mealkits_data = CartMealKit.objects.filter(user_cart=user_cart)

        # Create the Order
        order = Orders.objects.create(
            user_id=user,
            order_status_id=1,  # Assuming 1 is the status for 'Pending'
            total=0  # This will be calculated later
        )

        total_price = 0

        # Handle products
        for cart_product in products_data:
            product = cart_product.product
            product_total = product.price_per_unit * cart_product.quantity
            OrderProducts.objects.create(
                order=order,
                product=product,
                quantity=cart_product.quantity,
                total=product_total
            )
            total_price += product_total

        # Handle recipes with updated ingredient quantities and preparation types
        for cart_recipe in recipes_data:
            recipe = cart_recipe.recipe
            recipe_total = 0

            # Loop through the cart ingredients to calculate their total
            for cart_ingredient in cart_recipe.cartingredient_set.all():
                ingredient = cart_ingredient.recipe_ingredient.ingredient
                preparation_price = (
                    cart_ingredient.recipe_ingredient.preparation_type.additional_price
                    if cart_ingredient.recipe_ingredient.preparation_type
                    else 0
                )
                ingredient_total = (ingredient.price_per_unit + preparation_price) * cart_ingredient.quantity
                recipe_total += ingredient_total

            # Create an OrderRecipes entry
            OrderRecipes.objects.create(
                order=order,
                recipe=recipe,
                quantity=cart_recipe.quantity,
                total=recipe_total
            )
            total_price += recipe_total * cart_recipe.quantity

        # Handle meal kits
        for cart_mealkit in mealkits_data:
            mealkit = cart_mealkit.mealkit
            mealkit_total = 0

            # Calculate the total price for each recipe in the meal kit
            for cart_recipe in cart_mealkit.cartrecipe_set.all():
                recipe_total = 0
                for cart_ingredient in cart_recipe.cartingredient_set.all():
                    ingredient = cart_ingredient.recipe_ingredient.ingredient
                    preparation_price = (
                        cart_ingredient.recipe_ingredient.preparation_type.additional_price
                        if cart_ingredient.recipe_ingredient.preparation_type
                        else 0
                    )
                    ingredient_total = (ingredient.price_per_unit + preparation_price) * cart_ingredient.quantity
                    recipe_total += ingredient_total

                mealkit_total 

            # Create an OrderMealKits entry
            OrderMealKits.objects.create(
                order=order,
                mealkit=mealkit,
                quantity=cart_mealkit.quantity,
                total=mealkit_total
            )
            total_price += mealkit_total

        # Update order total
        order.total = total_price
        order.save()

        # Add DeliveryDetails
        DeliveryDetails.objects.create(
            order=order,
            delivery_location_id=data['delivery_location'],
            delivery_time_id=data['delivery_time'],
            delivery_date=delivery_date
        )

        # Clear the user's cart
        # products_data.delete()
        # recipes_data.delete()
        # mealkits_data.delete()

        return order
