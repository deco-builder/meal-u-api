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
    def update_order_status_to_delivering(order_id):
        """
        Updates the status of the order to 'delivering'
        """
        try:
            delivering_status = OrderStatuses.objects.get(name='delivering')

            order = Orders.objects.get(id=order_id)

            order.order_status = delivering_status
            order.save()

            return order
        except Orders.DoesNotExist:
            raise Exception(f"Order with id {order_id} does not exist")
        except OrderStatuses.DoesNotExist:
            raise Exception("The 'delivering' status does not exist")
        except Exception as e:
            raise e
    
    @staticmethod
    def update_order_status_to_delivered(order_id, photo_proof):
        """
        Updates the status of the order to 'delivered' and saves the photo proof.
        """
        try:
            delivered_status = OrderStatuses.objects.get(name='delivered')
            order = Orders.objects.get(id=order_id)

            # Check if a photo proof is provided
            if not photo_proof:
                raise Exception("Photo proof is required to mark the order as 'delivered'.")

            # Save the photo proof and update order status
            order.delivery_proof_photo = photo_proof
            order.order_status = delivered_status
            order.save()

            return order
        except Orders.DoesNotExist:
            raise Exception(f"Order with id {order_id} does not exist")
        except OrderStatuses.DoesNotExist:
            raise Exception("The 'delivered' status does not exist")
        except Exception as e:
            raise e
    
    @staticmethod
    def update_order_status_to_completed(order_id, user_passcode):
        """
        Updates the order status to 'completed' after verifying the provided passcode.
        """
        try:
            # Retrieve the 'completed' status from the OrderStatuses table
            completed_status = OrderStatuses.objects.get(name='completed')

            # Fetch the order by its ID
            order = Orders.objects.get(id=order_id)

            # Verify if the provided passcode matches the stored one
            if order.passcode != user_passcode:
                raise Exception("Invalid passcode")

            # Update the order's status to 'completed'
            order.order_status = completed_status
            order.save()

            return order
        except Orders.DoesNotExist:
            raise Exception(f"Order with id {order_id} does not exist")
        except OrderStatuses.DoesNotExist:
            raise Exception("The 'completed' status does not exist")
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