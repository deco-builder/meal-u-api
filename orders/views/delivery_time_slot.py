from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..services.delivery_time_slot import DeliveryTimeSlotService
from rest_framework.permissions import IsAuthenticated
from applibs.response import prepare_success_response, prepare_error_response

class DeliveryTimeSlotListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            delivery_time_slots_data = DeliveryTimeSlotService.get_all_delivery_time_slots()
            return Response(prepare_success_response(delivery_time_slots_data), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)
