import json
from ..models import Recipe
from ..serializers.recipe_details import RecipeDetailsSerializer
from ..serializers.create_recipe import (
    RecipeSerializer,
    IngredientSerializer,
    RecipeIngredientSerializer,
    RecipeDietaryDetailSerializer,
)
from groceries.models import PreparationType


class RecipeDetailsService:
    def get(self, recipe_id):
        try:
            product = (
                Recipe.objects.select_related("meal_type")
                .prefetch_related(
                    "recipedietarydetail_set__dietary_details",
                    "recipeingredient_set__ingredient",
                    "recipeingredient_set__preparation_type",
                )
                .get(id=recipe_id)
            )
            return RecipeDetailsSerializer(product).data
        except Exception as e:
            raise e

    def post(self, data, user, image):
        try:
            recipe = json.loads(data.get("recipe", {}))
            recipe["creator"] = user.id
            recipe["image"] = image

            recipe_serializer = RecipeSerializer(data=recipe)
            recipe_serializer.is_valid(raise_exception=True)
            recipe = recipe_serializer.save()

            ingredients_data = json.loads(data.get("ingredients", []))
            for ingredient_data in ingredients_data:
                ingredient = ingredient_data.get("ingredient", {})
                ingredient = {
                    "name": ingredient.get("name"),
                    "product_id": ingredient.get("product_id"),
                    "unit_id": ingredient.get("unit_id"),
                    "unit_size": ingredient.get("unit_size"),
                    "description": ingredient.get("description"),
                }

                ingredient_serializer = IngredientSerializer(data=ingredient)
                ingredient_serializer.is_valid(raise_exception=True)
                ingredient = ingredient_serializer.save()

                preparation_type = ingredient_data.get("preparation_type", 0)
                if preparation_type != None:
                    preparation_type_object = PreparationType.objects.get(id=preparation_type)
                else:
                    preparation_type_object = None

                recipe_ingredient_data = {
                    "recipe": recipe.id,
                    "ingredient": ingredient.id,
                    "preparation_type": preparation_type_object.id if preparation_type_object != None else None,
                }
                recipe_ingredient_serializer = RecipeIngredientSerializer(data=recipe_ingredient_data)
                recipe_ingredient_serializer.is_valid(raise_exception=True)
                recipe_ingredient_serializer.save()

            dietary_details = json.loads(data.get("dietary_details", []))
            for dietary_detail in dietary_details:
                dietary_detail_data = {"recipe": recipe.id, "dietary_details": dietary_detail}
                recipe_dietary_detail_serializer = RecipeDietaryDetailSerializer(data=dietary_detail_data)
                recipe_dietary_detail_serializer.is_valid(raise_exception=True)
                recipe_dietary_detail_serializer.save()

            return self.get(recipe.id)

        except Exception as e:
            raise e
