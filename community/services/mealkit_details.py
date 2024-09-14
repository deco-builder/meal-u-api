from ..models import MealKit
from ..serializers.mealkit_details import MealKitDetailsSerializer


class MealKitDetailsServices:
    def get(self, mealkit_id):
        try:
            mealkit = MealKit.objects.prefetch_related("mealkitdietarydetail_set__dietary_details").get(id=mealkit_id)
            serializer = MealKitDetailsSerializer(mealkit)
            return serializer.data
        except Exception as e:
            raise e
