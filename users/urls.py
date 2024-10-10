from django.urls import path
from .views.payment import UserPaymentMethodView
from .views.user import UserDetailView

urlpatterns = [
    path('payment-methods/', UserPaymentMethodView.as_view(), name='user_payment_methods'),
    path('user-profile/', UserDetailView.as_view(), name="user-profile")
]
