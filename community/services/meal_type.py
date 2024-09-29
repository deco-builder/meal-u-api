from ..models import MealType
from ..serializers.meal_type import MealTypeSerializer


class MealTypeServices:
    def get(self):
        try:
            meal_types = MealType.objects.all()
            serializer = MealTypeSerializer(meal_types, many=True)
            return serializer.data
        except Exception as e:
            raise e
