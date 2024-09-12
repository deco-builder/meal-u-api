from ..models import Orders, OrderStatuses
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
    
    @staticmethod
    def update_order_status_to_paid(order_id):
        """
        Updates the status of the order to 'Paid'.
        """
        try:
            # Retrieve the 'Paid' status from the OrderStatuses table
            paid_status = OrderStatuses.objects.get(name='Paid')

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