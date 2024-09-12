from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..services.payment import PaymentService
from applibs.response import prepare_success_response, prepare_error_response

class AddPaymentMethodView(APIView):
    def post(self, request):
        """
        Handles the request to add a new payment method for a user.
        """
        user_id = request.data.get('user')
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
