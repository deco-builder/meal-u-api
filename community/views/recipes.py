from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from applibs.response import prepare_success_response, prepare_error_response
from ..services.recipes import RecipesService


class RecipesView(APIView):
    def __init__(self):
        self.recipes_service = RecipesService()

    def get(self, request):
        try:
            dietary_details = request.query_params.getlist("dietary_details")
            search = request.query_params.get("search", None)

            if dietary_details:
                dietary_details = list(map(str, dietary_details))

            response = self.recipes_service.get(dietary_details=dietary_details, search=search)
            return Response(prepare_success_response(response), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)
