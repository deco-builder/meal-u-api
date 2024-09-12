from django.urls import path
from .views.payment import AddPaymentMethodView

urlpatterns = [
    path('add-payment-method/', AddPaymentMethodView.as_view(), name='add_payment_method'),
]
