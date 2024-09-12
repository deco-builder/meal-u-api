from django.db.models import Q
from .models import UserCart, CartIngredient, CartProduct, CartRecipe
from community.models import Ingredient, Recipe
from groceries.models import Product
from .serializers import UserCartSerializer, CartIngredientSerializer, CartProductSerializer, CartRecipeSerializer


class CartService:
    def get_cart(self, user):
        try:
            user_cart = UserCart.objects.filter(user=user).prefetch_related(
                'cartingredient_set__ingredient',
                'cartingredient_set__recipe',
                'cartproduct_set__product',
                'cartrecipe_set__recipe'
            ).first()

            if not user_cart:
                user_cart = UserCart.objects.create(user=user)

            serializer = UserCartSerializer(user_cart)
            return serializer.data
        except Exception as e:
            raise e

    def add_item(self, user, item_type, item_id, quantity=1, recipe_id=None):
        try:
            user_cart, _ = UserCart.objects.get_or_create(user=user)

            if item_type == 'ingredient':
                ingredient = Ingredient.objects.get(id=item_id)
                recipe = Recipe.objects.get(id=recipe_id) if recipe_id else None
                cart_item, created = CartIngredient.objects.get_or_create(
                    user_cart=user_cart,
                    ingredient=ingredient,
                    recipe=recipe,
                    defaults={'quantity': quantity}
                )
                if not created:
                    cart_item.quantity += quantity
                    cart_item.save()
                serializer = CartIngredientSerializer(cart_item)

            elif item_type == 'product':
                product = Product.objects.get(id=item_id)
                cart_item, created = CartProduct.objects.get_or_create(
                    user_cart=user_cart,
                    product=product,
                    defaults={'quantity': quantity}
                )
                if not created:
                    cart_item.quantity += quantity
                    cart_item.save()
                serializer = CartProductSerializer(cart_item)

            elif item_type == 'recipe':
                recipe = Recipe.objects.get(id=item_id)
                cart_item, created = CartRecipe.objects.get_or_create(
                    user_cart=user_cart,
                    recipe=recipe,
                    defaults={'quantity': quantity}
                )
                if not created:
                    cart_item.quantity += quantity
                    cart_item.save()
                serializer = CartRecipeSerializer(cart_item)

            else:
                raise ValueError("Invalid item type.")

            return serializer.data
        except Exception as e:
            raise e

    def remove_item(self, user, item_type, item_id):
        try:
            user_cart = UserCart.objects.get(user=user)

            if item_type == 'ingredient':
                CartIngredient.objects.filter(user_cart=user_cart, id=item_id).delete()
            elif item_type == 'product':
                CartProduct.objects.filter(user_cart=user_cart, id=item_id).delete()
            elif item_type == 'recipe':
                CartRecipe.objects.filter(user_cart=user_cart, id=item_id).delete()
            else:
                raise ValueError("Invalid item type.")
        except Exception as e:
            raise e

    def update_item_quantity(self, user, item_type, item_id, new_quantity):
        try:
            user_cart = UserCart.objects.get(user=user)

            if item_type == 'ingredient':
                item = CartIngredient.objects.get(user_cart=user_cart, id=item_id)
                item.quantity = new_quantity
                item.save()
                serializer = CartIngredientSerializer(item)
            elif item_type == 'product':
                item = CartProduct.objects.get(user_cart=user_cart, id=item_id)
                item.quantity = new_quantity
                item.save()
                serializer = CartProductSerializer(item)
            elif item_type == 'recipe':
                item = CartRecipe.objects.get(user_cart=user_cart, id=item_id)
                item.quantity = new_quantity
                item.save()
                serializer = CartRecipeSerializer(item)
            else:
                raise ValueError("Invalid item type.")

            return serializer.data
        except Exception as e:
            raise e