from orders.models import DeliveryDetails, DeliveryLocation, DeliveryTimeSlot
from ..serializers.delivery import DeliveryDetailsSerializer, DeliveryLocationSerializer, DeliveryTimeSlotSerializer

class DeliveryService:
    @staticmethod
    def add_delivery_details(order_id, delivery_location_id, delivery_time_id, delivery_date):
        """
        Adds delivery details for a specific order.
        """
        try:
            delivery_details = DeliveryDetails.objects.create(
                order_id=order_id,
                delivery_location_id=delivery_location_id,
                delivery_time_id=delivery_time_id,
                delivery_date=delivery_date
            )
            serializer = DeliveryDetailsSerializer(delivery_details)
            return serializer.data
        except Exception as e:
            raise e

    def get_all_delivery_locations():
        delivery_locations = DeliveryLocation.objects.all()
        serializer = DeliveryLocationSerializer(delivery_locations, many=True)
        return serializer.data

    @staticmethod
    def get_all_delivery_time_slots():
        delivery_time_slots = DeliveryTimeSlot.objects.all()
        serializer = DeliveryTimeSlotSerializer(delivery_time_slots, many=True)
        return serializer.data
