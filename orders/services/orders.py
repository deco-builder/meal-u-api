from ..models import Orders, OrderStatuses
from ..serializers.orders import OrderSerializer
from ..serializers.order_details import OrderDetailSerializer

class OrdersService:    
    def get_all_orders_for_user(user):
        """
        Retrieves all orders from the database and includes related products, recipes, and meal kits..
        """
        try:
            orders = Orders.objects.filter(user_id=user.id).prefetch_related(
                'orderproducts_set', 'orderrecipes_set', 'ordermealkits_set'
            )
            serializer = OrderSerializer(orders, many=True)
            return serializer.data
        except Exception as e:
            raise e
        
    @staticmethod
    def get_order_details(order_id):
        try:
            order = Orders.objects.get(id=order_id)
            serializer = OrderDetailSerializer(order)
            return serializer.data
        except Orders.DoesNotExist:
            raise Exception(f"Order with id {order_id} does not exist")
        except Exception as e:
            raise e
    
    @staticmethod
    def get_orders_by_status(status):
        try:
            orders = Orders.objects.filter( order_status__name=status)
            serializer = OrderSerializer(orders, many=True)
            return serializer.data
        except Exception as e:
            raise e
