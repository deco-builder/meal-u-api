from ..models import DietaryDetail
from ..serializers.dietary_details import DietaryDetailSerializer


class DietaryDetailServices:
    def get(self):
        try:
            dietary_details = DietaryDetail.objects.all()
            serializer = DietaryDetailSerializer(dietary_details, many=True)
            return serializer.data
        except Exception as e:
            raise e