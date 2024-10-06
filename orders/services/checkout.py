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
        delivery_date = data.get('delivery_date')
        if isinstance(delivery_date, str):
            delivery_date = datetime.strptime(delivery_date, '%Y-%m-%d').date()

        if delivery_date < date.today():
            raise ValidationError("Delivery date must be in the future.")

        user_cart = UserCart.objects.get(user_id=user)

        products_data = CartProduct.objects.filter(user_cart=user_cart).all()
        recipes_data = CartRecipe.objects.filter(user_cart=user_cart, mealkit__isnull=True).select_related("recipe").prefetch_related(
                    "cartingredient_set__recipe_ingredient__ingredient",
                    "cartingredient_set__recipe_ingredient__preparation_type",
                )
        mealkits_data = CartMealKit.objects.filter(user_cart=user_cart).select_related("mealkit").prefetch_related(
                    "cartrecipe_set__cartingredient_set__recipe_ingredient__ingredient",
                    "cartrecipe_set__cartingredient_set__recipe_ingredient__preparation_type",
                )
            

        product_serializer = CartProductSerializer(products_data, many=True)
        recipe_serializer = CartRecipeSerializer(recipes_data, many=True)
        mealkit_serializer = CartMealKitSerializer(mealkits_data, many=True)

        order = Orders.objects.create(
            user_id=user,
            order_status_id=1,  
            total=0  
        )

        total_price = 0
        for product in product_serializer.data:
                total_price += product["total_price"]
        for recipe in recipe_serializer.data:
                total_price += recipe["total_price"]
        for mealkit in mealkit_serializer.data:
                total_price += mealkit["total_price"]

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

        # Handle recipes with updated ingredient quantities and preparation types
        for cart_recipe in recipes_data:
            recipe = cart_recipe.recipe
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

            OrderRecipes.objects.create(
                order=order,
                recipe=recipe,
                quantity=cart_recipe.quantity,
                total=recipe_total
            )

        # Handle meal kits
        for cart_mealkit in mealkits_data:
            mealkit = cart_mealkit.mealkit
            mealkit_total = 0

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

                mealkit_total += recipe_total 

            # Create an OrderMealKits entry
            OrderMealKits.objects.create(
                order=order,
                mealkit=mealkit,
                quantity=cart_mealkit.quantity,
                total=mealkit_total
            )

        order.total = total_price
        order.save()

        DeliveryDetails.objects.create(
            order=order,
            delivery_location_id=data['delivery_location'],
            delivery_time_id=data['delivery_time'],
            delivery_date=delivery_date
        )

        products_data.delete()
        recipes_data.delete()
        mealkits_data.delete()

        return order
