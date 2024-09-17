from django.urls import path
from .views.orders import OrderListView, OrderStatusUpdateView, OrderDetailView
from .views.delivery_details import AddDeliveryDetailsView
from .views.checkout import CheckoutView  # Import the CheckoutView

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:order_id>/status/paid/', OrderStatusUpdateView.as_view(), name='order-status-paid'),
    path('add-delivery-details/', AddDeliveryDetailsView.as_view(), name='add-delivery-details'),
    path('orders/<int:order_id>/', OrderDetailView.as_view(), name='order-detail'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]
