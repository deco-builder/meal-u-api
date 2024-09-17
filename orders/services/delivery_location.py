from ..models import DeliveryLocation
from ..serializers.delivery_location import DeliveryLocationSerializer

def get_all_delivery_locations():
    delivery_locations = DeliveryLocation.objects.all()
    serializer = DeliveryLocationSerializer(delivery_locations, many=True)
    return serializer.data
