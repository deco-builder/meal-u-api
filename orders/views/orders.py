from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ..services.orders import OrdersService  # Import the service
from applibs.response import prepare_success_response, prepare_error_response

class OrderListView(APIView):
    """
    API View to retrieve all orders.
    """

    def get(self, request):
        try:
            orders = OrdersService.get_all_orders()  # Fetch serialized data directly
            return Response(orders, status=status.HTTP_200_OK)  # Return serialized data
            
        except Exception as e:
            return Response(
                prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST
            )
