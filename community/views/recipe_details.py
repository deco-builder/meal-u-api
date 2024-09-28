from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from user_auth.permission import IsWarehouseUser, IsClientUser
from applibs.response import prepare_success_response, prepare_error_response
from ..services.recipe_details import RecipeDetailsService


class RecipeDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsWarehouseUser | IsClientUser]

    def __init__(self):
        self.recipe_details_service = RecipeDetailsService()

    def get(self, request, recipe_id):
        try:
            response = self.recipe_details_service.get(recipe_id=recipe_id)
            return Response(prepare_success_response(response), status=status.HTTP_200_OK)

        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)


class RecipeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsWarehouseUser | IsClientUser]

    def __init__(self):
        self.recipe_details_service = RecipeDetailsService()

    def post(self, request):
        try:
            user = request.user
            image = request.FILES.get("image", None)
            response = self.recipe_details_service.post(request.data, user, image)
            return Response(prepare_success_response(response), status=status.HTTP_200_OK)

        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)
