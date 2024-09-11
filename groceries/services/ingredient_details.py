from django.db.models import Q
from ..models import Ingredient
from ..serializers.ingredient_details import IngredientDetailsSerializer


class IngredientDetailsServices:
    def get(self, ingredient_id):
        try:
            ingredient = Ingredient.objects.get(id=ingredient_id)
            return IngredientDetailsSerializer(ingredient).data
        except Exception as e:
            raise e
