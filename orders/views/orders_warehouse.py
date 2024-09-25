from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from user_auth.permission import IsWarehouseUser
from applibs.response import prepare_success_response, prepare_error_response
from ..services.orders_warehouse import OrderWarehouseService


class OrderWarehouseView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsWarehouseUser]

    def __init__(self):
        self.order_warehouse_service = OrderWarehouseService()

    def get(self, request):
        try:
            response = self.order_warehouse_service.get()
            return Response(prepare_success_response(response), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)
