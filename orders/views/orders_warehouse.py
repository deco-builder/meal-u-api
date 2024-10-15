from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from user_auth.permission import IsWarehouseUser, IsCourierUser
from applibs.response import prepare_success_response, prepare_error_response
from ..services.orders_warehouse import OrderWarehouseService
from datetime import datetime


class OrderWarehouseView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsWarehouseUser | IsCourierUser]

    def __init__(self):
        self.order_warehouse_service = OrderWarehouseService()

    def get(self, request):
        try:
            start_date = request.query_params.get("start_date")
            end_date = request.query_params.get("end_date")

            if start_date:
                try:
                    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                except ValueError:
                    raise Exception("Invalid start_date format")

            if end_date:
                try:
                    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                except ValueError:
                    raise Exception("Invalid end_date format")

            response = self.order_warehouse_service.get(start_date=start_date, end_date=end_date)
            return Response(prepare_success_response(response), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)
