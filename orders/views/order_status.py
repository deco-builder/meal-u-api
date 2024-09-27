from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from user_auth.permission import IsWarehouseUser
from applibs.response import prepare_success_response, prepare_error_response
from ..services.order_status import OrderStatusPreparingService, OrderStatusReadyToDeliverService


class OrderStatusPreparingView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsWarehouseUser]

    def __init__(self):
        self.order_status_preparing_service = OrderStatusPreparingService()

    def post(self, request, order_id):
        try:
            response = self.order_status_preparing_service.post(order_id)
            return Response(prepare_success_response(response), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)
        

class OrderStatusReadyToDeliverView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsWarehouseUser]

    def __init__(self):
        self.order_status_ready_to_deliver = OrderStatusReadyToDeliverService()

    def post(self, request, order_id):
        try:
            response = self.order_status_ready_to_deliver.post(order_id)
            return Response(prepare_success_response(response), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)
