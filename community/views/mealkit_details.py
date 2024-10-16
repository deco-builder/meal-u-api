from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from user_auth.permission import IsWarehouseUser, IsClientUser
from applibs.response import prepare_success_response, prepare_error_response
from ..services.mealkit_details import MealKitDetailsServices



class MealkitDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsWarehouseUser | IsClientUser]

    def __init__(self):
        self.mealkit_details_service = MealKitDetailsServices()

    def get(self, request, mealkit_id):
        try:
            response = self.mealkit_details_service.get(mealkit_id=mealkit_id)
            return Response(prepare_success_response(response), status=status.HTTP_200_OK)

        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)

class MealKitView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsWarehouseUser | IsClientUser]

    def __init__(self):
        self.mealkit_details_service = MealKitDetailsServices()

    def post(self, request):
        try:
            user = request.user
            image = request.FILES.get("image", None)
            response = self.mealkit_details_service.post(request.data, user, image)
            return Response(prepare_success_response(response), status=status.HTTP_200_OK)

        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)
