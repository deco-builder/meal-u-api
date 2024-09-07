from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from applibs.response import prepare_success_response, prepare_error_response
from ..serializers.login import LoginSerializer
from ..models import User


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    refresh = RefreshToken.for_user(user)
                    return Response(
                        prepare_success_response(
                            {
                                "email": user.email,
                                "first_name": user.first_name,
                                "last_name": user.last_name,
                                "refresh": str(refresh),
                                "access": str(refresh.access_token),
                            }
                        ),
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        prepare_error_response("Invalid password"),
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
            except User.DoesNotExist:
                return Response(
                    prepare_error_response("Invalid email"),
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        return Response(
            prepare_error_response(serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )
