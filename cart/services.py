from .models import UserCart, CartIngredient, CartProduct, CartRecipe, CartMealKit
from community.models import Recipe, MealKit, Ingredient
from groceries.models import Product, PreparationType
from .serializers import CartProductSerializer, CartRecipeSerializer, CartMealKitSerializer


class CartService:

    def get_cart(self, user):
        try:
            user_cart = UserCart.objects.get(user=user)

            products = CartProduct.objects.filter(user_cart=user_cart).all()
            recipes = CartRecipe.objects.filter(user_cart=user_cart, mealkit__isnull=True).select_related("recipe")
            mealkits = (
                CartMealKit.objects.filter(user_cart=user_cart)
                .select_related("mealkit")
                .prefetch_related(
                    "cartrecipe_set__cartingredient_set__ingredient",
                    "cartrecipe_set__cartingredient_set__preparation_type",
                )
            )

            product_serializer = CartProductSerializer(products, many=True)
            recipe_serializer = CartRecipeSerializer(recipes, many=True)
            mealkit_serializer = CartMealKitSerializer(mealkits, many=True)

            total_price = 0
            for product in product_serializer.data:
                total_price += product["total_price"]
            for recipe in recipe_serializer.data:
                total_price += recipe["total_price"]
            for mealkit in mealkit_serializer.data:
                total_price += mealkit["total_price"]

            return {
                "products": product_serializer.data,
                "recipes": recipe_serializer.data,
                "mealkits": mealkit_serializer.data,
                "total_item": len(product_serializer.data)
                + len(recipe_serializer.data)
                + len(mealkit_serializer.data),
                "total_price": total_price,
            }

        except Exception as e:
            raise e

    def add_item(self, user, item_type, item_data, quantity=1):
        try:
            user_cart, _ = UserCart.objects.get_or_create(user=user)

            if item_type == "recipe":
                return self._add_recipe(user_cart, item_data, quantity)
            elif item_type == "product":
                return self._add_product(user_cart, item_data, quantity)
            elif item_type == "mealkit":
                if not isinstance(item_data, dict) or "mealkit_id" not in item_data:
                    raise ValueError("Invalid mealkit data format. Expected a dictionary with 'mealkit_id'.")
                return self._add_mealkit(user_cart, item_data, quantity)
            else:
                raise ValueError(f"Invalid item type: {item_type}")

        except Exception as e:
            raise e

    def _add_recipe(self, user_cart, item_data, quantity):
        recipe_id = item_data.get("recipe_id")
        recipe_ingredients = item_data.get("recipe_ingredients", [])

        if not recipe_id:
            raise ValueError("Recipe ID is required.")

        recipe = Recipe.objects.get(id=recipe_id)
        cart_recipe, created = CartRecipe.objects.get_or_create(
            user_cart=user_cart, recipe=recipe, mealkit=None, defaults={"quantity": quantity}
        )
        if not created:
            cart_recipe.quantity += quantity
            cart_recipe.save()

        for ri_data in recipe_ingredients:
            ingredient = Ingredient.objects.get(id=ri_data["ingredient_id"])
            if ri_data["preparation_type_id"] != None:
                preparation_type = PreparationType.objects.get(id=ri_data["preparation_type_id"])
            else:
                preparation_type = None
            cart_ingredient, created = CartIngredient.objects.get_or_create(
                user_cart=user_cart,
                ingredient=ingredient,
                preparation_type=preparation_type,
                recipe=cart_recipe,
                defaults={"quantity": ri_data.get("quantity", 1) * quantity},
            )
            if not created:
                cart_ingredient.quantity += ri_data.get("quantity", 1) * quantity
                cart_ingredient.save()

        return self.get_cart(user_cart.user)

    def _add_mealkit_recipe(self, user_cart, item_data, quantity, mealkit):
        recipe_id = item_data.get("recipe_id")
        recipe_ingredients = item_data.get("recipe_ingredients", [])

        if not recipe_id:
            raise ValueError("Recipe ID is required.")

        recipe = Recipe.objects.get(id=recipe_id)
        cart_recipe = CartRecipe.objects.create(user_cart=user_cart, recipe=recipe, quantity=quantity, mealkit=mealkit)
        cart_recipe.save()

        for ri_data in recipe_ingredients:
            ingredient = Ingredient.objects.get(id=ri_data["ingredient_id"])
            if ri_data["preparation_type_id"] != None:
                preparation_type = PreparationType.objects.get(id=ri_data["preparation_type_id"])
            else:
                preparation_type = None
            cart_ingredient, created = CartIngredient.objects.get_or_create(
                user_cart=user_cart,
                ingredient=ingredient,
                preparation_type=preparation_type,
                recipe=cart_recipe,
                defaults={"quantity": ri_data.get("quantity", 1) * quantity},
            )
            cart_ingredient.save()

        return cart_recipe

    def _add_product(self, user_cart, item_data, quantity):
        product = Product.objects.get(id=item_data)
        cart_item, created = CartProduct.objects.get_or_create(
            user_cart=user_cart, product=product, defaults={"quantity": quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        serializer = CartProductSerializer(cart_item)
        return self.get_cart(user_cart.user)

    def _add_mealkit(self, user_cart, item_data, quantity):
        mealkit_id = item_data.get("mealkit_id")
        recipes = item_data.get("recipes", [])

        if not mealkit_id:
            raise ValueError("MealKit ID is required.")

        try:
            mealkit = MealKit.objects.get(id=mealkit_id)
        except MealKit.DoesNotExist:
            raise ValueError(f"MealKit with ID {mealkit_id} does not exist.")

        cart_mealkit, created = CartMealKit.objects.get_or_create(
            user_cart=user_cart, mealkit=mealkit, defaults={"quantity": quantity}
        )
        cart_mealkit.save()
        if not created:
            cart_mealkit.quantity += quantity
            cart_mealkit.save()

        for recipe_data in recipes:
            recipe_cart = self._add_mealkit_recipe(
                user_cart, recipe_data, recipe_data.get("quantity", 1) * quantity, cart_mealkit
            )

        return self.get_cart(user_cart.user)

    def remove_item(self, user, item_type, item_id):
        try:
            user_cart = UserCart.objects.get(user=user)

            if item_type == "ingredient":
                CartIngredient.objects.filter(user_cart=user_cart, id=item_id).delete()
            elif item_type == "product":
                CartProduct.objects.filter(user_cart=user_cart, id=item_id).delete()
            elif item_type == "recipe":
                CartRecipe.objects.filter(user_cart=user_cart, id=item_id).delete()
            elif item_type == "mealkit":
                cart_mealkit = CartMealKit.objects.get(user_cart=user_cart, id=item_id).delete()
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

            if item_type == "product":
                item = CartProduct.objects.get(user_cart=user_cart, id=item_id)
                item.quantity = new_quantity
                item.save()

            elif item_type == "ingredient":
                item = CartIngredient.objects.get(user_cart=user_cart, id=item_id)
                item.quantity = new_quantity
                item.save()

            elif item_type == "recipe":
                item = CartRecipe.objects.get(user_cart=user_cart, id=item_id)
                old_quantity = item.quantity
                item.quantity = new_quantity
                item.save()

                ingredients = CartIngredient.objects.filter(user_cart=user_cart, recipe=item)
                for ingredient in ingredients:
                    old_ingredient_quantity = ingredient.quantity
                    new_ingredient_quantity = max(old_ingredient_quantity / old_quantity * new_quantity, 1)
                    ingredient.quantity = new_ingredient_quantity
                    ingredient.save()

            elif item_type == "mealkit":
                item = CartMealKit.objects.get(user_cart=user_cart, id=item_id)
                old_quantity = item.quantity
                item.quantity = new_quantity
                item.save()

                recipes = CartRecipe.objects.filter(user_cart=user_cart, mealkit=item)
                for recipe in recipes:
                    old_recipe_quantity = recipe.quantity
                    new_recipe_quantity = max(old_recipe_quantity / old_quantity * new_quantity, 1)
                    self.update_item_quantity(user, "recipe", recipe.id, new_recipe_quantity)

            return self.get_cart(user)

        except UserCart.DoesNotExist:
            raise ValueError("Cart does not exist for this user.")
        except (CartIngredient.DoesNotExist, CartProduct.DoesNotExist, CartMealKit.DoesNotExist):
            raise ValueError(f"{item_type.capitalize()} not found in the cart.")
        except Exception as e:
            raise e

    def update_ingredient_preparation_type(self, user, item_id, new_preparation_type):
        try:
            user_cart = UserCart.objects.get(user=user)
            item = CartIngredient.objects.get(user_cart=user_cart, id=item_id)
            if new_preparation_type != None:
                preparation_type = PreparationType.objects.get(id=new_preparation_type)
            else:
                preparation_type = None
            item.preparation_type = preparation_type
            item.save()
            return self.get_cart(user)
        except UserCart.DoesNotExist:
            raise ValueError("Cart does not exist for this user.")
        except (CartIngredient.DoesNotExist,):
            raise ValueError(f"{item_id.capitalize()} not found in the cart.")
        except Exception as e:
            raise e

    def put(self, user, item_type, item_id, new_quantity, request):
        try:
            if item_type == "ingredient":
                new_preparation_type = request.data.get("preparation_type", None)
                self.update_ingredient_preparation_type(user, item_id, new_preparation_type)
            self.update_item_quantity(request.user, item_type, item_id, new_quantity)
            return self.get_cart(user)
        except Exception as e:
            raise e
