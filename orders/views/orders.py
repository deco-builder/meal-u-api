from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ..services.orders import OrdersService  
from applibs.response import prepare_success_response, prepare_error_response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from user_auth.permission import IsWarehouseUser, IsClientUser, IsCourierUser

class OrderListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsClientUser]
    """
    API View to retrieve all orders.
    """
    def __init__(self):
        self.orders_service = OrdersService

    def get(self, request):
        user = request.user
        try:
            response = self.orders_service.get_all_orders_for_user(user)
            return Response(prepare_success_response(response), status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST
            )

class OrderDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            response = OrdersService.get_order_details(order_id)
            return Response(prepare_success_response(response), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST
            )

class OrderListByStatusView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        status_param = request.query_params.get('status', None)
        
        if not status_param:
            return Response(
                prepare_error_response("Status query parameter is required."), 
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            response = OrdersService.get_orders_by_status(status_param)
            if not response:  
                return Response(
                    prepare_error_response("No orders found for the specified status."), 
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(prepare_success_response(response), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST
            )