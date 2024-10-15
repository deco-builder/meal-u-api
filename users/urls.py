from django.urls import path
from .views.payment import UserPaymentMethodView
from .views.user import UserDetailView, CreatorDetailView
from django.urls import re_path

urlpatterns = [
    path('payment-methods/', UserPaymentMethodView.as_view(), name='user_payment_methods'),
    # path('user-profile/', UserDetailView.as_view(), name="user-profile"),
    re_path(r'^user-profile/?$', UserDetailView.as_view(), name="user-profile"),
    path('creator-profile/<int:user_id>/', UserDetailView.as_view(), name="creator-profile")
]