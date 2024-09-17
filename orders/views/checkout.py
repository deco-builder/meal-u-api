from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError  
from ..services.checkout import CheckoutService
from applibs.response import prepare_success_response, prepare_error_response
from rest_framework.permissions import IsAuthenticated

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            order = CheckoutService.create_order(request.user, request.data)
            return Response(prepare_success_response({
                'order_id': order.id,
                'total': order.total
            }), status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(prepare_error_response(e.detail), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
