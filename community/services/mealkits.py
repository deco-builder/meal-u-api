from ..models import MealKit
from ..serializers.mealkits import MealKitsSerializer
from django.db.models import Q, Count


class MealKitsServices:
    def get(self, dietary_details=None, search=None):
        try:
            queryset = MealKit.objects.prefetch_related("mealkitdietarydetail_set__dietary_details").annotate(
                likes_count=Count('mealkitlike'),
                comments_count=Count('mealkitcomment') 
            )

            if search:
                queryset = queryset.filter(
                    Q(name__icontains=search)
                    | Q(description__icontains=search)
                    | Q(mealkitrecipe__recipe__recipeingredient__ingredient__product_id__name__icontains=search)
                    | Q(mealkitrecipe__recipe__recipeingredient__ingredient__product_id__description__icontains=search)
                    | Q(
                        mealkitrecipe__recipe__recipeingredient__ingredient__product_id__category_id__name__icontains=search
                    )
                )

            if dietary_details:
                queryset = queryset.filter(mealkitdietarydetail__dietary_details__name__in=dietary_details).distinct()

            mealkits = queryset.all()
            serializer = MealKitsSerializer(mealkits, many=True)
            return serializer.data
        except Exception as e:
            raise e
        