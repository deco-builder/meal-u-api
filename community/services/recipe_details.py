from django.db.models import Q
from ..models import Recipe
from ..serializers.recipe_details import RecipeDetailsSerializer


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
