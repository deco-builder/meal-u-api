from django.urls import path
from .views.payment import UserPaymentMethodView

urlpatterns = [
    path('payment-methods/', UserPaymentMethodView.as_view(), name='user_payment_methods'),
]
