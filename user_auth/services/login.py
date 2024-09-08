from ..serializers.login import LoginSerializer
from ..models import User
from rest_framework_simplejwt.tokens import RefreshToken


class LoginService:
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data["email"]
                password = serializer.validated_data["password"]
                try:
                    user = User.objects.get(email=email)
                    if user.check_password(password):
                        refresh = RefreshToken.for_user(user)
                        return {
                            "email": user.email,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "refresh": str(refresh),
                            "access": str(refresh.access_token),
                        }
                    else:
                        raise Exception("Invalid password")

                except User.DoesNotExist:
                    raise Exception("Invalid email")

            raise Exception(serializer.errors)

        except Exception as e:
            raise e
