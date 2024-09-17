from ..models import DeliveryTimeSlot
from ..serializers.delivery_time_slot import DeliveryTimeSlotSerializer

class DeliveryTimeSlotService:
    @staticmethod
    def get_all_delivery_time_slots():
        delivery_time_slots = DeliveryTimeSlot.objects.all()
        serializer = DeliveryTimeSlotSerializer(delivery_time_slots, many=True)
        return serializer.data
