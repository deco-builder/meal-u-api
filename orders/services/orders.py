from ..models import Orders, OrderStatuses
from ..serializers.orders import OrderSerializer
from ..serializers.order_details import OrderDetailSerializer

class OrdersService:    
    def get_all_orders_for_user(user):
        """
        Retrieves all orders from the database.
        """
        try:
            orders = Orders.objects.filter(user_id=user.id)
            serializer = OrderSerializer(orders, many=True)
            return serializer.data
        except Exception as e:
            raise e
    
    @staticmethod
    def update_order_status_to_paid(order_id):
        """
        Updates the status of the order to 'Paid'.
        """
        try:
            # Retrieve the 'Paid' status from the OrderStatuses table
            paid_status = OrderStatuses.objects.get(name='paid')

            # Fetch the order by its ID
            order = Orders.objects.get(id=order_id)

            # Update the order's status
            order.order_status = paid_status
            order.save()

            return order
        except Orders.DoesNotExist:
            raise Exception(f"Order with id {order_id} does not exist")
        except OrderStatuses.DoesNotExist:
            raise Exception("The 'Paid' status does not exist")
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