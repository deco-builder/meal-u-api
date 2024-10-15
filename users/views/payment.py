from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..services.payment import PaymentService
from applibs.response import prepare_success_response, prepare_error_response
from rest_framework.permissions import IsAuthenticated
from ..serializers.payment import UserPaymentMethodSerializer
from users.models import UserPaymentMethod

class UserPaymentMethodView(APIView):                           
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handles the request to add a new payment method for a user.
        """
        user_id = request.user.id
        method_id = request.data.get('method')
        last_four_digits = request.data.get('last_four_digits')
        expiration_date = request.data.get('expiration_date')

        try:
            # Add payment method
            payment_method = PaymentService.add_payment_method(
                user_id=user_id,
                method_id=method_id,
                last_four_digits=last_four_digits,
                expiration_date=expiration_date
            )
            return Response(prepare_success_response(payment_method), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        """
        Retrieves all payment methods for the authenticated user.
        """
        user = request.user

        try:
            # Use the PaymentService to get payment methods
            payment_methods_data = PaymentService.get_payment_methods(user)
            return Response(prepare_success_response(payment_methods_data), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)
