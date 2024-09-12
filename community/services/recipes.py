from django.db.models import Q
from ..models import Recipe
from ..serializers.recipes import RecipesSerializer


class RecipesService:
    def get(self, dietary_details=None, search=None):
        try:
            queryset = Recipe.objects.select_related("meal_type").prefetch_related(
                "recipedietarydetail_set__dietary_details",
                "recipeingredient_set__ingredient",
                "recipeingredient_set__preparation_type",
            )

            if search:
                queryset = queryset.filter(Q(name__icontains=search) | Q(description__icontains=search))

            if dietary_details:
                queryset = queryset.filter(recipedietarydetail__dietary_details__name__in=dietary_details).distinct()

            recipes = queryset.all()
            serializer = RecipesSerializer(recipes, many=True)
            return serializer.data
        except Exception as e:
            raise e