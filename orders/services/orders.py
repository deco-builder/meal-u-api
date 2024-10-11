from ..models import Orders, OrderStatuses
from ..serializers.orders import OrderSerializer
from ..serializers.order_details import OrderDetailSerializer
from datetime import datetime
from django.utils import timezone

class OrdersService:    
    def get_all_orders_for_user(user):
        """
        Retrieves all orders from the database and includes related products, recipes, and meal kits..
        """
        try:
            orders = Orders.objects.filter(user_id=user.id).prefetch_related(
                'orderproducts_set', 'orderrecipes_set', 'ordermealkits_set', 'deliverydetails_set__delivery_time'
            )
            # Get current date and time
            current_datetime = timezone.now()
            for order in orders:
                delivery_details = order.deliverydetails_set.first()

                if delivery_details:
                    delivery_date = delivery_details.delivery_date
                    cut_off_time = delivery_details.delivery_time.cut_off

                    cut_off_datetime = datetime.combine(delivery_date, cut_off_time)

                    cut_off_datetime = timezone.make_aware(cut_off_datetime, timezone.get_current_timezone())

                    if current_datetime >= cut_off_datetime:
                        cancelled_status = OrderStatuses.objects.get(name="cancelled")
                        order.order_status = cancelled_status
                        order.save()
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
