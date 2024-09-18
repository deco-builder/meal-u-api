from ..models import MealKit
from ..serializers.mealkits import MealKitsSerializer
from django.db.models import Q


class MealKitsServices:
    def get(self, dietary_details=None, search=None):
        try:
            queryset = MealKit.objects.prefetch_related("mealkitdietarydetail_set__dietary_details")

            if search:
                queryset = queryset.filter(Q(name__icontains=search) | Q(description__icontains=search))

            if dietary_details:
                queryset = queryset.filter(mealkitdietarydetail__dietary_details__name__in=dietary_details).distinct()

            mealkits = queryset.all()
            serializer = MealKitsSerializer(mealkits, many=True)
            return serializer.data
        except Exception as e:
            raise e