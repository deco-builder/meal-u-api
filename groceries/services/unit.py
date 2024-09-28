from ..models import Unit
from ..serializers.unit import UnitSerializer


class UnitServices:
    def get(self):
        try:
            units = Unit.objects.all()
            serializer = UnitSerializer(units, many=True)
            return serializer.data
        except Exception as e:
            raise e