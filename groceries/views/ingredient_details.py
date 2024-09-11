from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from applibs.response import prepare_success_response, prepare_error_response
from ..services.ingredient_details import IngredientDetailsServices


class IngredientDetailsView(APIView):
    def __init__(self):
        self.ingredient_details = IngredientDetailsServices()

    def get(self, request, ingredient_id):
        try:
            response = self.ingredient_details.get(ingredient_id=ingredient_id)

            return Response(prepare_success_response(response), status=status.HTTP_200_OK)

        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)
