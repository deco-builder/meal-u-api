from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from user_auth.permission import IsWarehouseUser, IsClientUser
from ..services.mealkits import MealKitsServices, CombinedService
from applibs.response import prepare_success_response, prepare_error_response


class MealKitsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsWarehouseUser | IsClientUser]
    
    def __init__(self):
        self.meal_kit_service = MealKitsServices()

    def get(self, request):
        try:
            dietary_details = request.query_params.getlist("dietary_details")
            search = request.query_params.get("search", None)
            creator = request.query_params.get("creator", None)

            if dietary_details:
                dietary_details = list(map(str, dietary_details))

            response = self.meal_kit_service.get(dietary_details=dietary_details, search=search, creator=creator)
            return Response(prepare_success_response(response), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)

class TrendingMealKitsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsClientUser]
    
    def __init__(self):
        self.meal_kit_service = MealKitsServices()

    def get(self, request):
        try:
            response = self.meal_kit_service.get_trending_mealkits()
            return Response(prepare_success_response(response), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)

class CommunityMealKitsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsWarehouseUser | IsClientUser]
    
    def __init__(self):
        self.meal_kit_service = MealKitsServices()

    def get(self, request):
        try:
            response = self.meal_kit_service.get_with_stats(request.user)
            return Response(prepare_success_response(response), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)

class CombinedMealKitRecipeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsClientUser | IsWarehouseUser]

    def __init__(self):
        self.combined_service = CombinedService()

    def get(self, request):
        try:
            response = self.combined_service.get_combined_mealkits_and_recipes()
            return Response(prepare_success_response(response), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)
