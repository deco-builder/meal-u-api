from django.db import models
from .models import UserCart, CartIngredient, CartProduct, CartRecipe, CartMealKit
from community.models import Ingredient, Recipe, RecipeIngredient, MealKit, MealKitRecipe
from groceries.models import Product
from .serializers import UserCartSerializer, CartIngredientSerializer, CartProductSerializer, CartRecipeSerializer, CartMealKitSerializer, MealKitsSerializer, RecipesSerializer
class CartService:

    # def get_total_quantity(self, user_cart):
    #     total = 0
    #     total += CartProduct.objects.filter(user_cart=user_cart).aggregate(total=models.Sum('quantity'))['total'] or 0
    #     total += CartRecipe.objects.filter(user_cart=user_cart).aggregate(total=models.Sum('quantity'))['total'] or 0
    #     total += CartMealKit.objects.filter(user_cart=user_cart).aggregate(total=models.Sum('quantity'))['total'] or 0
    #     # Note: We're not including CartIngredient in the total quantity as per your requirements
    #     return total

    # def get_total_price(self, user_cart):
    #     total_price = 0

    #     # Calculate price for products
    #     for cart_product in CartProduct.objects.filter(user_cart=user_cart).select_related('product'):
    #         total_price += cart_product.product.price_per_unit * cart_product.quantity

    #     # Get all meal kit recipes to exclude them from individual recipe pricing
    #     mealkit_recipe_ids = MealKitRecipe.objects.filter(
    #         mealkit__cartmealkit__user_cart=user_cart
    #     ).values_list('recipe_id', flat=True)

    #     # Calculate price for recipes that are not part of meal kits
    #     for cart_recipe in CartRecipe.objects.filter(user_cart=user_cart).select_related('recipe'):
    #         if cart_recipe.recipe.id not in mealkit_recipe_ids:
    #             recipe_serializer = RecipesSerializer(cart_recipe.recipe)
    #             recipe_price = recipe_serializer.data.get('total_price', 0)
    #             total_price += recipe_price * cart_recipe.quantity

    #     # Calculate price for meal kits using the serializer
    #     for cart_mealkit in CartMealKit.objects.filter(user_cart=user_cart).select_related('mealkit'):
    #         mealkit_serializer = MealKitsSerializer(cart_mealkit.mealkit)
    #         mealkit_price = mealkit_serializer.data.get('price', 0)
    #         total_price += mealkit_price * cart_mealkit.quantity

    #     return total_price

    def get_cart(self, user):
        try:
            user_cart = UserCart.objects.filter(user=user).prefetch_related(
                'cart_ingredients__recipe_ingredient__ingredient',
                'cart_ingredients__recipe_ingredient__recipe',
                'cart_ingredients__recipe_ingredient__preparation_type',
                'cart_products__product',
                'cart_recipes__recipe',
                'cart_mealkits__mealkit'
            ).first()

            if not user_cart:
                user_cart = UserCart.objects.create(user=user)
                user_cart.refresh_from_db()

            serializer = UserCartSerializer(user_cart)
            data = serializer.data

            # Get all meal kit recipes to mark recipes in the cart
            mealkit_recipe_ids = MealKitRecipe.objects.filter(
                mealkit__cartmealkit__user_cart=user_cart
            ).values_list('recipe_id', flat=True)

            # Mark recipes that are part of meal kits
            for recipe in data['cart_recipes']:
                recipe['is_from_mealkit'] = recipe['recipe']['id'] in mealkit_recipe_ids

            # data['total_quantity'] = self.get_total_quantity(user_cart)
            # data['total_price'] = self.get_total_price(user_cart)
            return data
        except Exception as e:
            raise e
            
    def add_item(self, user, item_type, item_data, quantity=1):
        user_cart, _ = UserCart.objects.get_or_create(user=user)
        
        if item_type == 'recipe':
            meal_kit_recipe_id = item_data.get('meal_kit_recipe_id')  # Expecting this to be passed when adding from a meal kit
            return self._add_recipe(user_cart, item_data, quantity, from_mealkit=True, meal_kit_recipe_id=meal_kit_recipe_id)
        elif item_type == 'product':
            return self._add_product(user_cart, item_data, quantity)
        elif item_type == 'mealkit':
            if not isinstance(item_data, dict) or 'mealkit_id' not in item_data:
                raise ValueError("Invalid mealkit data format. Expected a dictionary with 'mealkit_id'.")
            return self._add_mealkit(user_cart, item_data, quantity)
        else:
            raise ValueError(f"Invalid item type: {item_type}")

    def _add_recipe(self, user_cart, item_data, quantity, from_mealkit=False, meal_kit_recipe_id=None):
        recipe_id = item_data.get('recipe_id')
        recipe = Recipe.objects.get(id=recipe_id)
        meal_kit_recipe = MealKitRecipe.objects.get(id=meal_kit_recipe_id) if meal_kit_recipe_id else None

        cart_recipe, created = CartRecipe.objects.get_or_create(
            user_cart=user_cart,
            recipe=recipe,
            meal_kit_recipe=meal_kit_recipe,
            defaults={'quantity': quantity, 'is_from_mealkit': from_mealkit}
        )
        if not created:
            cart_recipe.is_from_mealkit = from_mealkit  
            cart_recipe.quantity += quantity
            cart_recipe.save()

        # Update or create cart ingredients
        for ri_data in item_data.get('recipe_ingredients', []):
            ingredient_id = ri_data['ingredient_id']
            preparation_type_id = ri_data.get('preparation_type_id', None)
            ingredient_quantity = ri_data['quantity'] * quantity

            recipe_ingredient = RecipeIngredient.objects.get(
                recipe_id=recipe_id, 
                ingredient_id=ingredient_id, 
                preparation_type_id=preparation_type_id
            )
            cart_ingredient, ci_created = CartIngredient.objects.update_or_create(
                user_cart=user_cart,
                recipe_ingredient=recipe_ingredient,
                cart_recipe=cart_recipe,  # Link to the specific CartRecipe
                defaults={'quantity': ingredient_quantity}
            )
            if not ci_created:
                cart_ingredient.quantity += ingredient_quantity
                cart_ingredient.save()

        return CartRecipeSerializer(cart_recipe).data

    def _add_product(self, user_cart, item_data, quantity):
        product = Product.objects.get(id=item_data)
        cart_item, created = CartProduct.objects.get_or_create(
            user_cart=user_cart,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        serializer = CartProductSerializer(cart_item)
        return serializer.data

    def _add_mealkit(self, user_cart, item_data, quantity):
        mealkit_id = item_data.get('mealkit_id')
        mealkit = MealKit.objects.get(id=mealkit_id)

        cart_mealkit, created = CartMealKit.objects.get_or_create(
            user_cart=user_cart,
            mealkit=mealkit,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_mealkit.quantity += quantity
            cart_mealkit.save()

        # Process each recipe specified in the request for the meal kit
        recipes_data = item_data.get('recipes', [])
        for recipe_data in recipes_data:
            recipe_id = recipe_data.get('recipe_id')
            # Fetch the MealKitRecipe that matches both the meal kit and the recipe
            meal_kit_recipe = MealKitRecipe.objects.get(mealkit_id=mealkit_id, recipe_id=recipe_id)

            self._add_recipe(
                user_cart,
                recipe_data,
                recipe_data.get('quantity', 1) * quantity,
                from_mealkit=True,
                meal_kit_recipe_id=meal_kit_recipe.id  # Passing the correct MealKitRecipe ID
            )

        return CartMealKitSerializer(cart_mealkit).data

    def remove_item(self, user, item_type, item_id):
        try:
            user_cart = UserCart.objects.get(user=user)
            
            if item_type == 'recipe_ingredient':
                CartIngredient.objects.filter(user_cart=user_cart, id=item_id).delete()
            
            elif item_type == 'product':
                CartProduct.objects.filter(user_cart=user_cart, id=item_id).delete()
            
            elif item_type == 'recipe':
                cart_recipe = CartRecipe.objects.filter(user_cart=user_cart, id=item_id).first()
                if cart_recipe:
                    try:
                        # Delete associated cart ingredients
                        CartIngredient.objects.filter(
                            user_cart=user_cart,
                            recipe_ingredient__recipe=cart_recipe.recipe
                        ).delete()

                        # Delete the cart recipe
                        cart_recipe.delete()
                    except Exception as delete_error:
                        raise delete_error
                else:
                    raise CartRecipe.DoesNotExist(f"No CartRecipe found for id: {item_id}")
            
            elif item_type == 'mealkit':
                cart_mealkit = CartMealKit.objects.filter(user_cart=user_cart, id=item_id).first()
                if cart_mealkit:
                    mealkit = cart_mealkit.mealkit

                    mealkit_recipes = MealKitRecipe.objects.filter(mealkit=mealkit)
                    for mealkit_recipe in mealkit_recipes:
                        # Delete associated cart ingredients for each recipe in the meal kit
                        CartIngredient.objects.filter(
                            user_cart=user_cart,
                            recipe_ingredient__recipe=mealkit_recipe.recipe
                        ).delete()
                        
                        # Delete the cart recipe
                        CartRecipe.objects.filter(
                            user_cart=user_cart,
                            recipe=mealkit_recipe.recipe
                        ).delete()

                    cart_mealkit.delete()
                else:
                    raise CartMealKit.DoesNotExist(f"No CartMealKit found for id: {item_id}")
            
            else:
                raise ValueError("Invalid item type.")

            # Return the updated cart data
            return self.get_cart(user)
        
        except UserCart.DoesNotExist:
            raise ValueError("Cart does not exist for this user.")
        except (CartIngredient.DoesNotExist, CartProduct.DoesNotExist, CartRecipe.DoesNotExist, CartMealKit.DoesNotExist) as e:
            # If the item doesn't exist, we can consider it as already removed
            return self.get_cart(user)
        except Exception as e:
            raise e

    def update_item_quantity(self, user, item_type, item_id, new_quantity):
        try:
            user_cart = UserCart.objects.get(user=user)

            if item_type == 'recipe_ingredient':
                item = CartIngredient.objects.get(user_cart=user_cart, id=item_id)
                item.quantity = new_quantity
                item.save()

            elif item_type == 'product':
                cart_product = CartProduct.objects.get(user_cart=user_cart, id=item_id)
                cart_product.quantity = new_quantity
                cart_product.save()

            elif item_type == 'recipe':
                cart_recipe = CartRecipe.objects.get(user_cart=user_cart, id=item_id)
                cart_recipe.quantity = new_quantity
                cart_recipe.save()

                # Update associated CartIngredient quantities
                cart_ingredients = CartIngredient.objects.filter(
                    user_cart=user_cart,
                    recipe_ingredient__recipe=cart_recipe.recipe
                )
                for cart_ingredient in cart_ingredients:
                    cart_ingredient.quantity = new_quantity
                    cart_ingredient.save()
                        
            elif item_type == 'mealkit':
                cart_mealkit = CartMealKit.objects.get(user_cart=user_cart, id=item_id)
                cart_mealkit.quantity = new_quantity
                cart_mealkit.save()
                
                mealkit_recipes = MealKitRecipe.objects.filter(mealkit=cart_mealkit.mealkit)
                for mealkit_recipe in mealkit_recipes:
                    cart_recipe, _ = CartRecipe.objects.get_or_create(
                        user_cart=user_cart,
                        recipe=mealkit_recipe.recipe,
                        defaults={'quantity': mealkit_recipe.quantity * new_quantity}
                    )
                    if not _:
                        cart_recipe.quantity = mealkit_recipe.quantity * new_quantity
                        cart_recipe.save()

            else:
                raise ValueError(f"Invalid item_type: {item_type}")

            return self.get_cart(user)
        except UserCart.DoesNotExist:
            raise ValueError("Cart does not exist for this user.")
        except (CartIngredient.DoesNotExist, CartProduct.DoesNotExist, CartMealKit.DoesNotExist, CartRecipe.DoesNotExist):
            raise ValueError(f"{item_type.capitalize()} with id {item_id} not found in the cart.")
        except Exception as e:
            raise e