from ..models import Orders
from ..serializers.orders import OrderSerializer

class OrdersService:
    def get_all_orders():
        """
        Retrieves all orders from the database.
        """
        try:
            orders = Orders.objects.all()
            serializer = OrderSerializer(orders, many=True)
            return serializer.data
        except Exception as e:
            raise e