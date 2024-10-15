from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers.user import UserSerializer
from applibs.response import prepare_success_response, prepare_error_response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from ..models import User

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

class CreatorDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user)  
            return Response(prepare_success_response(serializer.data), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST
            )