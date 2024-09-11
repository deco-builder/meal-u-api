from django.db.models import Q
from ..models import Ingredient
from ..serializers.ingredients import IngredientsSerializer


class IngredientsServices:
    def get(self, categories=None, dietary_details=None, search=None):
        try:
            queryset = Ingredient.objects.select_related(
                "category_id", "unit_id"
            ).prefetch_related("ingredientdietarydetail_set__dietary_details")

            if categories:
                queryset = queryset.filter(category_id__name__in=categories)

            if dietary_details:
                queryset = queryset.filter(
                    ingredientdietarydetail__dietary_details__name__in=dietary_details
                ).distinct()

            if search:
                queryset = queryset.filter(
                    Q(name__icontains=search) | Q(description__icontains=search)
                )

            if dietary_details:
                queryset = queryset.filter(
                    ingredientdietarydetail__dietary_details__name__in=dietary_details
                ).distinct()

            ingredients = queryset.all()
            serializer = IngredientsSerializer(ingredients, many=True)
            return serializer.data
        except Exception as e:
            raise e
