from django.urls import path
from .views.orders import OrderListView, OrderStatusUpdateView

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:order_id>/status/paid/', OrderStatusUpdateView.as_view(), name='order-status-paid'),
]
