from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from user_auth.permission import IsWarehouseUser, IsClientUser
from applibs.response import prepare_success_response, prepare_error_response
from ..services.categories import CategoryServices


class CategoryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsWarehouseUser | IsClientUser]

    def __init__(self):
        self.category_service = CategoryServices()

    def get(self, request):
        try:
            response = self.category_service.get()
            return Response(
                prepare_success_response(response), status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST
            )
