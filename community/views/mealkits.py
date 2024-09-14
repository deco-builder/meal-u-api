from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..services.mealkits import MealKitsServices
from applibs.response import prepare_success_response, prepare_error_response


class MealKitsView(APIView):
    def __init__(self):
        self.meal_kit_service = MealKitsServices()

    def get(self, request):
        try:
            response = self.meal_kit_service.get()
            return Response(prepare_success_response(response), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)
