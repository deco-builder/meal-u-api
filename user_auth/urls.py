from django.urls import path
from .views.login import LoginView
from .views.register import RegisterView
from .views.google_oauth import GoogleOAuthView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("oauth/google/", GoogleOAuthView.as_view(), name="OAuth Google"),
]
