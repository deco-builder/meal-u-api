from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from user_auth.permission import IsWarehouseUser, IsClientUser, IsCourierUser
from applibs.response import prepare_success_response, prepare_error_response
from ..services.order_status import OrderStatusPreparingService, OrderStatusReadyToDeliverService, OrderStatusPaidService, OrderStatusDeliveringService, OrderStatusDeliveredService, OrderStatusCompletedService
from rest_framework.parsers import MultiPartParser, FormParser

class OrderStatusPaidUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsClientUser]

    def __init__(self):
        self.order_status_paid_service = OrderStatusPaidService()

    def post(self, request, order_id):
        
        try:
            use_voucher = request.data.get("use_voucher", False)  # Get the flag from the request body
            response = self.order_status_paid_service.post(order_id, use_voucher)
            return Response(prepare_success_response(response), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST
            )

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

class OrderStatusDeliveringUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsCourierUser]

    def __init__(self):
        self.order_status_delivering_service = OrderStatusDeliveringService()
    def post(self, request, order_id):
        try:
            response = self.order_status_delivering_service.post(order_id)
            return Response(prepare_success_response(f"Order {order_id} status updated to 'delivering'"), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST
            )

class OrderStatusDeliveredUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsCourierUser]
    parser_classes = (MultiPartParser, FormParser)
    
    def __init__(self):
        self.order_status_delivered_service = OrderStatusDeliveredService() 

    def post(self, request, order_id):
        try:
            photo_proof = request.FILES.get('photo_proof', None)

            order = self.order_status_delivered_service.post(order_id, photo_proof)

            return Response(prepare_success_response(f"Order {order_id} status updated to 'delivered' with photo proof"), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST
            )

class OrderStatusCompletedUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsClientUser]

    def __init__(self):
        self.order_status_completed_service = OrderStatusCompletedService() 

    def post(self, request, order_id):
        try:
            user_passcode = request.data.get('passcode')

            if not user_passcode:
                return Response(prepare_error_response("Passcode is required"), status=status.HTTP_400_BAD_REQUEST)

            order = self.order_status_completed_service.post(order_id, user_passcode)
            
            return Response(prepare_success_response(f"Order {order_id} status updated to 'completed'"), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST
            )
