from django.urls import path
from .views.orders import OrderListView, OrderStatusUpdateView
from .views.delivery_details import AddDeliveryDetailsView

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:order_id>/status/paid/', OrderStatusUpdateView.as_view(), name='order-status-paid'),
    path('add-delivery-details/', AddDeliveryDetailsView.as_view(), name='add-delivery-details'),

]
