from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from user_auth.permission import IsWarehouseUser, IsClientUser
from applibs.response import prepare_success_response, prepare_error_response
from ..services.product_details import ProductDetailsService


class ProductDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsWarehouseUser | IsClientUser]
    
    def __init__(self):
        self.product_service = ProductDetailsService()

    def get(self, request, product_id):
        try:
            response = self.product_service.get(product_id=product_id)

            return Response(prepare_success_response(response), status=status.HTTP_200_OK)

        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)
