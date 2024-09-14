from ..models import MealKit
from ..serializers.mealkits import MealKitsSerializer


class MealKitsServices:
    def get(self):
        try:
            queryset = MealKit.objects.prefetch_related("mealkitdietarydetail_set__dietary_details").all()
            serializer = MealKitsSerializer(queryset, many=True)
            return serializer.data
        except Exception as e:
            raise e
