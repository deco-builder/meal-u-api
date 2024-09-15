from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ..services.orders import OrdersService  # Import the service
from applibs.response import prepare_success_response, prepare_error_response
from rest_framework.permissions import IsAuthenticated

class OrderListView(APIView):
    permission_classes = [IsAuthenticated]
    """
    API View to retrieve all orders.
    """
    def __init__(self):
        self.orders_service = OrdersService

    def get(self, request):
        user = request.user  # Get the authenticated user
        try:
            response = self.orders_service.get_all_orders_for_user(user)  # Fetch serialized data directly
            return Response(prepare_success_response(response), status=status.HTTP_200_OK)  # Return serialized data
            
        except Exception as e:
            return Response(
                prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST
            )

class OrderStatusUpdateView(APIView):
    """
    API View to update an order status to 'Paid'.
    """
    def post(self, request, order_id):
        try:
            # Call the service layer to update the status to 'Paid'
            order = OrdersService.update_order_status_to_paid(order_id)
            return Response(prepare_success_response(f"Order {order_id} status updated to 'Paid'"), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST
            )
