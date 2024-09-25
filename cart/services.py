from django.db.models import Q
from .models import UserCart, CartIngredient, CartProduct, CartRecipe, CartMealKit
from community.models import Ingredient, Recipe, RecipeIngredient, MealKit, MealKitRecipe
from groceries.models import Product
from .serializers import UserCartSerializer, CartIngredientSerializer, CartProductSerializer, CartRecipeSerializer, CartMealKitSerializer

class CartService:
    
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
            return serializer.data
        except Exception as e:
            raise e
            
    def add_item(self, user, item_type, item_data, quantity=1):
        try:
            user_cart, _ = UserCart.objects.get_or_create(user=user)
            
            if item_type == 'recipe':
                return self._add_recipe(user_cart, item_data, quantity)
            elif item_type == 'product':
                return self._add_product(user_cart, item_data, quantity)
            elif item_type == 'mealkit':
                if not isinstance(item_data, dict) or 'mealkit_id' not in item_data:
                    raise ValueError("Invalid mealkit data format. Expected a dictionary with 'mealkit_id'.")
                return self._add_mealkit(user_cart, item_data, quantity)
            else:
                raise ValueError(f"Invalid item type: {item_type}")

        except Exception as e:
            raise e

    def _add_recipe(self, user_cart, item_data, quantity):
        recipe_id = item_data.get('recipe_id')
        recipe_ingredients = item_data.get('recipe_ingredients', [])

        if not recipe_id:
            raise ValueError("Recipe ID is required.")

        recipe = Recipe.objects.get(id=recipe_id)
        cart_recipe, created = CartRecipe.objects.get_or_create(
            user_cart=user_cart,
            recipe=recipe,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_recipe.quantity += quantity
            cart_recipe.save()

        for ri_data in recipe_ingredients:
            recipe_ingredient = RecipeIngredient.objects.get(
                recipe_id=recipe_id,
                ingredient_id=ri_data['ingredient_id'],
                preparation_type_id=ri_data.get('preparation_type_id')
            )
            cart_ingredient, created = CartIngredient.objects.get_or_create(
                user_cart=user_cart,
                recipe_ingredient=recipe_ingredient,
                defaults={'quantity': ri_data.get('quantity', 1) * quantity}
            )
            if not created:
                cart_ingredient.quantity += ri_data.get('quantity', 1) * quantity
                cart_ingredient.save()

        serializer = CartRecipeSerializer(cart_recipe)
        return serializer.data

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
        recipes = item_data.get('recipes', [])

        if not mealkit_id:
            raise ValueError("MealKit ID is required.")

        try:
            mealkit = MealKit.objects.get(id=mealkit_id)
        except MealKit.DoesNotExist:
            raise ValueError(f"MealKit with ID {mealkit_id} does not exist.")

        cart_mealkit, created = CartMealKit.objects.get_or_create(
            user_cart=user_cart,
            mealkit=mealkit,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_mealkit.quantity += quantity
            cart_mealkit.save()

        for recipe_data in recipes:
            recipe_id = recipe_data.get('recipe_id')
            recipe_quantity = recipe_data.get('quantity', 1)
            recipe_ingredients = recipe_data.get('recipe_ingredients', [])

            recipe = Recipe.objects.get(id=recipe_id)
            cart_recipe, created = CartRecipe.objects.get_or_create(
                user_cart=user_cart,
                recipe=recipe,
                defaults={'quantity': recipe_quantity * quantity}
            )
            if not created:
                cart_recipe.quantity += recipe_quantity * quantity
                cart_recipe.save()

            for ri_data in recipe_ingredients:
                recipe_ingredient = RecipeIngredient.objects.get(
                    recipe_id=recipe_id,
                    ingredient_id=ri_data['ingredient_id'],
                    preparation_type_id=ri_data.get('preparation_type_id')
                )
                cart_ingredient, created = CartIngredient.objects.get_or_create(
                    user_cart=user_cart,
                    recipe_ingredient=recipe_ingredient,
                    defaults={'quantity': ri_data.get('quantity', 1) * recipe_quantity * quantity}
                )
                if not created:
                    cart_ingredient.quantity += ri_data.get('quantity', 1) * recipe_quantity * quantity
                    cart_ingredient.save()

        serializer = CartMealKitSerializer(cart_mealkit)
        return serializer.data

    def remove_item(self, user, item_type, item_id):
        try:
            user_cart = UserCart.objects.get(user=user)

            if item_type == 'recipe_ingredient':
                CartIngredient.objects.filter(user_cart=user_cart, id=item_id).delete()
            elif item_type == 'product':
                CartProduct.objects.filter(user_cart=user_cart, id=item_id).delete()

            elif item_type == 'recipe':
                cart_recipe = CartRecipe.objects.filter(user_cart=user_cart, id=item_id).first()
                # print(f"Attempting to delete CartRecipe with id: {item_id}")
                if cart_recipe:
                    # print(f"CartRecipe found: {cart_recipe.id}")
                    try:
                        # Delete associated ingredients
                        deleted_ingredients = CartIngredient.objects.filter(
                            user_cart=user_cart,
                            recipe_ingredient__recipe=cart_recipe.recipe
                        ).delete()
                        # print(f"Deleted associated ingredients: {deleted_ingredients}")

                        # Delete the cart recipe
                        deleted_recipe = cart_recipe.delete()
                        # print(f"Deleted CartRecipe: {deleted_recipe}")
                    except Exception as delete_error:
                        # print(f"Error during deletion: {str(delete_error)}")
                        raise delete_error
                else:
                    # print(f"No CartRecipe found for id: {item_id} in user_cart: {user_cart.id}")
                    all_cart_recipes = CartRecipe.objects.filter(user_cart=user_cart)
                    # print(f"All CartRecipes for this user: {list(all_cart_recipes.values())}")

            elif item_type == 'mealkit':
                cart_mealkit = CartMealKit.objects.get(user_cart=user_cart, id=item_id)
                mealkit = cart_mealkit.mealkit
                
                mealkit_recipes = MealKitRecipe.objects.filter(mealkit=mealkit)
                for mealkit_recipe in mealkit_recipes:
                    CartRecipe.objects.filter(
                        user_cart=user_cart,
                        recipe=mealkit_recipe.recipe
                    ).delete()
                
                cart_mealkit.delete()
            else:
                raise ValueError("Invalid item type.")

            return self.get_cart(user)
        except UserCart.DoesNotExist:
            raise ValueError("Cart does not exist for this user.")
        except CartProduct.DoesNotExist:
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
                item, created = CartRecipe.objects.get_or_create(
                    user_cart=user_cart,
                    id=item_id,
                    defaults={'quantity': new_quantity, 'recipe_id': item_id}  # Assuming item_id is also the recipe_id
                )
                if not created:
                    item.quantity = new_quantity
                    item.save()

                # Update associated CartIngredient quantities
                recipe_ingredients = RecipeIngredient.objects.filter(recipe=item.recipe)
                for ri in recipe_ingredients:
                    cart_ingredient, _ = CartIngredient.objects.get_or_create(
                        user_cart=user_cart,
                        recipe_ingredient=ri,
                        defaults={'quantity': ri.quantity * new_quantity}
                    )
                    if not created:
                        cart_ingredient.quantity = ri.quantity * new_quantity
                        cart_ingredient.save()
                    
            elif item_type == 'mealkit':
                item = CartMealKit.objects.get(user_cart=user_cart, id=item_id)
                
                mealkit = item.mealkit
                mealkit_recipes = MealKitRecipe.objects.filter(mealkit=mealkit)
                for mealkit_recipe in mealkit_recipes:
                    cart_recipe = CartRecipe.objects.get(
                        user_cart=user_cart,
                        recipe=mealkit_recipe.recipe
                    )
                    cart_recipe.quantity = mealkit_recipe.quantity * new_quantity
                    cart_recipe.save()
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