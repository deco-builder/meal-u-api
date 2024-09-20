from django.db.models import Q
from .models import UserCart, CartIngredient, CartProduct, CartRecipe, CartMealKit
from community.models import Ingredient, Recipe, RecipeIngredient, MealKit
from groceries.models import Product
from .serializers import UserCartSerializer, CartIngredientSerializer, CartProductSerializer, CartRecipeSerializer, CartMealKitSerializer


class CartService:
    def get_cart(self, user):
        try:
            user_cart = UserCart.objects.filter(user=user).prefetch_related(
                'cart_ingredients__recipe_ingredient__ingredient',
                'cart_ingredients__recipe_ingredient__recipe',
                'cart_products__product',
                'cart_recipes__recipe',
                'cart_mealkits__mealkit'
            ).first()

            if not user_cart:
                user_cart = UserCart.objects.create(user=user)
                user_cart.refresh_from_db()

            serializer = UserCartSerializer(user_cart)
            return serializer.data
        except Exception as e:
            raise e

    def add_item(self, user, item_type, item_id, quantity=1):
        try:
            user_cart, _ = UserCart.objects.get_or_create(user=user)

            if item_type == 'recipe_ingredient':
                recipe_id = item_id['recipe_id']
                ingredient_id = item_id['ingredient_id']
                preparation_type_id = item_id['preparation_type_id']

                recipe_ingredient = RecipeIngredient.objects.get(
                    recipe_id=recipe_id,
                    ingredient_id=ingredient_id,
                    preparation_type_id=preparation_type_id
                )
                
                cart_ingredient, created = CartIngredient.objects.get_or_create(
                    user_cart=user_cart,
                    recipe_ingredient=recipe_ingredient,
                    defaults={'quantity': quantity}
                )
                if not created:
                    cart_ingredient.quantity += quantity
                    cart_ingredient.save()

                serializer = CartIngredientSerializer(cart_ingredient)
                
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
                cart_recipe, created = CartRecipe.objects.get_or_create(
                    user_cart=user_cart,
                    recipe=recipe,
                    defaults={'quantity': quantity}
                )
                if not created:
                    cart_recipe.quantity += quantity
                    cart_recipe.save()

                serializer = CartRecipeSerializer(cart_recipe)

            elif item_type == 'mealkit':
                mealkit = MealKit.objects.get(id=item_id)
                cart_mealkit, created = CartMealKit.objects.get_or_create(
                    user_cart=user_cart,
                    mealkit=mealkit,
                    defaults={'quantity': quantity}
                )
                if not created:
                    cart_mealkit.quantity += quantity
                    cart_mealkit.save()

                serializer = CartMealKitSerializer(cart_mealkit)

            else:
                raise ValueError("Invalid item type.")

            return serializer.data
        except Exception as e:
            raise e

    def remove_item(self, user, item_type, item_id):
        try:
            user_cart = UserCart.objects.get(user=user)

            if item_type == 'recipe_ingredient':
                CartIngredient.objects.filter(user_cart=user_cart, id=item_id).delete()
            elif item_type == 'product':
                CartProduct.objects.filter(user_cart=user_cart, id=item_id).delete()
            elif item_type == 'recipe':
                CartRecipe.objects.filter(user_cart=user_cart, id=item_id).delete()
            elif item_type == 'mealkit':
                CartMealKit.objects.filter(user_cart=user_cart, id=item_id).delete()
            else:
                raise ValueError("Invalid item type.")

            # Return the updated cart data
            return self.get_cart(user)
        except UserCart.DoesNotExist:
            raise ValueError("Cart does not exist for this user.")
        except CartProduct.DoesNotExist:
            # If the CartProduct doesn't exist, we can consider it as already removed
            return self.get_cart(user)
        except Exception as e:
            raise e

    def update_item_quantity(self, user, item_type, item_id, new_quantity):
        try:
            user_cart = UserCart.objects.get(user=user)

            if item_type == 'recipe_ingredient':
                item = CartIngredient.objects.get(user_cart=user_cart, id=item_id)
            elif item_type == 'product':
                item = CartProduct.objects.get(user_cart=user_cart, id=item_id)
            elif item_type == 'recipe':
                item = CartRecipe.objects.get(user_cart=user_cart, id=item_id)
            elif item_type == 'mealkit':
                item = CartMealKit.objects.get(user_cart=user_cart, id=item_id)
            else:
                raise ValueError("Invalid item type.")

            item.quantity = new_quantity
            item.save()

            return self.get_cart(user)
        except UserCart.DoesNotExist:
            raise ValueError("Cart does not exist for this user.")
        except (CartIngredient.DoesNotExist, CartProduct.DoesNotExist, CartMealKit.DoesNotExist):
            raise ValueError(f"{item_type.capitalize()} not found in the cart.")
        except Exception as e:
            raise e