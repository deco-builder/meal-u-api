from orders.models import DeliveryDetails
from ..serializers.delivery_details import DeliveryDetailsSerializer

class DeliveryService:
    @staticmethod
    def add_delivery_details(order_id, user_delivery_location_id, delivery_time_id, delivery_date):
        """
        Adds delivery details for a specific order.
        """
        try:
            delivery_details = DeliveryDetails.objects.create(
                order_id=order_id,
                user_delivery_location_id=user_delivery_location_id,
                delivery_time_id=delivery_time_id,
                delivery_date=delivery_date
            )
            serializer = DeliveryDetailsSerializer(delivery_details)
            return serializer.data
        except Exception as e:
            raise e
