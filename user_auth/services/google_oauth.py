import requests
from django.conf import settings
from ..models import User
from rest_framework_simplejwt.tokens import RefreshToken


class GoogleOAuthService:
    def get(self, request):
        try:
            auth_code = request.query_params.get("code")
            if not auth_code:
                raise Exception("Authorization code not provided")

            tokens = exchange_token_with_google(auth_code)
            if not tokens:
                raise Exception("Failed to get tokens from Google")

            user_info = validate_google_token(tokens.get("id_token"))
            if not user_info:
                raise Exception("Invalid token")

            user = create_or_update_user(user_info)
            if not user:
                raise Exception("Failed to get user details")

            refresh = RefreshToken.for_user(user)
            image_url = user.image.url if user.image else None

            return {
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "profile_picture": image_url,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

        except Exception as e:
            raise e


def exchange_token_with_google(auth_code: str):
    data = {
        "code": auth_code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post("https://oauth2.googleapis.com/token", data=data)
    if response.status_code == 200:
        return response.json()
    return None


def validate_google_token(id_token: str):
    url = f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


def create_or_update_user(user_info):
    email = user_info.get("email")
    if not email:
        raise Exception("Invalid user data.")

    user, _ = User.objects.get_or_create(
        email=email,
        first_name=user_info.get("given_name", ""),
        last_name=user_info.get("family_name", ""),
    )

    return user
