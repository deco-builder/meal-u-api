from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..services.delivery_details import DeliveryService
from applibs.response import prepare_success_response, prepare_error_response

class AddDeliveryDetailsView(APIView):
    def post(self, request):
        """
        Handles the request to add new delivery details for an order.
        """
        order_id = request.data.get('order')
        delivery_location_id = request.data.get('delivery_location')
        delivery_time_id = request.data.get('delivery_time')
        delivery_date = request.data.get('delivery_date')

        try:
            # Add delivery details
            delivery_details = DeliveryService.add_delivery_details(
                order_id=order_id,
                delivery_location_id=delivery_location_id,
                delivery_time_id=delivery_time_id,
                delivery_date=delivery_date
            )
            return Response(prepare_success_response(delivery_details), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)
