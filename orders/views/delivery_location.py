from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..services.delivery import DeliveryService
from applibs.response import prepare_success_response, prepare_error_response
from rest_framework.permissions import IsAuthenticated

class DeliveryLocationListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            delivery_locations_data = DeliveryService.get_all_delivery_locations()
            return Response(prepare_success_response(delivery_locations_data), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)
        