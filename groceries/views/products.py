from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from user_auth.permission import IsWarehouseUser, IsClientUser
from applibs.response import prepare_success_response, prepare_error_response
from ..services.products import ProductsService


class ProductsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsWarehouseUser | IsClientUser]

    def __init__(self):
        self.products_service = ProductsService()

    def get(self, request):
        try:
            categories = request.query_params.getlist("categories")
            dietary_details = request.query_params.getlist("dietary_details")
            search = request.query_params.get("search", None)

            if categories:
                categories = list(map(str, categories))

            if dietary_details:
                dietary_details = list(map(str, dietary_details))

            response = self.products_service.get(categories=categories, dietary_details=dietary_details, search=search)

            return Response(prepare_success_response(response), status=status.HTTP_200_OK)

        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)
