from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers.user import UserSerializer
from ..services.user import UserService
from applibs.response import prepare_success_response, prepare_error_response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            user = request.user  
            serializer = UserSerializer(user)  
            return Response(prepare_success_response(serializer.data), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, *args, **kwargs):
        try:
            print("test")
            user = request.user
            updated_user = UserService.update_user_profile(user, request.data)
            serializer = UserSerializer(updated_user)
            return Response(prepare_success_response(serializer.data), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST
            )