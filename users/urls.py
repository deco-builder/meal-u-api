from django.urls import path
from .views.payment import UserPaymentMethodView
from .views.user import UserDetailView
from django.urls import re_path

urlpatterns = [
    path('payment-methods/', UserPaymentMethodView.as_view(), name='user_payment_methods'),
    re_path(r'^user-profile/?$', UserDetailView.as_view(), name="user-profile"),
]
